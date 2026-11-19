# slugkit

Turns titles into URL slugs. Pure Python, no dependencies.

```python
from slugkit import slugify

slugify("Crème brûlée, 2 ways!")        # "creme-brulee-2-ways"
slugify("Hello   World", separator="_") # "hello_world"
slugify("A very long title", max_length=10)  # "a-very"
```

## Develop

```sh
python3 -m unittest discover -s tests -v
```

CI runs the same command on every push.
