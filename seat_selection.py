def is_available(row, index):
    if row[index] == '*':
        row[index] = 'o'
        return True
    return False


def default_selection(row, tickets):
    ln = len(row)
    mid = ln // 2 - 1
    booked = 0
    mid_available = is_available(row, mid)
    if mid_available:
        booked += 1
    right = mid + 1
    left = mid - 1
    backward = True

    while booked != tickets:
        if backward:
            available = is_available(row, right) if right != ln else False
            right = right + 1
            backward = False
        else:
            available = is_available(row, left) if left != -1 else False
            left = left - 1
            backward = True

        if available:
            booked += 1

        if left < 0 and right > ln - 1:
            return row, tickets - booked

    return row, tickets - booked


def user_selection(row, tickets):
    booked = 0
    idx = 0
    while tickets != booked:
        if idx == len(row):
            return row, tickets - booked

        if row[idx] == '*':
            row[idx] = 'o'
            booked += 1
        idx += 1

    return row, tickets - booked
