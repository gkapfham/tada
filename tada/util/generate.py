"""Generate data for Tada"""

import sys
import random
import string
from hypothesis_jsonschema import from_schema
from hypothesis import given, settings
from hypothesis import HealthCheck
from . import read


GENERATE = sys.modules[__name__]

DEFAULT_VALUE_INT = random.randint(0, 100)
DEFAULT_VALUE_CHAR = "C"
DEFAULT_VALUE_TEXT = "TEXT"
DEFAULT_VALUE_BOOLEAN = True


def generate_strategy(function, path, size):
    """generate a function with strategy from path and size"""
    json_schema = read.read_schema(path)
    for schema in json_schema:
        schema["maxItems"] = int(size)
        schema["minItems"] = int(size)
    strategy = []
    for j in json_schema:
        strategy.append(from_schema(j))
    # strategy = generate_strategy(json_schema)
    function = given(*strategy)(function)
    function = settings(
        max_examples=1,
        suppress_health_check=[
            HealthCheck.large_base_example,
            HealthCheck.too_slow,
            HealthCheck.data_too_large,
            HealthCheck.filter_too_much,
        ],
    )(function)
    return function


def generate_data(chosen_types, chosen_size):
    """Generate a list of data values"""
    generated_values = ()
    # call a generate function for each type
    for current_type in chosen_types:
        generator_to_invoke = getattr(GENERATE, "generate_" + str(current_type))
        generated_value = generator_to_invoke(chosen_size)
        generated_values = generated_values + (generated_value,)
    return generated_values


def generate_fake_hypothesis(a):
    """ use tool to test foo function """
    f = open("data.txt", "w+")
    f.write(str(a))
    f.close()


def generate_int(chosen_size):
    """Generate an int value"""
    lowerbound = 10 ** (int(chosen_size) - 1)
    upperbound = (10 ** int(chosen_size)) - 1
    return random.randint(lowerbound, upperbound)
    # return 10**(int(chosen_size))


def generate_int_list(chosen_size):
    """Generate an int list"""
    output = [random.random() for _ in range(int(chosen_size))]
    return output


def generate_char_list(chosen_size):
    """Generate a char list"""
    output = [
        random.choice(string.ascii_letters + string.digits)
        for _ in range(int(chosen_size))
    ]
    return output


# pylint: disable=unused-argument
def generate_char(chosen_size):
    """Generate a char value"""
    return DEFAULT_VALUE_CHAR


# pylint: disable=unused-argument
def generate_string(chosen_size):
    """Generate a string value"""
    return DEFAULT_VALUE_TEXT


# pylint: disable=unused-argument
def generate_boolean(chosen_size):
    """Generate a boolean value"""
    return DEFAULT_VALUE_BOOLEAN


def generate_float(chosen_size):
    """Generate an float value"""
    return float(chosen_size)
