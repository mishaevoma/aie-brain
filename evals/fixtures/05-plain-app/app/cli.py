"""Command line for the helpdesk."""
import argparse

from app import db, tagging


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="ticketdesk")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("text")
    add.add_argument("--from", dest="sender", required=True)
    listing = commands.add_parser("list")
    listing.add_argument("--category", choices=tagging.CATEGORIES)
    close = commands.add_parser("close")
    close.add_argument("ticket_id", type=int)
    args = parser.parse_args(argv)

    connection = db.connect()
    if args.command == "add":
        category = tagging.tag_ticket(args.text)
        print(f"#{db.add(connection, args.sender, args.text, category)} [{category}]")
    elif args.command == "list":
        for row in db.list_open(connection, args.category):
            print(f"#{row['id']} [{row['category']}] {row['sender']}: {row['text']}")
    else:
        db.close(connection, args.ticket_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
