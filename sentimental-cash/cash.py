# TODO
from cs50 import get_float


def main():

    owed = get_change()

    # use function to calculate quarters and then subtract that from the total amount owed
    quarters = calculate_quarter(owed)
    owed = owed - quarters * 25

    # use function to calculate dimes and then subtract that from the total amount owed
    dimes = calculate_dime(owed)
    owed = owed - dimes * 10

    # use function to calculate nickels and then subtract that from the total amount owed
    nickels = calculate_nickel(owed)
    owed = owed - nickels * 5

    # use function to calculate pennies and then subtract that from the total amount owed
    pennies = calculate_penny(owed)
    owed = owed - pennies * 1

    coins = quarters + nickels + dimes + pennies

    print(f"{coins}")


# ask for how much change is owed. keep loop going if user give negative amount
def get_change():
    while True:
        change = get_float("Change owed: ")
        if change > 0:
            break
    return change * 100


# calculate how many quarters you need
def calculate_quarter(n):
    quarter = 0
    while n >= 25:
        n -= 25
        quarter += 1
    return quarter


# calculate how many dimes you need
def calculate_dime(n):
    dime = 0
    while n >= 10:
        n -= 10
        dime += 1
    return dime


# calculate how many nickels you need
def calculate_nickel(n):
    nickel = 0
    while n >= 5:
        n -= 5
        nickel += 1
    return nickel


# calculate how many pennies you need
def calculate_penny(n):
    penny = 0
    while n >= 1:
        n -= 1
        penny += 1
    return penny


if __name__ == "__main__":
    main()

