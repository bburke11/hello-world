# print name and say hello

def main():
#output greeting
    name = input("What is your name? ")
    hello(name)
    
    # output wirhout passing the expected argument
    hello()

def hello(to='John Doe'):
    print("Hello," , to)

main()