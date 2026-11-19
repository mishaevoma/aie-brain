# slugkit

A small library with one public function, `slugkit.slugify`. Python 3.10+, standard library only.

- Test: `python3 -m unittest discover -s tests -v`. CI runs exactly this.
- Every behaviour change needs a test in `tests/test_core.py` that fails without it.
- No dependencies. Do not add one without asking.
- `slugify` must stay pure: same input, same output, no I/O.
