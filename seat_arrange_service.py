import re

alphabet_map = {
    'A': '0', 'B': '1', 'C': '2', 'D': '3', 'E': '4', 'F': '5', 'G': '6', 'H': '7', 'I': '8',
    'J': '9', 'K': '10', 'L': '11', 'M': '12', 'N': '13', 'O': '14', 'P': '15', 'Q': '16', 'R': '17',
    'S': '18', 'T': '19', 'U': '20', 'V': '21', 'W': '22', 'X': '23', 'Y': '24', 'Z': '25'

}

alphabet_map_by_index = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I',
    9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
    18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'

}


def get_available_seats(seat_area):
    return sum(sl.count('*') for sl in seat_area)


def get_last_seat_arrange(confirmed_bookings, last_confirmed_booking_id):
    if confirmed_bookings:
        v = confirmed_bookings.get(last_confirmed_booking_id)
        return v

    rows = 8  # max 26
    cols = 10  # max 50
    seat_area = [['*' for _ in range(cols)] for _ in range(rows)]

    return seat_area


def get_seated_area(seat_area):
    new_seat_area = [['#' if seat_area[k][v] == 'o' else seat_area[k][v] for v in range(len(seat_area[0]))] for k in
                     range(len(seat_area))]

    ln = len(new_seat_area)
    i = ln - 1
    while i >= 0:
        rw = new_seat_area[i]
        for idx, col in enumerate(rw):
            if col == 'o':
                rw[idx] = '#'
            else:
                rw[idx] = col
        i -= 1

    return new_seat_area


def display_seat_area(seat_area):
    cols = seat_area[0]
    ln = len(seat_area)
    i = ln - 1
    # if cols gt 9 allocate additional space to two digits numbers
    line_len = len(cols) * 2 + 2 if len(cols) < 10 else ((len(cols) - 9) * 3) + 2 + 9 * 2
    total_pad = line_len - 12  # 12 deduct for s c r e e n word
    pl = total_pad // 2
    pr = total_pad - pl

    area = ''.join([' ' for _ in range(pl)]) + 'S C R E E N' + ''.join([' ' for _ in range(pr)]) + '\n'
    area += ''.join(['-' for _ in range(pl)]) + '-----------' + ''.join(['-' for _ in range(pr)]) + '\n'
    while i >= 0:
        row = seat_area[i]
        row_title = alphabet_map_by_index.get(i)
        area += f'{row_title} '
        for k, col in enumerate(row):
            area += f' {col}' if k < 10 else f'  {col}'
        area += '\n'
        i -= 1
    area += '   '
    area += ' '.join([str(index + 1) for index in range(len(cols))])

    print(area)


def validate_seat_position(seat_position):
    regex_patten = '^[A-Z][0-9]{2}$'
    if seat_position == '' or re.match(regex_patten, seat_position):
        return True

    return False
