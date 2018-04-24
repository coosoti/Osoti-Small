"""Utils rules for input validation
"""
from .validators import Validation

# Create meal validation rules

CREATE_MEAL_RULES = [
    #Assuming food with minimal characters in title is three  e.g tea
    {'title': [('minimum', 3), ('required', True)]},
    {'price': [('float', True), ('required', True)]},
]


def validate(inputs, input_rules):
    """ Method to implement validation rules on user input. """
    errors_dict = {}
    valid = Validation(inputs)
    for rules in input_rules:
        for key in rules:
            rule_key = key
            for rule in rules[rule_key]:
                execute = getattr(valid, rule[0])(
                    rule_key, rule[1])
                if execute is True:
                    pass
                if execute != True:
                    if rule_key in errors_dict:
                        errors_dict[rule_key].append(execute)
                    else:
                        errors_dict[rule_key] = []
                        errors_dict[rule_key].append(execute)
    if len(errors_dict) > 0:
        return errors_dict
    return True