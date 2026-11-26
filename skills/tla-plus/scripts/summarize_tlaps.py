#!/usr/bin/env python3
"""Summarize a saved TLAPM Toolbox log without running the prover."""

import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path
import re


PROVED = {"proved", "trivial"}
TIMEOUT_REASONS = {"timeout", "internal timeout"}
IDENTIFIER = r"[0-9_]*[A-Za-z][A-Za-z_0-9]*"
SUMMARY = re.compile(
    r"^\[(?:INFO|ERROR)\]: (?:All (\d+) obligations? proved|"
    r"(\d+)/(\d+) obligations? failed)\.$"
)
FILE_LOCATION = re.compile(r'^File "([^"]+)", line ')
LOCATION = re.compile(r"(\d+):(\d+):(\d+):(\d+)")
TIMING = re.compile(
    r"(?:; )?time-limit: \S+(?:; time-used: (\d+(?:\.\d+)?) \([^)]*\))?$"
)
DECLARATION = re.compile(
    r"(?m)^(?:[ \t]*(THEOREM|LEMMA|PROPOSITION|COROLLARY)\b"
    rf"(?:\s+({IDENTIFIER})\s*==)?"
    r"|(?:LOCAL|ASSUME|ASSUMPTION|AXIOM|USE|HIDE|INSTANCE|EXTENDS|"
    rf"VARIABLES?|CONSTANTS?|RECURSIVE)\b|{IDENTIFIER}[ \t]*"
    r"(?:\([^\n]*\)[ \t]*)?==|={4,})"
)
SOURCE_TOKENS = re.compile(r'\(\*|\*\)|\\\*[^\n]*|"(?:[^"\\\n]|\\.)*"')
BLOCK_TOKENS = re.compile(r"\(\*|\*\)")


def theorem_boundaries(source):
    """Keep source lines while removing comments and string literals."""
    chunks = []
    position = depth = 0
    while token := (BLOCK_TOKENS if depth else SOURCE_TOKENS).search(source, position):
        value = token.group()
        between = source[position:token.start()]
        chunks.append(re.sub(r"[^\n]", " ", between) if depth else between)
        if value == "(*":
            depth += 1
        elif value == "*)" and depth:
            depth -= 1
        chunks.append(" " * len(value))
        position = token.end()
    chunks.append(re.sub(r"[^\n]", " ", source[position:]) if depth else source[position:])
    cleaned = "".join(chunks)
    if depth or len(re.findall(r"(?m)^[ \t]*-{4,}[ \t]+MODULE\b", cleaned)) != 1:
        return []

    boundaries = []
    line, position = 1, 0
    for match in DECLARATION.finditer(cleaned):
        line += cleaned.count("\n", position, match.start())
        boundaries.append((line, match[2]))
        position = match.start()
    return boundaries


@dataclass
class Obligation:
    location: str | None = None
    proved: bool = False
    last_attempt: dict | None = None

    def record(self, fields):
        self.location = fields.get("loc", self.location)
        status = fields["status"]
        if status == "to be proved" or self.proved:
            return
        self.proved = status in PROVED
        method = fields.get("meth")
        timing = TIMING.search(method) if method else None
        self.last_attempt = {
            "status": status,
            "backend": fields.get("prover"),
            "method": (method[:timing.start()] or None) if timing else method,
            "reason": fields.get("reason"),
            "elapsed_seconds": float(timing[1]) if timing and timing[1] else None,
            "cached": {"true": True, "false": False}.get(fields.get("already")),
        }


@dataclass
class ProofLog:
    obligations: dict[int, Obligation] = field(default_factory=dict)
    expected: int | None = None
    totals: tuple[int, int] | None = None
    file: str | None = None
    partial: bool = False
    incomplete_proof: bool = False

    def record(self, fields):
        kind = fields.get("type")
        if kind == "obligation":
            identifier = fields.get("id", "")
            if not identifier.isascii() or not identifier.isdecimal() or not fields.get("status"):
                self.partial = True
                return
            self.obligations.setdefault(int(identifier), Obligation()).record(fields)
        elif kind == "obligationsnumber":
            count = fields.get("count", "")
            if self.expected is not None:
                raise ValueError("expected a log for one TLAPM module, found multiple obligation counts")
            if count.isascii() and count.isdecimal():
                self.expected = int(count)
            else:
                self.partial = True

    def read(self, lines):
        frame = None
        preceding_file = None
        for raw_line in lines:
            line = raw_line.rstrip("\r\n")
            if line == "@!!BEGIN":
                self.partial |= frame is not None
                frame = {}
            elif line == "@!!END":
                if frame is None:
                    self.partial = True
                else:
                    self.record(frame)
                frame = None
            elif frame is not None:
                key, separator, value = line[3:].partition(":")
                if line.startswith("@!!") and separator:
                    frame[key] = value
            elif match := SUMMARY.fullmatch(line):
                if self.totals is not None:
                    raise ValueError("expected a log for one TLAPM module, found multiple proof summaries")
                self.totals = (int(match[2] or 0), int(match[1] or match[3]))
                self.file = preceding_file
            elif match := FILE_LOCATION.match(line):
                preceding_file = match[1]
            elif line.startswith(("[ERROR]: Proof incomplete in module ",
                                  "[ERROR]: No proof obligation found for the selected target.")):
                self.incomplete_proof = True
        self.partial |= frame is not None

    def report(self, source, runner):
        boundaries = theorem_boundaries(source.read_text(encoding="utf-8")) if source else []
        location_file = self.file or (str(source) if source else None)
        unresolved = []
        for identifier, obligation in sorted(self.obligations.items()):
            if obligation.proved:
                continue
            location = {"file": location_file}
            theorem = None
            if match := LOCATION.fullmatch(obligation.location or ""):
                line, column, end_line, end_column = map(int, match.groups())
                location.update(line=line, column=column, end_line=end_line, end_column=end_column)
                for declaration_line, name in boundaries:
                    if declaration_line > line:
                        break
                    theorem = name
            unresolved.append({
                "id": identifier, "theorem": theorem, "location": location,
                "last_attempt": obligation.last_attempt,
            })

        final_failures = all(
            entry["last_attempt"] and entry["last_attempt"]["status"] == "failed"
            for entry in unresolved
        )
        if runner:
            status = runner["termination"]
        elif (self.partial or self.expected != len(self.obligations)
              or self.totals != (len(unresolved), self.expected) or not final_failures):
            status = "incomplete_log"
        elif unresolved:
            reasons = {entry["last_attempt"]["reason"] for entry in unresolved}
            status = "timeout" if reasons <= TIMEOUT_REASONS else "proof_failure"
        elif self.incomplete_proof:
            status = "incomplete_proof"
        else:
            status = "complete"
        return {
            "status": status, "expected_obligations": self.expected,
            "unresolved": unresolved, "runner": runner,
        }


def read_runner_status(path):
    record = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(record, dict)
            or record.get("termination") not in ("timeout", "memory_exhaustion")
            or not isinstance(record.get("evidence"), str)
            or not record["evidence"].strip()):
        raise ValueError("runner status requires termination (timeout or memory_exhaustion) and evidence")
    return {"termination": record["termination"], "evidence": record["evidence"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path, help="combined stdout and stderr from one Toolbox-mode run")
    parser.add_argument("--source", type=Path, help="matching TLA+ source for theorem names")
    parser.add_argument("--runner-status", type=Path, help="JSON sidecar with explicit runner evidence")
    args = parser.parse_args()
    try:
        proof = ProofLog()
        with args.log.open(encoding="utf-8") as log:
            proof.read(log)
        runner = read_runner_status(args.runner_status) if args.runner_status else None
        print(json.dumps(proof.report(args.source, runner), indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
