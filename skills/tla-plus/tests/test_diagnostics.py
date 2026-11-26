import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


SKILL = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
PROOF = FIXTURES / "proof"
WITNESS = FIXTURES / "witness"
JAR = os.environ.get("TLA_TOOLS_JAR")


def run_script(name, *args):
    return subprocess.run(
        [sys.executable, SKILL / "scripts" / name, *args],
        capture_output=True, text=True, timeout=30,
    )


class ProofLogTests(unittest.TestCase):
    def summary(self, name, *args):
        result = run_script("summarize_tlaps.py", PROOF / name, *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_successful_log_and_successful_fallback(self):
        for name in ("grouped.log", "Fallback.log"):
            with self.subTest(name=name):
                result = self.summary(name)
                self.assertEqual(result["status"], "complete")
                self.assertEqual(result["unresolved"], [])

    def test_failure_reports_theorem_location_backend_and_time(self):
        result = self.summary("false.log", "--source", PROOF / "FalseGoal.tla")
        self.assertEqual(result["status"], "proof_failure")
        failure, = result["unresolved"]
        self.assertEqual(failure["theorem"], "FalseClaim")
        self.assertEqual(failure["location"]["line"], 4)
        self.assertEqual(failure["last_attempt"]["backend"], "isabelle")
        self.assertEqual(failure["last_attempt"]["elapsed_seconds"], 0.1)

    def test_backend_timeout_uses_reason_and_recorded_zero_time(self):
        result = self.summary("Timeout.log")
        self.assertEqual(result["status"], "timeout")
        timeout, = result["unresolved"]
        self.assertEqual(timeout["last_attempt"]["reason"], "timeout")
        self.assertEqual(timeout["last_attempt"]["elapsed_seconds"], 0.0)

    def test_tlapm_internal_timeout_is_reported_as_timeout(self):
        with TemporaryDirectory() as directory:
            log = Path(directory) / "internal.log"
            log.write_text(
                (PROOF / "Timeout.log").read_text().replace(
                    "@!!reason:timeout", "@!!reason:internal timeout"),
                encoding="utf-8",
            )
            result = self.summary(log)
        self.assertEqual(result["status"], "timeout")
        self.assertEqual(result["unresolved"][0]["last_attempt"]["reason"], "internal timeout")

    def test_recognizes_digit_leading_theorem_name_after_nested_comment(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "FalseGoal.tla"
            source.write_text(
                (PROOF / "FalseGoal.tla").read_text().replace(
                    "THEOREM FalseClaim", '(* " (* inner *)" *) THEOREM 1FalseClaim'),
                encoding="utf-8",
            )
            result = self.summary("false.log", "--source", source)
        self.assertEqual(result["unresolved"][0]["theorem"], "1FalseClaim")

    def test_truncated_log_keeps_the_last_complete_attempt(self):
        result = self.summary("truncated.log")
        self.assertEqual(result["status"], "incomplete_log")
        first, pending = result["unresolved"]
        self.assertEqual(first["last_attempt"]["status"], "being proved")
        self.assertIsNone(first["last_attempt"]["elapsed_seconds"])
        self.assertIsNone(pending["last_attempt"])

    def test_runner_memory_evidence(self):
        result = self.summary("truncated.log", "--runner-status", PROOF / "oom.json")
        self.assertEqual(result["status"], "memory_exhaustion")
        self.assertIn("OOMKilled", result["runner"]["evidence"])


class TraceTests(unittest.TestCase):
    def inspect(self, trace, state, *predicates):
        return run_script(
            "inspect_tlc_state.py", "--jar", JAR or "unused.jar", "--variables", "x",
            "--constants", WITNESS / "constants.cfg", WITNESS / trace,
            WITNESS / "Counter.tla", str(state), *predicates,
        )

    def test_rejects_unsupported_trace_before_starting_tlc(self):
        result = self.inspect("unsupported.json", 1, "BelowLimit")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported trace format", result.stderr)
        self.assertIn("-dumpTrace tla", result.stderr)

    def test_rejects_alternate_tla_trace_layout(self):
        with TemporaryDirectory() as directory:
            trace = Path(directory) / "Alternate.tla"
            trace.write_text(
                "---- MODULE Alternate ----\nCounterExample == [state |-> {<<1, 0>>}]\n====\n",
                encoding="utf-8",
            )
            result = self.inspect(trace, 1, "BelowLimit")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported trace format", result.stderr)

    @unittest.skipUnless(JAR, "set TLA_TOOLS_JAR for TLC integration tests")
    def test_evaluates_supplied_predicates_on_selected_state(self):
        for index, x, truth in ((2, 1, "TRUE"), (3, 2, "FALSE")):
            with self.subTest(index=index):
                result = self.inspect("Witness.tla", index, "BelowLimit", "CanIncrement")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"State {index}", result.stdout)
                self.assertIn(f"x |-> {x}", result.stdout)
                self.assertIn(f"BelowLimit |-> {truth}", result.stdout)
                self.assertIn(f"CanIncrement |-> {truth}", result.stdout)

    @unittest.skipUnless(JAR, "set TLA_TOOLS_JAR for TLC integration tests")
    def test_reports_absent_state(self):
        result = self.inspect("Witness.tla", 4, "BelowLimit")
        self.assertEqual(result.returncode, 2)
        self.assertIn("state 4 is absent or ambiguous", result.stderr)

    @unittest.skipUnless(JAR, "set TLA_TOOLS_JAR for TLC integration tests")
    def test_preserves_tlc_model_values_in_multi_variable_state(self):
        result = run_script(
            "inspect_tlc_state.py", "--jar", JAR, "--variables", "holding,active",
            "--model-values", "a,b", "--constants", WITNESS / "atom-constants.cfg",
            WITNESS / "AtomWitness.tla", WITNESS / "Atoms.tla", "2", "IsNode", "IsInitial",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("active |-> TRUE", result.stdout)
        self.assertRegex(result.stdout, r"holding \|-> [ab]")
        self.assertIn("IsNode |-> TRUE", result.stdout)
        self.assertIn("IsInitial |-> FALSE", result.stdout)

    @unittest.skipUnless(JAR, "set TLA_TOOLS_JAR for TLC integration tests")
    def test_accepts_a_path_in_tlcs_trace_header_and_digit_leading_identifiers(self):
        with TemporaryDirectory() as directory:
            model = Path(directory) / "Counter.tla"
            trace = Path(directory) / "Witness.tla"
            constants = Path(directory) / "constants.cfg"
            model.write_text(
                re.sub(r"\bx\b", "1x", (WITNESS / model.name).read_text())
                .replace("BelowLimit", "1BelowLimit"),
                encoding="utf-8",
            )
            trace.write_text(
                (WITNESS / trace.name).read_text().replace("MODULE Witness", "MODULE traces/Witness")
                .replace("[x |->", "[1x |->"),
                encoding="utf-8",
            )
            constants.write_text(
                '(* In the witness run: (* INIT and NEXT were separate. *) *)\nCONSTANT Limit = 2\n',
                encoding="utf-8",
            )
            result = run_script(
                "inspect_tlc_state.py", "--jar", JAR, "--variables", "1x", "--constants",
                constants, trace, model, "2", "1BelowLimit",
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1x |-> 1", result.stdout)
        self.assertIn("1BelowLimit |-> TRUE", result.stdout)


if __name__ == "__main__":
    unittest.main()
