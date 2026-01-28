# this program asks user for a number and prints the square root

def main():
    number = float(input("Please enter a number: "))
    print(f"The square of {number} is {squared(number)}")

def squared(n):
        return n * n

main()