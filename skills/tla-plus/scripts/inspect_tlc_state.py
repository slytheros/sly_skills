#!/usr/bin/env python3
"""Evaluate model predicates on a saved TLC counterexample state."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from uuid import uuid4


IDENTIFIER = r"[0-9_]*[A-Za-z][A-Za-z0-9_]*"
MODULE_HEADER = re.compile(r"(?m)^[ \t]*-{4,}[ \t]+MODULE[ \t]+[^\r\n]+?[ \t]+-{4,}[ \t]*$")
TRACE_DEFINITION = re.compile(r"(?m)^[ \t]*CounterExample[ \t]*==\s*\[")
STATE_FIELD = re.compile(rf"\bstate\s*\|->\s*\{{\s*(?:\}}|<<\s*[0-9]+\s*,\s*\[\s*{IDENTIFIER}\s*\|->)")
CONFIG_TOKENS = re.compile(r'\(\*|\\\*[^\n]*|"(?:[^"\\\n]|\\.)*"|(' + IDENTIFIER + ")")
BLOCK_TOKENS = re.compile(r"\(\*|\*\)")
NON_CONSTANT_CONFIG = {
    "INIT", "NEXT", "SPECIFICATION", "INVARIANT", "INVARIANTS", "PROPERTY",
    "PROPERTIES", "CONSTRAINT", "CONSTRAINTS", "ACTION_CONSTRAINT",
    "ACTION_CONSTRAINTS", "SYMMETRY", "VIEW", "ALIAS", "CHECK_DEADLOCK",
    "POSTCONDITION", "POSTCONDITIONS", "_PERIODIC", "_RL_REWARD", "_POSSIBLE",
}


def read_trace(path):
    message = (
        "unsupported trace format: expected a TLC -dumpTrace tla module "
        "with a CounterExample.state record"
    )
    if path.suffix != ".tla":
        raise ValueError(message)
    try:
        trace = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(message) from exc
    if not MODULE_HEADER.search(trace) or not TRACE_DEFINITION.search(trace) or not STATE_FIELD.search(trace):
        raise ValueError(message)
    return trace


def read_constants(path):
    if not path:
        return ""
    config = path.read_text(encoding="utf-8")
    identifiers = []
    position = depth = 0
    while token := (BLOCK_TOKENS if depth else CONFIG_TOKENS).search(config, position):
        position = token.end()
        if token[0] == "(*":
            depth += 1
        elif token[0] == "*)":
            depth -= 1
        elif token[1]:
            identifiers.append(token[1])
    if (depth or (identifiers and identifiers[0] not in {"CONSTANT", "CONSTANTS"})
            or NON_CONSTANT_CONFIG.intersection(identifiers)):
        raise ValueError("--constants expects TLC CONSTANT or CONSTANTS declarations only")
    return config


def write_probe(directory, args, trace, variables, model_values, constants):
    probe = "InspectWitness" + uuid4().hex
    witness = f"{probe}Trace"
    witness_declarations = probe_declarations = substitutions = ""
    if model_values:
        probe_atoms = [f"{probe}Atom{index}" for index in range(len(model_values))]
        atoms = list(zip(model_values, probe_atoms))
        witness_declarations = "\nCONSTANTS " + ", ".join(model_values)
        probe_declarations = "\nCONSTANTS " + ", ".join(probe_atoms)
        substitutions = " WITH " + ", ".join(f"{name} <- {atom}" for name, atom in atoms)
        constants += "".join(f"\nCONSTANT {atom} = {name}" for name, atom in atoms)

    variable_fields = ", ".join(f'"{name}"' for name in variables)
    bindings = "\n".join(f"  /\\ {name} = {probe}Selected.{name}" for name in variables)
    results = ",\n".join(f"    {name} |-> IF {name} THEN TRUE ELSE FALSE" for name in args.predicates)
    # A path in TLC's dump argument can appear verbatim in its generated header.
    staged_trace = MODULE_HEADER.sub(f"---- MODULE {witness} ----{witness_declarations}", trace, count=1)
    directory.joinpath(f"{witness}.tla").write_text(staged_trace, encoding="utf-8")
    directory.joinpath(f"{probe}.tla").write_text(
        f"""---- MODULE {probe} ----
EXTENDS {args.model.stem}{probe_declarations}
LOCAL {probe}TLC == INSTANCE TLC
LOCAL {probe}Sets == INSTANCE FiniteSets
LOCAL {probe}Witness == INSTANCE {witness}{substitutions}
{probe}Hits == {{pair \\in {probe}Witness!CounterExample.state : pair[1] = {args.state}}}
{probe}Selected ==
  IF {probe}Sets!Cardinality({probe}Hits) = 1
  THEN (CHOOSE pair \\in {probe}Hits : TRUE)[2]
  ELSE {probe}TLC!Assert(FALSE, "state {args.state} is absent or ambiguous")
{probe}Init ==
  /\\ {probe}TLC!Assert(DOMAIN {probe}Selected = {{{variable_fields}}},
              "state fields do not match the supplied variables")
{bindings}
{probe}Next == UNCHANGED <<{", ".join(variables)}>>
{probe}Results == {probe}TLC!PrintT(
  [state |-> {probe}Selected, results |-> [
{results}]])
====
""",
        encoding="utf-8",
    )
    directory.joinpath(f"{probe}.cfg").write_text(
        f"INIT {probe}Init\nNEXT {probe}Next\nINVARIANT {probe}Results\n{constants}\n",
        encoding="utf-8",
    )
    return probe


def inspect(args):
    trace = read_trace(args.trace)
    variables = [name.strip() for name in args.variables.split(",")]
    model_values = [name.strip() for name in args.model_values.split(",")] if args.model_values else []
    for names in (variables, args.predicates, model_values):
        if any(not re.fullmatch(IDENTIFIER, name) for name in names):
            raise ValueError("variables, predicates, and model values must be unqualified TLA+ identifiers")
        if len(set(names)) != len(names):
            raise ValueError("variable, predicate, and model value lists must each contain unique names")
    if args.state < 1:
        raise ValueError("state index must be positive and one-based")
    if args.model.suffix != ".tla" or not re.fullmatch(IDENTIFIER, args.model.stem):
        raise ValueError("model file must be a named .tla module")
    if not args.model.is_file():
        raise ValueError(f"model file does not exist: {args.model}")
    if not args.jar.is_file():
        raise ValueError(f"TLC jar does not exist: {args.jar}")

    constants = read_constants(args.constants)
    libraries = [args.model.resolve().parent, *(path.resolve() for path in args.library)]
    with TemporaryDirectory(prefix="tlc-witness-") as scratch:
        directory = Path(scratch)
        probe = write_probe(directory, args, trace, variables, model_values, constants)
        results = directory / "results.txt"
        run = subprocess.run(
            ["java", "-XX:+UseParallelGC", "-DTLA-Library=" + os.pathsep.join(map(str, libraries)),
             "-cp", str(args.jar.resolve()), "tlc2.TLC", "-workers", "1",
             "-userFile", str(results), probe],
            cwd=directory, capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        output = results.read_text(encoding="utf-8").strip() if results.is_file() else ""
        if run.returncode or not output:
            raise ValueError(f"TLC could not evaluate the selected state:\n{run.stdout}{run.stderr}".rstrip())
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True, help="path to a compatible tla2tools.jar")
    parser.add_argument("--variables", required=True, help="comma-separated model state variables")
    parser.add_argument("--model-values", help="comma-separated TLC model values occurring in the dump")
    parser.add_argument("--constants", type=Path, help="TLC cfg fragment with constant assignments")
    parser.add_argument("--library", type=Path, action="append", default=[], help="extra module directory")
    parser.add_argument("trace", type=Path, help="saved TLC -dumpTrace tla module")
    parser.add_argument("model", type=Path, help="model module defining the state and predicates")
    parser.add_argument("state", type=int, help="one-based trace state number")
    parser.add_argument("predicates", nargs="+", help="names of nullary Boolean state predicates")
    args = parser.parse_args()
    try:
        output = inspect(args)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"State {args.state}\n{output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
