# The main code file containing 2 methods to calculate square and cube of a number

def calculate_square(num):
    square = num * num
    return square

def calculate_cube(num):
    cube = calculate_square(num) * num
    return cube
