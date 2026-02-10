# Employee Performance Bonus + Annual Financial Snapshot (2026 single filer estimate)
# Assumptions:
# - User is a single filer
# - Uses 2026 standard deduction ($16,100)
# - Federal income tax only + FICA (Social Security + Medicare)
# - This is an estimate (ignores credits, pre-tax deductions, state taxes, etc.)

STANDARD_DEDUCTION_2026_SINGLE = 16100.00

# 2026 federal tax brackets (single) for *taxable income*
# Each tuple: (top_of_bracket, rate)
BRACKETS_2026_SINGLE = [
    (12400, 0.10),
    (50400, 0.12),
    (105700, 0.22),
    (201775, 0.24),
    (256225, 0.32),
    (640600, 0.35),
    (float("inf"), 0.37),
]

# FICA assumptions for 2026
SOCIAL_SECURITY_RATE = 0.062
SOCIAL_SECURITY_WAGE_BASE_2026 = 184500.00
MEDICARE_RATE = 0.0145
ADDL_MEDICARE_RATE = 0.009
ADDL_MEDICARE_THRESHOLD_SINGLE = 200000.00


def money(x: float) -> str:
    """Format a number like $65,000.00"""
    return f"${x:,.2f}"


def federal_income_tax_2026_single(gross_income: float) -> float:
    """Estimate federal income tax for a single filer using the 2026 brackets + standard deduction."""
    taxable = max(0.0, gross_income - STANDARD_DEDUCTION_2026_SINGLE)

    tax = 0.0
    lower = 0.0

    for upper, rate in BRACKETS_2026_SINGLE:
        if taxable <= lower:
            break

        amount_in_bracket = min(taxable, upper) - lower
        tax += amount_in_bracket * rate
        lower = upper

    return tax


def fica_tax_2026(gross_wages: float) -> float:
    """Estimate employee FICA taxes (Social Security + Medicare)."""
    ss_tax = min(gross_wages, SOCIAL_SECURITY_WAGE_BASE_2026) * SOCIAL_SECURITY_RATE
    medicare_tax = gross_wages * MEDICARE_RATE

    # Additional Medicare tax for single filers over $200,000
    addl_medicare_tax = 0.0
    if gross_wages > ADDL_MEDICARE_THRESHOLD_SINGLE:
        addl_medicare_tax = (gross_wages - ADDL_MEDICARE_THRESHOLD_SINGLE) * ADDL_MEDICARE_RATE

    return ss_tax + medicare_tax + addl_medicare_tax


def bonus_rate_from_score(score: float) -> float:
    """Return bonus rate based on performance score."""
    if 90 <= score <= 100:
        return 0.20
    elif 80 <= score <= 89:
        return 0.10
    elif 70 <= score <= 79:
        return 0.05
    else:
        return 0.00


while True:
    # ---- Inputs ----
    try:
        salary = float(input("Enter annual salary: $").replace(",", "").strip())
        score = float(input("Enter performance score (0-100): ").strip())
    except ValueError:
        print("Invalid input. Please enter numbers only.\n")
        continue

    # ---- Validation ----
    if salary < 0:
        print("Salary cannot be negative.\n")
        continue
    if score < 0 or score > 100:
        print("Performance score must be between 0 and 100.\n")
        continue

    # ---- Bonus calculation ----
    rate = bonus_rate_from_score(score)
    bonus = salary * rate

    # ---- Annual snapshot calculations ----
    gross_total = salary + bonus

    est_federal_tax = federal_income_tax_2026_single(gross_total)
    est_fica = fica_tax_2026(gross_total)

    est_total_taxes = est_federal_tax + est_fica
    est_take_home = gross_total - est_total_taxes

    # ---- Output (aligned & formatted) ----
    print("\n" + "=" * 44)
    print("ANNUAL FINANCIAL SNAPSHOT (EST.)")
    print("=" * 44)
    print(f"{'Base Salary:':25}{money(salary):>19}")
    print(f"{'Performance Score:':25}{score:>19.1f}")
    print(f"{'Bonus Rate:':25}{(rate*100):>18.0f}%")
    print(f"{'Bonus Amount:':25}{money(bonus):>19}")
    print("-" * 44)
    print(f"{'Gross Total Pay:':25}{money(gross_total):>19}")
    print(f"{'Std Deduction (2026):':25}{money(STANDARD_DEDUCTION_2026_SINGLE):>19}")
    print(f"{'Est. Federal Income Tax:':25}{money(est_federal_tax):>19}")
    print(f"{'Est. FICA (SS+Medicare):':25}{money(est_fica):>19}")
    print("-" * 44)
    print(f"{'Est. Total Taxes:':25}{money(est_total_taxes):>19}")
    print(f"{'Est. Take-Home Pay:':25}{money(est_take_home):>19}")
    print("=" * 44 + "\n")

    # ---- Loop option ----
    again = input("Calculate another employee? (y/n): ").strip().lower()
    if again != "y":
        break

