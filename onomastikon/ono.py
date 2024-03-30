import csv
import os
import random
from typing import Optional

NAME, GENDER, COUNTRY, OCCURRENCES = 0, 1, 2, 3


class Onomastikon:

    def __init__(self, locale: Optional[str] = None):
        self.locale = locale
        self.first_names = self.load_locale("first_names")
        self.last_names = self.load_locale("last_names")

    def load_locale(self, which_file: str):
        data_dir = "data"
        data_file = os.path.join(data_dir, f"{which_file}.csv")
        return_value = []

        with open(data_file, "r") as f:
            reader = csv.reader(f)
            if self.locale:
                return_value = [row for row in reader if row[2] == self.locale]
            else:
                return_value = list(reader)

        return return_value

    def _random_element(self, data, gender, include_weights=True):
        filtered = [name for name in data if name[GENDER] == gender]
        if not filtered:
            return None
        if include_weights:
            weights = [int(name[OCCURRENCES]) for name in filtered]
            return random.choices(filtered, weights=weights, k=1)[0]
        return random.choice(filtered)

    def random_first_name(self, gender, include_weights=True):
        # Return a random first name
        _name = self._random_element(self.first_names, gender, include_weights)
        if _name:
            return _name[NAME]
        return None

    def random_last_name(self, gender, include_weights=True):
        _name = self._random_element(self.last_names, gender, include_weights)
        if _name:
            return _name[NAME]
        return None

    def random_full_name(self, gender, include_weights=True, include_middle_name=False):
        first_name = self.random_first_name(gender)
        middle_name = ""
        if include_middle_name:
            middle_name = self.random_first_name(gender, include_weights)
        last_name = self.random_last_name(gender)
        if first_name and last_name:
            if middle_name:
                return f"{first_name} {middle_name} {last_name}"
            return f"{first_name} {last_name}"
        return None
