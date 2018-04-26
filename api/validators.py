""" This class validates user input and will be used in the input_utils module
"""

import re


class Validation:
    """Has methods to validate user's input
    """

    def __init__(self, user_inputs):
        """ This avails input dictionary to the class
        """
        self.all = user_inputs

    def email(self, key, email):
        """Check required input is email type
        """
        if key in self.all:
            if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z]+$", self.all[key]):
                return "Invalid email address"
            return True
        return True

    def confirm(self, key, confirm):
        """Check if given password matches with the other one
        """
        if key in self.all and confirm in self.all:
            if self.all[confirm] != self.all[key]:
                return confirm + " don't match"
            return True
        return True

    def string(self, key, string):
        """Check if the input given is a string"""
        if key in self.all and self.all[key] is not None:
            if not re.match(r"[^[a-zA-Z0-9]+$", self.all[key]):
                return True
            return key + " should be a string"
        return True

    def float(self, key, float):
        """Check if the input given is a float"""
        if key in self.all and self.all[key] is not None:
            if not re.match(r"[^[0-9]+\.?[0-9]+$", self.all[key]):
                return True
            return key + " should be a type float e.g 450.00"
        return True

    def minimum(self, key, minimum):
        """Check the required character size"""
        if key in self.all and self.all[key] is not None:
            if len(self.all[key]) < int(minimum):
                return key + " should not be less than " + str(minimum) + " characters"
            return True
        return True

    def maximum(self, key, maximum):
        """Check the required character size"""
        if key in self.all and self.all[key] is not None:
            if len(self.all[key]) > int(maximum):
                return key + " should not be greater than " + str(maximum) + " characaters"
            return True
        return True

    def required(self, key, is_required=True):
        """Check input it is required"""
        if key in self.all:
            if self.all[key] is None:
                return key + " should not be empty"
            return True
        return key + " is required"
