# ticketdesk

A small helpdesk for a five-person support team. Tickets live in SQLite. Staff add, list, assign and close them from the command line.

```sh
python3 -m app.cli add "I was charged twice for March" --from dana@example.com
python3 -m app.cli list --category billing
python3 -m app.cli close 14
```

New tickets get a category automatically (`billing`, `bug`, `how-to` or `account`), so each one lands in the right person's list. That is the only place a language model is used; set `ANTHROPIC_API_KEY` and `pip install anthropic` for it.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

## Data

`data/labelled_tickets.csv` has 40 tickets from the old helpdesk with the category the support lead gave each one. It was exported during the migration.
