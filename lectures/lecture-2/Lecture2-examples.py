## This script should run directly as `python Lecture2-examples.py`
# if the python environment is configured correctly

#### Atomic types ####
integer = 123
floating_point = 3.1415
complex_number = 0+1j
string = "Hello, World!"
boolean = True  # or False
none = None

# Tuples are like an immutable (unchangeable) list
tup = ('A', 'B', 3)
# String can also use single-quotes
string = "An altered string"

# Lists
example_list = list()
example_list = []  # Same thing
# Ordered, and iterable
# Basic iteration in "for" loop
for index_number in range(10):
    example_list.append(index_number)

# Dictionary
example_dictionary = dict()
example_dictionary = {}  # Same thing
# An iterable map of keys to values
example_dictionary['pet'] = 'cat'
example_dictionary['count'] = 12345

# Sets
set1 = set()
# Sets are unordered, and maintain unique values only
set1.update([1,2,3])
print(f"Set 1: {set1}")
set1.update([2,3,4,5])
print(f"Set 1: {set1}")

# Beware that variables are not protected
very_valuable_dictionary = {'contents': 
    'something super important that took 24 hours to complete'
    }
very_valuable_dictionary = '...Ooops :/'


#### Control flow
# Boolean control flow
condition = True
if condition:
    # Proceed this way
    ...  
    # (Ellipsis is a special built-in 
    # called a no-op (no operation))
else:
    # Proceed this way
    ...

# Numeric control flow
condition = 1
if condition < 1:
    ...
elif condition == 1:
    ...
elif condition > 1:
    ...
# Or, for example
if condition >= 1:
    ...
else:
    ...

# match-case (Python >= 3.10): Similar to case/switch 
# statements in other languages
def match_case(condition):
    match condition:
        case 1:
            return "Only performs matching, " \
                "no other comparison operators"
        case _:
            return "This is the default for all " \
                "non-matching cases. " \
                "'_' indicates 'All other values'"

# Control flow can include catching errors in computations
assertion = False
try:
    assert(assertion), "This should never pass an assertion"
except Exception as e:
    print(f"Caught error: {e}")

# Basic system calls
#### Printing ####
# Multiple ways to print a string
print(f"This is an f-string: {string}")
print("This is 'modern' formatting: {}".format(string))
print("This is legacy C-like formatting, but is considered deprecated: %s" % string)
# There is a way to try catching errors in control flow
try:
    print("This is legacy C-like formatting, but is considered deprecated: %i" % string)
except Exception as e:
    print("\t - Errors like this are why this form is deprecated")
    print(f"{e}: Caused an exception")
    pass

# Special characters: \t - "tab", \n - "newline" 
# (on Windows, this is \r\n ("carriage return+newline"))
print(f"Tab:[\t] Newline: [\n]")

# Assertions
assert(True), "Error on True is not correct"

# Type checking at runtime
print(f"The type here should be an integer: {type(42)}")

# Opening and reading a file
# Use the "with" context manager keyword
with open('example.vcf', 'r') as file_pointer:
    # A list of every line in the example, split on '\n' by default
    data = file_pointer.readlines()
    print("*"*80)
    print(data)
    print("*"*80)
# Writing a file out
with open('output.csv', 'w') as output_pointer:
    for line in data:
        output_pointer.write(line)

#### Functions
# 'def' keyword flags Python that the following block is a function
def function1(argument1, argument2):
    # Functions are passed arguments
    # So the name is very important, as Python does not perform type checking
    # For example, strings can be added but not divided
    print(f"{argument1} ::: {argument2}")
    # By default, Python requires the "return" keyword or will return "None"

def add_numbers(num1, num2):
    return num1 + num2

# Functions are "stateless" and "scoped"
numerical_arg = 1
def stateless_function(numerical_arg):
    print(f"I got a numerical argument: {numerical_arg}")
    numerical_arg = numerical_arg + 1
    print(f"Now, that is: {numerical_arg}")

print(f"Numerical arg started as: {numerical_arg}")
stateless_function(numerical_arg)
print(f"Numerical arg is now: {numerical_arg}")

# State must be returned from a function
def add_one(numerical_arg):
    return numerical_arg + 1
numerical_arg = add_one(numerical_arg)

# Function variables are scoped, but can be inherited from the environment
# Note that functions don't require arguments
value = 1
def add_and_report():
    value += 1
    print(f"LOCAL Value: {value}")
print(f"GLOBAL Value: {value}")

# The 'global' keyword can be used to persist variables, 
# but can cause problems as a codebase grows
global_value = 1
def add_global():
    global global_value
    global_value += 1
    print(f"LOCAL Value (with global keyword): {global_value}")

print(f"GLOBAL Value (with global keyword): {global_value}")
add_global()
print(f"GLOBAL Value (with global keyword): {global_value}")

#### Objects
# Defined using the 'class' keyword
class MyAddingObject:

    # Classes can have 'class variables' and 'class methods'
    classAttribute = 'AddingObject'
    # We will not worry about class methods here

    # Objects have a constructor method called __init__
    def __init__(self, num1, num2):
        self.number1 = num1
        self.number2 = num2

    def add_numbers(self):
        return self.number1 + self.number2

    def change_number_1(self, new_value):
        self.number1 = new_value
    
    def change_number_2(self, new_value):
        self.number2 = new_value

adder = MyAddingObject(1, 1)
# Objects maintain state internally
print(f"Object addition: {adder.add_numbers()}")
adder.change_number_1(10)
adder.change_number_2(10)
print(f"Object addition, revised state: {adder.add_numbers()}")

#### Packages
# Python has many packages by default, called the "stdlib" (standard library)
# There is also a standard package manager for 
# handling external dependecies, called `pip`

# The standard library package for interacting with the
# operating system is os
import os
# For example, allow all users to run a script in their home
# directories by asking the OS what a user shortcut is
# In Linux/Mac, this is "~" or "$HOME". On Windows, it is %USERPROFILE%.
my_home_dir = os.path.expanduser("~/")
print(f"My home directory is: {my_home_dir}")

# "unlink" is the old term for delete or remove
os.unlink("output.csv")
# This is equivalent to os.remove(), 
# which was added later as "unlink" left common use

# AI packages rely on common math packages
import scipy
# Imports can be aliased
import numpy as np
import pandas as pd
# This is true of AI/ML packages as well
import sklearn as skl
# We can also import only the components we are interested in
from sklearn.tree import DecisionTreeClassifier
