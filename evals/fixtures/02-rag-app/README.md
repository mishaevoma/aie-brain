# handbook-qa

Answers staff questions from the company handbook in Slack.

The handbook is about 1,100 pages of Markdown (roughly 1.4 million tokens), exported nightly into `docs/`. This repository keeps a small sample of it for development.

## Run

```sh
pip install anthropic voyageai
python3 ingest.py                  # builds index.json from docs/
python3 qa.py "How long do I have to file an expense claim?"
```

## How it works

1. `ingest.py` cuts every Markdown file under `docs/` into 400-character chunks and stores one embedding per chunk.
2. `qa.py` embeds the question, takes the 25 closest chunks and sends them to the model with the conversation so far.

## Tests

```sh
python3 -m unittest -v
```

## Known problems

People in #ask-handbook say it gets expense questions wrong more often than leave questions, and that it sometimes cannot find a form by its number (for example EXP-204). `data/asked.csv` has the questions from the first two weeks, with the file that holds the right answer, as noted by the People team.
