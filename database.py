import os
import re
import csv
from datetime import datetime

from entry import Entry


class Database:

    def __init__(self, database_name='work_entries'):
        self.database_name = database_name + '.csv'
        self.database_file_path = os.path.dirname(os.path.realpath(__file__)) + self.database_name

        self.entries = self.read_database()

    def create_database(self):
        """Creates csv if it doesn't already exist."""

        if not os.path.exists(self.database_file_path):
            open(self.database_name, 'a').close()

    def rewrite_database(self):
        """Creates completely new database"""

        with open(self.database_name, 'w') as f:

            fieldnames = self.entries[0].fields

            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            if len(self.entries) == 0:
                # if we only have one entry a different method needs to be used
                writer.writerow(self.entries.to_dict())
            else:
                entry_list = []

                for entry in self.entries:
                    entry_list.append(entry.to_dict())

                writer.writerows(entry_list)

    def read_database(self):
        """Opens up data to be worked with."""

        entries = []

        with open(self.database_name) as f:
            data = csv.DictReader(f)

            for row in data:
                entry_data = dict()

                entry_data['Date'] = row['Date']
                entry_data['Title'] = row['Title']
                entry_data['Time Spent'] = row['Time Spent']
                entry_data['Notes'] = row['Notes']

                entries.append(entry_data)

        return entries

    def add_entries(self, entries):
        """Takes a list of Entry objects"""

        with open(self.database_name, 'a') as f:

            fieldnames = entries[0].fields

            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if os.stat(self.database_name).st_size == 0:
                writer.writeheader()

            if len(entries) == 0:
                # if we only have one entry a different method needs to be used
                writer.writerow(entries.to_dict())
            else:
                entry_list = []

                for entry in entries:
                    entry_list.append(entry.to_dict())

                writer.writerows(entry_list)

    def del_entry(self, entry, title):
        """Takes one entry. Can take more if needed"""

        for entry in self.all_entries:
            if entry.title == title:
                del entry

        self.rewrite_database(self.all_entries)

    def edit_entry(self, entry, title):
        """Takes one entry. Can take more if needed"""

        for entry in self.all_entries:
            if entry.title == title:
                del entry

    def set_index(self):

        return len(self.all_entries)


class Search(Database):

    def __init__(self):
        super().__init__()

    def exact_date(self, date):
        """Finds entry from an exact date search and returns a list of matching objects."""

        entries_found = []

        for data in self.entries:
            if date in data['Date']:
                entries_found.append(Entry.from_dict(data))

        return entries_found

    def range_of_dates(self, start_date, end_date):
        """Finds entry from a ranged date search and returns a list of matching objects."""

        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")

        entries_found = []

        for data in self.entries:
            data_date = datetime.strptime(data['Date'], "%m/%d/%Y")

            if data_date >= start_date and data_date <= end_date:
                entries_found.append(Entry.from_dict(data))

        return entries_found

    def exact_search(self, search_term):
        """Finds entry from an exact title or notes search and returns a list of matching objects."""

        entries_found = []

        for data in self.entries:
            if search_term.lower() in data['Title'].lower() or search_term.lower() in data['Notes'].lower():
                entries_found.append(Entry.from_dict(data))

        return entries_found

    def regex_pattern(self, pattern):
        """Finds entry from a regex title search and returns a list of matching objects."""

        entries_found = []

        for data in self.entries:
            if re.search(pattern, data['Title']) or re.search(pattern, data['Notes']):
                entries_found.append(Entry.from_dict(data))

        return entries_found