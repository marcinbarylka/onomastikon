import csv
import os
import random


NAME, GENDER, COUNTRY, OCCURRENCES = 0, 1, 2, 3


class Onomastikon:

    def __init__(self, locale: str):
        self.locale = locale
        self.first_names = self.load_locale("first_names")
        self.last_names = self.load_locale("last_names")

    def load_locale(self, which_file: str):
        # Load the data for the given locale
        data_dir = "data"
        data_file = os.path.join(data_dir, f"{which_file}.csv")
        return_value = []
        with open(data_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[2] == self.locale:
                    return_value.append(row)
        return return_value

    def _random_element(self, data, gender):
        filtered = [name for name in data if name[GENDER] == gender]
        if not filtered:
            return None
        weights = [int(name[OCCURRENCES]) for name in filtered]
        return random.choices(filtered, weights=weights, k=1)[0]

    def random_first_name(self, gender):
        # Return a random first name
        _name = self._random_element(self.first_names, gender)
        if _name:
            return _name[NAME]
        return None

    def random_last_name(self, gender):
        _name =  self._random_element(self.last_names, gender)
        if _name:
            return _name[NAME]
        return None

    def random_full_name(self, gender):
        first_name = self.random_first_name(gender)
        last_name = self.random_last_name(gender)
        if first_name and last_name:
            return f"{first_name} {last_name}"
        return None