# study-buddy

A terminal tutor for learning German that remembers you between sessions.

```sh
pip install anthropic
python3 buddy.py
```

## How memory works

After each reply, the model is asked what is worth remembering about the learner. Every line it returns is appended to `memory.jsonl` with the date. When a session starts, everything in `memory.jsonl` is put into the system prompt, so the tutor knows where you left off.

The conversation itself is not saved. Only the notes are.

## Tests

```sh
python3 -m unittest -v
```

## Known problems

- After four months `memory.jsonl` has about 1,900 lines. Sessions start slowly, and the tutor drills things I mastered long ago.
- It still tells me to prepare for the B1 exam. I passed it in March. Nothing ever removes a note.
- It never remembers what I am good at or what I asked to practise, so every session starts with my weak spots.
