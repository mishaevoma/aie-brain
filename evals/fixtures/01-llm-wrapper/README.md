# commitmsg

Writes a commit message for whatever is staged.

```sh
git add -p
python3 commitmsg.py            # prints a message
git commit -m "$(python3 commitmsg.py)"
```

Needs `ANTHROPIC_API_KEY` and `pip install anthropic`.

## How it works

One call: the staged diff goes to the model with the house rules for commit messages, and the reply is printed. No history, no tools.

## Changing the prompt

The prompt lives in `commitmsg.py`. Run the tests before you change it:

```sh
python3 -m unittest -v
```

Then try it on the diffs in `examples/`. Each `.diff` has the message I would have written next to it (`.msg`). I read the output and compare by eye.
