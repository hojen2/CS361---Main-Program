import time

# Top level list to store habits
habits = []

def main_menu():
    while True:
        print('\nHabit Tracker Main Menu')
        print('=' * 72)
        print('A simple command-line habit tracker to keep you on track of your goals.')
        print('=' * 72)
        print('1. Manage Habits')
        print('2. Track Activities')
        print('3. View Progress')
        print('4. Data Management')
        print('5. Exit Program')

        choice = input('\nSelect an option (1-5): ')

        if choice == '1':
            manage_habits_menu()
        else:
            print('\nInvalid choice. Please enter a number between 1 and 5.\n')

def manage_habits_menu():
    while True:
        print('\nManage Habits')
        print('=' * 72)
        print('1. Add Habit')
        print('2. Edit Habit')
        print('3. Delete Habit')
        print('4. View All Habits and Goals')
        print('5. Exit to Main Menu')

        choice = input('\nSelect an option: ')

        if choice == '1':
            add_habit()
        elif choice == '2':
            edit_habit()
        elif choice == '3':
            delete_habit()
        elif choice == '4':
            view_habit()
        elif choice == '5':
            print('\nReturning to Main Menu...')
            time.sleep(1.5) # Adds a delay os 1.5 seconds to give the effect of a loading screen
        else:
            print('\nInvalid choice. Please enter a number between 1 and 5.\n')

def add_habit():
    print('\nAdd New Habit')
    print('=' * 72)

    # Get habit name
    name = input('Enter habit name: ').strip().lower() # .strip removes whitespace and .lower removes uppercase

    # Get goal timeframe (daily/weekly/monthly)
    while True:
        period = input('Enter the period (day/week/month): ').strip().lower()
        if period not in ['day', 'week', 'month']:
            print('** Please enter "day", "week", or "month". **')
        else:
            break

    # Get goal frequency per period (must be positive integer).
    while True:
        try:
            frequency = int(input('Enter frequency: ').strip())
            if frequency < 1:
                print('** Please enter a positive number. **')
                continue
            break
        except ValueError:
            print('** Please enter a valid number. **')

    # Get category
    category = input('Enter category: ').strip().lower()

    # Finally, stores habit as a dictionary
    habit = {
        'name': name,
        'period': period,
        'frequency': frequency,
        'category': category
    }

    habits.append(habit) # Add habit to list

    # Display confirmation prompt
    print(f'\n"{name.capitalize()}" added successfully [{frequency}x per {period} in category "{category.capitalize()}"]!')
    
    choice = input('\nPress "A" to add another habit or Enter to return to Manage Habits menu: ').strip().lower()
    if choice == 'a':
        add_habit()
    else:
        print('\nReturning to Manage Habits menu...')
        time.sleep(1.5)
        return

def edit_habit():
    if not habits:
        print('\nNo habits to edit.\n')
        input('\nPress Enter to return to Manage Habits menu...')
        return

    while True:
        print('\nEdit Habit')
        print("=" * 72)

        # Gives the user two ways to select habit
        print('\nChoose one of the following options to edit a habit:')
        print('1. Select habit from entire list.')
        print('2. Search habit by keyword.')

        while True:
            selection_choice = input('Choose an option (or press Enter to return to Manage Habits menu): ').strip()

            # Exit if user presses Enter
            if selection_choice == '':
                print('\nReturning to Manage Habits menu...')
                time.sleep(1.5)
                return

            if selection_choice in ['1', '2', '3']:
                break
            else:
                print('** Please enter 1, 2, or 3. **')

        # Filter habits based on selection
        if selection_choice == '2':
            while True:
                keyword = input('Enter keyword to search: ').strip().lower()
                filtered_habits = [h for h in habits if keyword in h['name'].lower()]  # list comprehension
                if filtered_habits:
                    break
                else:
                    print('\nNo habits found matching that keyword.')
                    try_again = input('Would you like to try another keyword? (Y to retry / Enter to return): ').strip().lower()
                    if try_again != 'y':
                        print('\nReturning to Manage Habits menu...')
                        time.sleep(1.5)
                        return
        else:
            filtered_habits = habits  # no filter/keyword search applies so this option shows all habits


        # Show list of habits (just names) using enumeration
        print('\nAvailable Habits:')
        for i, habit in enumerate(filtered_habits, start=1): # change index to start at 1 for readability
            print(f'{i}. {habit['name'].capitalize()}')

        # Select a habit
        while True:
            try:
                num_choice = int(input('\nEnter the number of the habit to edit: ').strip())
                if 1 <= num_choice <= len(filtered_habits):
                    habit_to_edit = filtered_habits[num_choice - 1]
                    break
                else:
                    print(f'** Please enter a number between 1 and {len(filtered_habits)}. **')
            except ValueError:
                print('** Please enter a valid number. **')

        # Display habit details after selection
        print('\nCurrent Habit Details:\n')
        print(f'Name: {habit_to_edit["name"].capitalize()}')
        print(f'Goal: {habit_to_edit["frequency"]}x per {habit_to_edit['period']}')
        print(f'Category: {habit_to_edit["category"].capitalize()}')
        print('-' * 72)
        print('\nPress Enter to keep a field unchanged.\n')

        # Edit habit name
        temp_name = input(f'Enter new name: ').strip() or habit_to_edit['name'] # keeps old name if user presses Enter

        # Edit habit frequency
        temp_freq = habit_to_edit['frequency']  # initialized to current value
        while True:
            user_input = input(f'Enter new frequency: ').strip()
            if not user_input:  # user pressed Enter, keep old value
                break
            try:
                user_input = int(user_input)
                if user_input < 1:
                    print('** Please enter a positive number. **')
                    continue
                temp_freq = user_input  # update only if valid
                break
            except ValueError:
                print('** Please enter a valid number. **')

        # Edit habit timeframe
        temp_period = habit_to_edit['period']  # start with current value
        while True:
            user_input = input(f'Enter new time period (day/week/month): ').strip().lower()
            if not user_input:  # user pressed Enter, keep old value
                break
            if user_input in ['day', 'week', 'month']:
                temp_period = user_input  # update only if valid
                break
            else:
                print('** Please enter "day", "week", or "month". **')

        # Edit habit category
        temp_category = input(f'Enter new category: ').strip()

        # Ask user to confirm changes
        while True:
            confirm = input('\nConfirm changes? (Y/N): ').strip().lower()
            if confirm == 'y':
                habit_to_edit['name'] = temp_name
                habit_to_edit['frequency'] = temp_freq
                habit_to_edit['period'] = temp_period
                # Only update category if user typed something
                if temp_category:
                    habit_to_edit['category'] = temp_category
                print('\nChanges saved successfully!')

                # Print updated habit details
                print('\nUpdated Habit Details:\n')
                print(f'Name: {habit_to_edit["name"].capitalize()}')
                print(f'Goal: {habit_to_edit["frequency"]}x per {habit_to_edit["period"]}')
                print(f'Category: {habit_to_edit["category"].capitalize()}')
                print('-' * 72)

                break
            elif confirm == 'n':
                print('\nChanges canceled. No updates made.')
                break
            else:
                print('** Please enter "Y" or "N". **')

        # After saving or discarding, ask if user wants to edit another or return to Manage Habits menu
        while True:
            next_action = input('\nWould you like to edit another habit? (Y to continue / Enter to return to Manage Habits): ').strip().lower()
            if next_action == 'y':
                break  # goes back to the top of the while loop to edit another
            elif next_action == '':
                print('\nReturning to Manage Habits menu...')
                time.sleep(1.5)
                return  # exits edit_habit() and returns to Manage Habits
            else:
                print('** Please enter Y or press Enter. **')

def delete_habit():
    if not habits:
        print('\nNo habits to delete.\n')
        input('\nPress Enter to return to Manage Habits menu...')
        return

    while True:
        print('\nDelete Habit')
        print("=" * 72)

        # Like edit function, gives user 2 ways to select habit to delete
        print('\nChoose one of the following options to delete a habit:')
        print('1. Select habit from entire list.')
        print('2. Search habit by keyword.')

        while True:
            selection_choice = input('Choose an option (or press Enter to return to Manage habits Menu): ').strip()

            # Exit if user presses Enter
            if selection_choice == '':
                print('\nReturning to Manage Habits menu...')
                time.sleep(1.5)
                return

            if selection_choice in ['1', '2']:
                break
            else:
                print('** Please enter 1 or 2. **')

        # Filter habits based on selection
        if selection_choice == '2':
            while True:
                keyword = input('Enter keyword to search: ').strip().lower()
                filtered_habits = [h for h in habits if keyword in h["name"].lower()]
                if filtered_habits:
                    break
                else:
                    print('\nNo habits found matching that keyword.')
                    try_again = input(
                        'Would you like to try another keyword? (Y to retry / Enter to return): ').strip().lower()
                    if try_again == 'y':
                        continue
                    elif try_again == '':
                        print('\nReturning to Manage Habits menu...')
                        time.sleep(1.5)
                        return

        else:
            filtered_habits = habits

        # Show list of habits
        print('\nAvailable Habits:')
        for i, habit in enumerate(filtered_habits, start=1):
            print(f'{i}. {habit["name"].capitalize()}')

        # Select a habit to delete
        while True:
            try:
                num_choice = int(input('\nEnter the number of the habit to delete: ').strip())
                if 1 <= num_choice <= len(filtered_habits):
                    habit_to_delete = filtered_habits[num_choice - 1]
                    break
                else:
                    print(f'** Please enter a number between 1 and {len(filtered_habits)}. **')
            except ValueError:
                print('** Please enter a valid number. **')

        # Confirm deletion
        print('\nHabit selected for deletion:')
        print(f'Name: {habit_to_delete["name"].capitalize()}')
        print(f'Goal: {habit_to_delete["frequency"]}x per {habit_to_delete["period"]}')
        print(f'Category: {habit_to_delete["category"].strip().capitalize() if habit_to_delete["category"].strip() else "N/A"}')
        print('-' * 72)

        confirm = input(
            'Are you sure you want to delete this habit? This action cannot be undone. (Y/N): ').strip().lower()
        if confirm == 'y':
            habits.remove(habit_to_delete)
            print(f'\n"{habit_to_delete["name"].capitalize()}" has been deleted successfully>')
        elif confirm == 'n':
            print('\nDeletion cancelled.')
            continue
        else:
            print('** Please enter "Y" or "N". **')

        # Option to delete another habit
        again = input('\nPress "D" to delete another habit or Enter to return to Manage Habits menu: ').strip().lower()
        if again == 'd':
            continue
        else:
            print('\nReturning to Manage Habits menu...')
            time.sleep(1.5)
            return

def view_habit():
    try:
        if not habits:
            print('\nNo habits to view.\n')
            input('\nPress Enter to return to Manage Habits menu...')
            return

        while True:
            print('\nView Habits')
            print('=' * 72)

            # Offers user three ways to view habits
            print('\nChoose one of the following options:')
            print('1. View all habits.')
            print('2. Search habits by keyword.')
            print('3. View habits by category.')

            while True:
                selection_choice = input('Choose an option (or press Enter to return to Manage Habits menu): ').strip()

                # Exit if user presses Enter
                if selection_choice == '':
                    print('\nReturning to Manage Habits menu...')
                    time.sleep(1.5)
                    return

                if selection_choice in ['1', '2', '3']:
                    break
                else:
                    print('** Please enter 1, 2, or 3. **')

            # Option 1: View all habits
            if selection_choice == '1':
                print('\nAll Habits:')
                print('-' * 72)
                for habit in habits:
                    print(f'Name: {habit["name"].capitalize()}')
                    print(f'Goal: {habit["frequency"]}x per {habit["period"]}')
                    print(f'Category: {habit["category"].capitalize()}')
                    print('-' * 72)
                input('\nPress Enter to return...')

            # Option 2: Search habits by keyword
            elif selection_choice == '2':
                while True:
                    keyword = input('Enter keyword to search: ').strip().lower()
                    filtered_habits = [h for h in habits if keyword in h['name'].lower()]
                    if filtered_habits:
                        print('\nMatching Habits:')
                        print('-' * 72)
                        for habit in filtered_habits:
                            print(f'Name: {habit["name"].capitalize()}')
                            print(f'Goal: {habit["frequency"]}x per {habit["period"]}')
                            print(f'Category: {habit["category"].capitalize()}')
                            print('-' * 72)
                        input('\nPress Enter to return...')
                        break
                    else:
                        print('\nNo habits found matching that keyword.')
                        try_again = input(
                            'Would you like to try another keyword? (Y to retry / Enter to return): ').strip().lower()
                        if try_again != 'y':
                            print('\nReturning to View Habits menu...')
                            time.sleep(1.5)
                            break

            # Option 3: View habits by category
            elif selection_choice == '3':
                while True:  # loop for category menu
                    print('\nView by Category')
                    print("=" * 72)
                    print('\nChoose one of the following options:')
                    print('1. View all categories.')
                    print('2. View habits from a chosen category.')

                    category_choice = input('Choose an option (or press Enter to return to previous menu): ').strip()

                    # Press Enter returns to previous menu
                    if category_choice == '':
                        print('\nReturning to View Habits menu...')
                        time.sleep(1.5)
                        break

                    # Validate input
                    if category_choice not in ['1', '2']:
                        print('** Please enter 1 or 2, or press Enter to return. **')
                        continue

                    # Sub-option 1: View all unique categories
                    if category_choice == '1':
                        # avoid blank placeholder categories
                        unique_categories = sorted(
                            set(h['category'].strip().title() for h in habits if h['category'].strip())
                        )

                        if not unique_categories:
                            print('\nNo categories available.')
                        else:
                            print('\nCategories:')
                            print('-' * 72)
                            for cat in unique_categories:
                                print(f'- {cat}')
                            print('-' * 72)

                        input('\nPress Enter to return...')

                    # Sub-option 2: View habits in a chosen category
                    elif category_choice == '2':
                        category_name = input('Enter category name: ').strip().lower()
                        if not category_name:  # Empty input returns to category menu
                            print('\nReturning to Category menu...')
                            continue

                        filtered_by_category = [
                            h for h in habits if h['category'].strip().lower() == category_name
                        ]

                        if filtered_by_category:
                            print(f'\nHabits in "{category_name.title()}" category:')
                            print('-' * 72)
                            for habit in filtered_by_category:
                                print(f'Name: {habit["name"].title()}')
                                print(f'Goal: {habit["frequency"]}x per {habit["period"]}')
                                print(f'Category: {habit["category"].title()}')
                                print('-' * 72)
                            input('\nPress Enter to return...')
                        else:
                            print(f'\nNo habits found in "{category_name.title()}" category.')
                            try_again = input(
                                'Would you like to try another category? (Y to retry / press Enter to return): '
                            ).strip().lower()
                            if try_again != 'y':
                                print('\nReturning to View Habits menu...')
                                time.sleep(1)
                                break


    except KeyboardInterrupt:
        print('\n\nReturning to Manage Habits menu...')
        time.sleep(1.5)
        return

if __name__ == "__main__":
    main_menu()