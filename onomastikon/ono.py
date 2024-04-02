"""An onomastikon is a list of names, often used to generate random names."""

import csv
import os
import random
from typing import Optional

import appdirs

from onomastikon.config import get_project_meta

NAME, GENDER, COUNTRY, OCCURRENCES = 0, 1, 2, 3


class Onomastikon:

    def __init__(self, locale: Optional[str] = None) -> None:
        self.locale = locale
        self.first_names = self.load_locale("first_names")
        self.last_names = self.load_locale("last_names")

    def load_locale(self, which_file: str) -> list:
        """
        Load the data from the CSV file.

        :param which_file: The file to load
        :return: List of data
        """
        _meta = get_project_meta()
        data_dir = appdirs.user_data_dir(_meta["name"], _meta["authors"][0])
        data_file = os.path.join(data_dir, "data", f"{which_file}.csv")
        return_value = []

        with open(data_file, "r") as f:
            reader = csv.reader(f)
            if self.locale:
                return_value = [row for row in reader if row[2] == self.locale]
            else:
                return_value = list(reader)

        return return_value

    def _random_element(self, data, gender, ignore_weights=False) -> Optional[str]:
        """
        Return a random element from the data.

        :param data: The data to choose from
        :param gender: The gender to filter by
        :param ignore_weights: Ignore weights in the random choice
        :return: A random element
        """
        filtered = [name for name in data if name[GENDER] == gender]
        if not filtered:
            return None
        if not ignore_weights:
            weights = [int(name[OCCURRENCES]) for name in filtered]
            return random.choices(filtered, weights=weights, k=1)[0]
        return random.choice(filtered)

    def random_first_name(self, gender, ignore_weights=True) -> Optional[str]:
        """
        Return a random first name.

        :param gender: The gender to filter by
        :param ignore_weights: Include weights in the random choice
        :return: A random first name
        """
        _name = self._random_element(self.first_names, gender, ignore_weights)
        if _name:
            return _name[NAME]
        return None

    def random_last_name(self, gender, ignore_weights=True) -> Optional[str]:
        """
        Return a random last name.

        :param gender: The gender to filter by
        :param ignore_weights: Include weights in the random choice
        :return: A random last name
        """
        _name = self._random_element(self.last_names, gender, ignore_weights)
        if _name:
            return _name[NAME]
        return None

    def random_full_name(self, gender, include_weights=True) -> Optional[str]:
        """
        Return a random full name.

        :param gender: The gender to filter by
        :param include_weights: Include weights in the random choice
        :return: A random full name
        """
        first_name = self.random_first_name(gender)
        last_name = self.random_last_name(gender)
        if first_name and last_name:
            return f"{first_name} {last_name}"
        return None

    def random_name(
        self,
        gender: str,
        include_weights=True,
        second_name_prob: int = 0,
        second_last_name_prob: int = 0,
    ) -> Optional[str]:
        """
        Return a random name.

        :param gender:
        :type: str
        :param include_weights: Include weights in the random choice
        :type include_weights: bool
        :param second_name_prob: Probability of having a second name (default is 0%)
        :type second_name_prob: int
        :param second_last_name_prob: Probability of having a second last name (default is 0%)
        :type second_last_name_prob: int

        :return: A random name
        :rtype: str
        """
        first_name = self.random_first_name(
            ignore_weights=include_weights, gender=gender
        )
        last_name = self.random_last_name(
            ignore_weights=include_weights, gender=gender
        )
        second_name = None
        second_last_name = None
        if random.randint(1, 100) <= second_name_prob:
            second_name = f"{self.random_first_name(ignore_weights=include_weights, gender=gender)}"
        if random.randint(1, 100) <= second_last_name_prob:
            second_last_name = f"{self.random_last_name(ignore_weights=include_weights, gender=gender)}"
        result = ""
        if first_name:
            result = first_name
        if second_name:
            result = f"{result} {second_name}"
        if last_name:
            result = f"{result} {last_name}"
        if second_last_name:
            result = f"{result}-{second_last_name}"
        return result
