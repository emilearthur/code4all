import collections
import csv
from os import name, write 
from random import randint
from collections import Counter, namedtuple

dataset_filename = "colors.csv"

def hex_to_rgb(hex_color):
    """
    RGB values are tuples of integers between 0 and 255. 
    This function converts from hex to RBG
    
    Notes: 
    range returns number [1,3,5] which represents the three channels. 
    For each of the three numbers, it extracts the two character string between i and i+2. 
    We then proceed to convert the string to base-16 integer using the int function. 
    The above funtion result to a generator which is then converted to a tuple. 
    """
    return tuple(int(hex_color[i : i+2], 16) for i in range(1, 6, 2)) 


def load_colors(filename):
    """Load colors and 

    Args:
        filename ([sting]): [name of file to read colors from]

    Returns:
        [generator of hex color and label]: [description]

    """
    with open(filename) as dataset_file:
        lines = csv.reader(dataset_file) # csv will return iterator of list of strings as ["Green", "#6edd13"] 
        for line in lines:
            label, hex_color = line 
            yield (hex_to_rgb(hex_color), label)


def generator_colors(count=100):
    "functions to generate colors"
    for i in range(count):
        yield (randint(0, 255), randint(0, 255), randint(0, 255))


def color_distance(color1, color2):
    """calculate distance between two colors

    Args:
        color1 (tuple): color 1 
        color2 (tuple): color 2 

    Returns:
        [Int]: sum_distance_squared of the two colors. 
    """
    channels = zip(color1, color2) 
    sum_distance_squared = 0 
    for c1, c2 in channels:
        sum_distance_squared += (c1 - c2) ** 2
    return sum_distance_squared 


def nearest_neighbors(model_colors, target_colors, num_neighbors=5):
    model_colors = list(model_colors) 
    for target in target_colors:
        distances = sorted(((color_distance(c[0], target), c) for c in model_colors))
        yield target, distances[:5]


def name_colors(model_colors, target_colors, num_neighbors=5):
    for target, near in nearest_neighbors(model_colors, target_colors, num_neighbors=5):
        print(target, near) 
        name_guess = Counter(n[1] for n in near).most_common()[0][0] 
        yield target, name_guess 


def write_results(colors, filename="output.csv"):
    with open(filename, "w") as file:
        writer = csv.writer(file) 
        for (r, b, g), name in colors:
            writer.writerow([name, f"#{r:02x}{g:02x}{b:02x}"])


def process_colors(dataset_filename="colors.csv"):
    model_colors = load_colors(dataset_filename)  # returns generator 
    colors = name_colors(model_colors, generator_colors(), 5)  # returns generator , also generator_color method is a generator.
    write_results(colors) 

if __name__ == "__main__":
    process_colors()

