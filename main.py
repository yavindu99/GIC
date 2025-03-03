from seat_arrange_service import get_available_seats, alphabet_map, get_seated_area, display_seat_area, \
    get_last_seat_arrange, validate_seat_position
from seat_selection import default_selection, user_selection

# seat area defaults to rows - 8, cols - 10. To change this change seat_arrange_service.py line 26 & 27
# keep track of confirmed bookings within a session
confirmed_bookings = {}
last_confirmed_booking_id = None

print('Please enter movie title')
movie_title = input()
tickets = 0

print('Welcome to GIC Cinemas')


def start():
    last_seat_arrange = get_last_seat_arrange(confirmed_bookings, last_confirmed_booking_id)
    options = {
        '[1]': f'Book tickets for {movie_title} ({get_available_seats(last_seat_arrange)} seats available)',
        '[2]': 'Check bookings',
        '[3]': 'Exit'
    }

    # display above options
    for key, value in options.items():
        print(f'{key} {value}')

    print('Please enter your selection:')
    selection = input()

    if selection == '1':
        book_tickets()
    elif selection == '2':
        check_booking()
    elif selection == '3':
        logout()
    else:
        print("Invalid selection. Please choose 1, 2, or 3.")
        start()


def book_tickets():
    print("Enter number of tickets to book, or enter blank to go back to main menu:")
    global tickets
    # get number of tickets user wants
    tickets = input()

    if tickets == '':
        start()
    else:
        # get latest confirmed seat arrangement.
        # if no confirmed bookings previously done then initial seat arrangement will be retrieved.
        last_arrange = get_last_seat_arrange(confirmed_bookings, last_confirmed_booking_id)
        available_seats = get_available_seats(last_arrange)

        # check if seats are available to allocate for requested tickets
        while int(tickets) > available_seats:
            print(f'Sorry, there are only {available_seats} seats available')
            print('Enter number of tickets to book, or enter blank to go back to main menu:')

            tickets = input()
            if tickets == '':
                start()
                return

        # get copy of the latest seat arrangement.
        # confirmed seats are display in #
        seat_area = get_seated_area(last_arrange)

        # seat default selection logic
        remaining = int(tickets)
        index = 0
        while remaining > 0:
            row = seat_area[index]
            seat_area[index], remaining = default_selection(row, remaining)
            index += 1
        display_seat_area(seat_area)
        print('Enter blank to accept seat selection, or enter new seating position:')
        user_selected_seat = input()

        # validate user seat input. eg: B05 is valid. B5/b05/b5 invalid
        while not validate_seat_position(user_selected_seat):
            print('Enter blank to accept seat selection, or enter new seating position:')
            user_selected_seat = input()

        # user select seat logic
        while user_selected_seat != '':
            seat_area = get_last_seat_arrange(confirmed_bookings, last_confirmed_booking_id)
            selected_seat_row = user_selected_seat[0]
            selected_seat_column = user_selected_seat[1:]

            # convert user input to necessary data types
            # B05 -> B to 2(row no), 05 to 5(column no)
            start_row_index = int(alphabet_map[selected_seat_row])
            start_col_index = int(selected_seat_column) if int(selected_seat_column) >= 10 else int(
                selected_seat_column[1:])

            # divide all seats into two arrays in case needed to use default seat section as well
            seat_area_for_user_selection = [seat_area[start_row_index][start_col_index - 1:]] + seat_area[
                                                                                                start_row_index + 1:]
            seat_area_for_default_selection = seat_area[:start_row_index] + [
                seat_area[start_row_index][:start_col_index - 1]]

            remaining = int(tickets)
            available_seats_count = get_available_seats(seat_area)

            # user select seat logic
            index = 0
            while available_seats_count >= remaining:
                if index == len(seat_area_for_user_selection):
                    break
                row = seat_area_for_user_selection[index]
                seat_area_for_user_selection[index], remaining = user_selection(row, remaining)
                index += 1

            # default seat selection logic
            outer_index = 0
            while remaining > 0:
                if outer_index == len(seat_area_for_default_selection):
                    break
                row = seat_area_for_default_selection[outer_index]
                seat_area_for_default_selection[index], remaining = default_selection(row, remaining)
                outer_index += 1

            combined_split_array = seat_area_for_default_selection[-1] + seat_area_for_user_selection[0]
            seat_area = seat_area_for_default_selection[:-1] + [
                combined_split_array] + seat_area_for_user_selection[1:]

            # display seat area in console.
            # o - current selected seats, # - already confirmed seats, * - available seats
            display_seat_area(seat_area)

            # confirm current selected seats
            print('Enter blank to accept seat selection, or enter new seating position:')
            user_selected_seat = input()

            while not validate_seat_position(user_selected_seat):
                print('Enter blank to accept seat selection, or enter new seating position:')
                user_selected_seat = input()

        # add to confirmed bookings
        add_to_bookings(seat_area)


def add_to_bookings(seat_area):
    global last_confirmed_booking_id
    if not last_confirmed_booking_id:
        key = 'GIC1'
    else:
        key = last_confirmed_booking_id[:3] + str(int(last_confirmed_booking_id[3:]) + 1)

    confirmed_bookings[key] = seat_area
    last_confirmed_booking_id = key

    print(f'Successfully reserved {tickets} {movie_title} tickets')
    print(f'booking id: {key}')

    start()


def check_booking():
    print('Enter booking id, or enter blank to go back to main menu:')
    booking_id = input()

    if booking_id == '':
        start()
    else:
        while confirmed_bookings.get(booking_id) is None:
            print("No booking found for this ID. Enter blank to go back to main menu:")
            booking_id = input()
            if booking_id == '':
                start()
                return
        area = confirmed_bookings.get(booking_id)
        last_arrange = get_last_seat_arrange(confirmed_bookings, last_confirmed_booking_id)

        # display confirmed seats(#) and user's seats(o) in a booking
        for i, rows in enumerate(last_arrange):
            for j, v in enumerate(rows):
                if area[i][j] != 'o' and (v == 'o' or v == '#'):
                    area[i][j] = '#'

        print('Selected seats:')
        print(display_seat_area(area))

        start()


def logout():
    print("Thank you for using GIC Cinemas system. Bye!")


start()
