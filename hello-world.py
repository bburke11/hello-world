# This program asks the user for their name and says hello

name = input("What is your name? ")

clean_name = " ".join(name.replace(".", "").split()).title()

print(f"Hello, {clean_name}")
    