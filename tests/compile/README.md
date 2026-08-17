# Compile Golden Test Suite

Status: **candidate test definition, not executed compiler evidence**.

This directory defines semantic golden cases for the compile service. Until issue #5 produces an executable compile path, these fixtures specify expected behavior rather than prove it.

Golden dimensions:

- manifest ordering;
- include/exclude precedence;
- title and heading behavior;
- scene and section breaks;
- front/back matter;
- footnotes and citations;
- comments excluded by default;
- missing assets and unsupported syntax warnings;
- source-map coverage;
- repeated compile from identical frozen inputs.

See `golden-cases.yaml`.
