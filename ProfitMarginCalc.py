def new_func():
    # Prompt user for inputs
    revenue = float(input("What's the revenue? "))
    cost = float(input("What's the cost? "))

# Calculate profit
    profit = revenue - cost

# Check for valid revenue before calculating margin
    if revenue > 0:
        margin = (profit / revenue) * 100
        print(f"Profit: ${profit:,.2f} | Margin: {margin:.2f}%")
    else:
        print("Invalid revenue.")

new_func()