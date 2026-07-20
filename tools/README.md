# Knowledge Base Support Tools

This directory contains small, repository-local support tools. It must not become a product
implementation or a second knowledge workflow.

## Validator

`validate_kb.py` uses only the Python standard library:

~~~sh
python tools/validate_kb.py
~~~

Pass `--strict` to make warnings fail. The future packaged `kb` tool may absorb this behavior;
until then this script is the exercised validation reference for the current manual workflow.
