from datetime import datetime


class Entry:
    """This will help on the transfer to the database later on..."""

    def __init__(self, date, title, time_spent, notes=''):
        self.fields = ['Date', 'Title', 'Time Spent', 'Notes']

        self.date = date
        self.title = title
        self.time_spent = time_spent
        self.notes = notes

    def to_dict(self):
        """Turn object data into a dictionary"""

        entry_dict = {
            self.fields[0]: self.date,
            self.fields[1]: self.title,
            self.fields[2]: self.time_spent,
            self.fields[3]: self.notes,
        }

        return entry_dict

    @classmethod
    def from_dict(cls, raw_dict):
        """Turn object data into a dictionary"""

        entry_obj = cls(raw_dict['Date'], raw_dict['Title'],
                        raw_dict['Time Spent'], raw_dict['Notes'])

        return entry_obj

    @staticmethod
    def date_check(date_str):
        """Dates must be in DD/MM/YYYY format"""

        date_good = True

        try:
            datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            date_good = False

        return date_good

    @staticmethod
    def time_check(time_str):
        """Times must be in minutes format"""

        time_good = True

        try:
            datetime.strptime(time_str, "%M")
        except ValueError:
            time_good = False

        return time_good

    def display_entry(self):
        """Prints an entry object for user"""

        text = ""

        for key, value in self.to_dict().items():
            text += key + ": " + value + "\n"

        return text
