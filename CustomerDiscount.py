# Customer Discount Eligibility Program

def money(x: float) -> str:
    """Format numbers as currency ($1,234.56)."""
    return f"${x:,.2f}"


while True:
    # ---- Inputs ----
    try:
        purchase_amount = float(input("Enter purchase amount: $").replace(",", "").strip())
        member_input = input("Are you a member? (yes/no): ").strip().lower()
    except ValueError:
        print("Invalid input. Please enter numeric values for purchase amount.\n")
        continue

    # ---- Validation ----
    if purchase_amount < 0:
        print("Purchase amount cannot be negative.\n")
        continue

    if member_input not in ("yes", "no"):
        print("Membership status must be 'yes' or 'no'.\n")
        continue

    is_member = member_input == "yes"

    # ---- Discount logic ----
    discount_rate = 0.0

    if is_member:
        if purchase_amount >= 100:
            discount_rate = 0.15
        else:
            discount_rate = 0.05
    else:
        if purchase_amount >= 150:
            discount_rate = 0.10
        else:
            discount_rate = 0.00

    # ---- Calculations ----
    discount_amount = purchase_amount * discount_rate
    final_price = purchase_amount - discount_amount

    # ---- Output (aligned & formatted) ----
    print("\n" + "=" * 40)
    print("ORDER SUMMARY")
    print("=" * 40)
    print(f"{'Purchase Amount:':22}{money(purchase_amount):>18}")
    print(f"{'Membership Status:':22}{('Member' if is_member else 'Non-Member'):>18}")
    print(f"{'Discount Applied:':22}{discount_rate * 100:>17.0f}%")
    print(f"{'Discount Amount:':22}{money(discount_amount):>18}")
    print("-" * 40)
    print(f"{'Final Price:':22}{money(final_price):>18}")
    print("=" * 40 + "\n")

    # ---- Loop option ----
    again = input("Process another customer? (y/n): ").strip().lower()
    if again != "y":
        break
