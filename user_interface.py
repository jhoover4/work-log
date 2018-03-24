import os
from datetime import datetime

from entry import Entry
from database import Search


class InterfaceHelpers:

    def __init__(self, database):
        self.database = database

    @staticmethod
    def clear():
        """Clears screen for user."""

        os.system('cls' if os.name == 'nt' else 'clear')

    def input_date(self, msg):
        self.clear()
        task_date = input(msg)

        while not Entry.date_check(task_date):
            self.clear()
            err_msg = "ERROR: {} isn't a valid date.\n\n".format(task_date)

            task_date = input(err_msg + msg)

        return task_date

    def input_time(self, msg):
        self.clear()
        time_spent = input(msg)

        while not Entry.time_check(time_spent):
            self.clear()
            err_msg = "ERROR: {} isn't a valid number of minutes.\n\n".format(time_spent)

            time_spent = input(err_msg + msg)

        return time_spent

    def input_employee(self, msg):
        employee_input = input(msg)

        while not employee_input.isalpha():
            self.clear()
            err_msg = "ERROR: {} isn't a valid name.\n\n".format(employee_input)

            employee_input = input(err_msg + msg)

        return employee_input

    def input_text(self, msg):
        self.clear()
        notes = input(msg)

        return notes

    def add_task(self):
        """For adding new tasks to the csv file.
        Must have a date, title, time spent, and optional body text.
        """

        task_date = self.input_date("Date of the task (Please use DD/MM/YYYY): \n")
        task_title = self.input_text("Title of the task: \n")
        time_spent = self.input_time("Time spent (integer of rounded minutes): \n")
        notes = self.input_text("Notes (Optional, you can leave this empty): \n")

        new_entry = Entry(task_date, task_title, time_spent, notes)
        self.database.add_entries([new_entry])

        self.clear()
        input("The task has been added! Press any key to return to the menu\n")

    def search_task(self):
        """For searching tasks from the csv file.
        Must have a date, title, time spent, and optional body text"""

        search_ui_input = ['a', 'b', 'c', 'd', 'e', 'q']

        while True:
            self.clear()

            prompt = "Do you want to search by:\n\n"
            prompt += "a) Exact Date\n"
            prompt += "b) Range of Dates\n"
            prompt += "c) Exact Search\n"
            prompt += "d) Regex Pattern\n"
            prompt += "e) Return to Menu\n\n"
            prompt += "> "

            user_input = str(input(prompt)).strip()

            while user_input not in search_ui_input:
                self.clear()

                print(prompt)
                user_input = str(input("Please enter valid input\n")).strip()

            search_csv = Search()

            if user_input.lower() == "e":
                break

            self.clear()

            if user_input.lower() == "a":
                task_date = input("Date of the task (Please use DD/MM/YYYY):\n")

                while not Entry.date_check(task_date):
                    self.clear()
                    print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))
                    task_date = input("Date of the task (Please use DD/MM/YYYY):\n")

                entries = search_csv.exact_date(task_date)

            if user_input.lower() == "b":
                start_date = input("Start date in range (Please use DD/MM/YYYY):\n")
                end_date = input("End date in range (Please use DD/MM/YYYY):\n")

                while not Entry.date_check(start_date) or not Entry.date_check(end_date):
                    self.clear()
                    print("Error: {} doesn't seem to be a valid date.\n\n".format(task_date))

                    print("Start date in range:\n")
                    start_date = input("Please use DD/MM/YYYY: \n")

                    print("End date in range:\n")
                    end_date = input("Please use DD/MM/YYYY: \n")

                entries = search_csv.range_of_dates(start_date, end_date)

            if user_input.lower() == "c":
                task_title = input("Search by task title or notes: \n")

                entries = search_csv.exact_search(task_title)

            if user_input.lower() == "d":
                pattern = input("Search by task title or notes with a regex pattern (case sensitive): \n")

                entries = search_csv.regex_pattern(pattern)

            if not entries:
                print("No entries available\n\n")
            else:
                if len(entries) > 1:
                    self.search_returned_entries(entries)
                else:
                    self.entry_pagination(entries)

    def entry_pagination(self, entries):
        """Pages through returned entries for user"""

        # sort by oldest date to newest date
        entries.sort(key=lambda entry: datetime.strptime(entry.date, '%m/%d/%Y'))

        user_input = ''
        i = 0
        query_len = len(entries)

        while user_input.lower() != 'q' and i <= query_len - 1:
            self.clear()
            valid_input = ['q', 'e', 'd']

            if query_len == 1:
                prompt = "One task returned. Press (q) to return to menu, (d) to delete, or (e) to edit.\n\n"
            else:
                prompt = "Page through returned tasks. Press (q) to return to menu, (d) to delete, or (e) to edit.\n\n"

            prompt += entries[i].display_entry() + "\n"

            if i != 0 and query_len != 1:
                prompt += "(p)revious\n"
                valid_input.append('p')
            if i != query_len - 1 and query_len != 1:
                prompt += "(n)ext\n"
                valid_input.append('n')

            user_input = input(prompt + ">")

            while user_input.lower() not in valid_input:
                self.clear()
                user_input = input(prompt + "Please enter valid input\n>")

            if user_input.lower() == 'p':
                i -= 1
            elif user_input.lower() == 'd':
                self.database.del_entry(entries[i])
            elif user_input.lower() == 'e':
                self.edit_task(entries[i])
            else:
                i += 1

    def edit_task(self, entry):
        """UI for user to edit a task."""

        user_input = ''

        while user_input.lower() != 'q':
            self.clear()

            valid_input = ['q', 'a', 'b', 'c', 'd', 'e']

            prompt = "What would you like to edit? Press (q) to return to tasks.\n\n"

            prompt += "a) Task Date: " + entry.date + "\n"
            prompt += "b) Title: " + entry.title + "\n"
            prompt += "c) Time Spent: " + str(entry.time_spent) + "\n"
            prompt += "d) Notes: " + entry.notes + "\n"
            prompt += "\n>"

            user_input = input(prompt)

            while user_input.lower() not in valid_input:
                self.clear()

                user_input = input(prompt + "Please enter valid input\n")

            old_title = entry.title
            if user_input == "a":
                entry.date = self.input_date("Update Task Date:\n>")
            if user_input == "b":
                entry.title = self.input_text("Update Title:\n>")
            if user_input == "c":
                entry.time_spent = self.input_time("Update Time Spent:\n>")
            if user_input == "d":
                entry.notes = self.input_text("Update Notes:\n>")

            self.database.edit_entry(entry, old_title)

    def date_search(self, entries):
        user_input = input("Please enter a date:\n> ")

        while not Entry.date_check(user_input):
            user_input = input("Please use MM/DD/YYYY: \n")

        entries_found = []

        for entry in entries:
            if entry.date == user_input:
                entries_found.append(entry)

        self.entry_pagination(entries_found)

    def search_returned_entries(self, selected_entries):
        """User UI to search a set of entries."""

        valid_input = ['a', 'b', 'c', 'q']

        prompt = "There are multiple returned entries. How would you like to search them?\n"
        prompt += "a) Search by date\n"
        prompt += "b) Page through entries\n"
        prompt += "c) Return to menu\n\n"
        prompt += "> "

        user_input = input(prompt)

        while user_input.lower() not in valid_input:
            print("Not a valid entry. Please choose an option or press 'q' to quit ")
            user_input = input("\n> ")

        if user_input.lower() == "c" or user_input.lower() == "q":
            return

        if user_input.lower() == "a":
            self.date_search(selected_entries)

        if user_input.lower() == "b":
            self.entry_pagination(selected_entries)
