import unittest

from app import db


class TicketStoreTest(unittest.TestCase):
    def setUp(self):
        self.connection = db.connect(":memory:")

    def test_added_ticket_is_listed(self):
        ticket_id = db.add(self.connection, "dana@example.com", "charged twice", "billing")
        rows = db.list_open(self.connection)
        self.assertEqual([row["id"] for row in rows], [ticket_id])

    def test_list_filters_by_category(self):
        db.add(self.connection, "a@example.com", "charged twice", "billing")
        db.add(self.connection, "b@example.com", "page crashes", "bug")
        self.assertEqual(len(db.list_open(self.connection, "bug")), 1)

    def test_closed_ticket_is_not_listed(self):
        ticket_id = db.add(self.connection, "a@example.com", "charged twice", "billing")
        db.close(self.connection, ticket_id)
        self.assertEqual(db.list_open(self.connection), [])


if __name__ == "__main__":
    unittest.main()
