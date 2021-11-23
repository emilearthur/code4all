"""
This exercise stub and the test suite contain several enumerated constants.

Since Python 2 does not have the enum module, the idiomatic way to write
enumerated constants has traditionally been a NAME assigned to an arbitrary,
but unique value. An integer is traditionally used because it’s memory
efficient.
It is a common practice to export both constants and functions that work with
those constants (ex. the constants in the os, subprocess and re modules).

You can learn more here: https://en.wikipedia.org/wiki/Enumerated_type
"""


# Score categories.
# Change the values as you see fit.
YACHT = "YACHT"
ONES = "ONES"
TWOS = "TWOS"
THREES = "THREES"
FOURS = "FOURS"
FIVES = "FIVES"
SIXES = "SIXES"
FULL_HOUSE = "FULL_HOUSE"
FOUR_OF_A_KIND = "FOUR_OF_A_KIND"
LITTLE_STRAIGHT = "LITTLE_STRAIGHT"
BIG_STRAIGHT = "BIG_STRAIGHT"
CHOICE = "CHOICE"


def score(dice, category):
    if len(dice) != 5:
        raise ValueError("Lenght of dice should be 5")

    dice = sorted(dice)

    if category == "ONES":
        out = dice.count(1)
        return 1 * out

    elif category == "TWOS":
        out = dice.count(2)
        return 2 * out

    elif category == "THREES":
        out = dice.count(3)
        return 3 * out

    elif category == "FOURS":
        out = dice.count(4)
        return 4 * out

    elif category == "FIVES":
        out = dice.count(5)
        return 5 * out

    elif category == "SIXES":
        out = dice.count(6)
        return 6 * out

    elif category == "FULL_HOUSE":
        threes = 0
        twos = 0

        for a in dice:
            if dice.count(a) == 3:
                threes = 3 * a
        for a in dice:
            if dice.count(a) == 2:
                twos = 2 * a

        if threes and twos != 0:
            return threes + twos
        return 0

    elif category == "FOUR_OF_A_KIND":
        fours = 0
        for a in dice:
            if dice.count(a) >= 4:
                fours = 4 * a
        if fours != 0:
            return fours
        return 0

    elif category == "LITTLE_STRAIGHT":
        if dice == [1, 2, 3, 4, 5]:
            return 30
        return 0

    elif category == "BIG_STRAIGHT":
        if dice == [2, 3, 4, 5, 6]:
            return 30
        return 0

    elif category == "CHOICE":
        return sum(dice)

    elif category == "YACHT":
        fives = 0
        for a in dice:
            if dice.count(a) == 5:
                fives = a
        if fives != 0:
            return 50
        return 0
    else:
        return "Choose a category"
