import unittest
from seat_selection import default_selection


class TestSeatSelection(unittest.TestCase):
    def test_seat_selection_remaining_tickets(self):
        row = ['*' for _ in range(10)]
        tickets = 12
        row, remaining = default_selection(row, tickets)
        self.assertEqual(2, remaining)

    def test_seat_selection_remaining_tickets_with_already_booked_seats(self):
        row = ['*' for _ in range(10)]
        row[0] = '#'
        row[1] = '#'
        tickets = 8
        row, remaining = default_selection(row, tickets)
        self.assertEqual(0, remaining)

    def test_seat_selection_book_status(self):
        row = ['*' for _ in range(10)]
        tickets = 12
        row, remaining = default_selection(row, tickets)
        self.assertEqual(10, sum([1 for v in row if v == 'o']))

    def test_seat_selection_book_status_with_already_booked_seats(self):
        row = ['*' for _ in range(10)]
        row[0] = '#'
        row[1] = '#'
        tickets = 8
        row, remaining = default_selection(row, tickets)
        self.assertEqual(8, sum([1 for v in row if v == 'o']))


if __name__ == '__main__':
    unittest.main()
