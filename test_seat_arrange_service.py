import unittest
from seat_arrange_service import get_available_seats, get_last_seat_arrange,validate_seat_position


class TestSeatSelection(unittest.TestCase):
    def test_available_ticket_count(self):
        rows = 8
        cols = 10
        seat_area = [['*' for _ in range(cols)] for _ in range(rows)]
        seat_area[0][0] = 'o'
        available_seats = get_available_seats(seat_area)
        self.assertEqual(79, available_seats)

    def test_last_seat_arrangement_with_empty_bookings(self):
        rows = 8
        cols = 10
        seat_area = [['*' for _ in range(cols)] for _ in range(rows)]
        last_seat_area = get_last_seat_arrange({}, '')
        self.assertEqual(seat_area, last_seat_area)

    def test_last_seat_arrangement_with_exiting_bookings(self):
        rows = 8
        cols = 10
        seat_area = [['*' for _ in range(cols)] for _ in range(rows)]
        confirmed_bookings = {
            'GC1': seat_area
        }
        last_seat_area = get_last_seat_arrange(confirmed_bookings, 'GC1')
        self.assertEqual(seat_area, last_seat_area)

    def test_seat_position_input(self):
        rs = validate_seat_position('B05')
        self.assertEqual(True, rs)


if __name__ == '__main__':
    unittest.main()
