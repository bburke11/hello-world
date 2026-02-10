# Loan Risk Classification + Loan Pricing (Treasury + Spread)
# Assumptions:
# - Treasury curve is stored below (as of 2/10/26)
# - "Closest maturity" means nearest Treasury maturity by years
# - Spread is based on credit score + loan-to-income ratio (loan_amount / annual_income)
# - Expected Yield = Treasury Rate + Spread

def money(x: float) -> str:
    """Format a number like $65,000.00"""
    return f"${x:,.2f}"

def pct(x: float) -> str:
    """Format decimal as percent like 4.25%"""
    return f"{x * 100:.2f}%"

# --- Treasury curve (EDIT to match your uploaded chart) ---
# Rates are decimals (ex: 0.0430 = 4.30%)
TREASURY_CURVE = {
    1: 0.0342,   # 1Y
    2: 0.0348,   # 2Y
    3: 0.0355,   # 3Y
    5: 0.0375,   # 5Y
    7: 0.0397,   # 7Y
    10: 0.0421,  # 10Y
    20: 0.0479,  # 20Y
    30: 0.0485,  # 30Y
}

def closest_treasury_rate(maturity_years: int) -> tuple[int, float]:
    """Return (closest_maturity, rate) from the curve."""
    closest = min(TREASURY_CURVE.keys(), key=lambda y: abs(y - maturity_years))
    return closest, TREASURY_CURVE[closest]

def risk_category(credit_score: int, annual_income: float) -> str:
    """Original assignment risk classification."""
    if credit_score >= 720 and annual_income >= 60000:
        return "Low Risk"
    elif credit_score >= 650 and annual_income >= 40000:
        return "Medium Risk"
    else:
        return "High Risk"

def spread_bps(credit_score: int, loan_to_income: float) -> int:
    """
    Determine spread in basis points (bps) above Treasury.
    Logic:
    - Higher credit score => lower spread
    - Higher loan-to-income => higher spread
    """

    # Base spread from credit score (bps)
    if credit_score >= 800:
        base = 100   # 1.00%
    elif credit_score >= 740:
        base = 175   # 1.75%
    elif credit_score >= 680:
        base = 275   # 2.75%
    elif credit_score >= 620:
        base = 375   # 3.75%
    else:
        base = 500   # 5.00%

    # Add-on from loan-to-income (bps)
    # (Loan amount as % of annual income)
    if loan_to_income <= 0.20:
        add_on = 0
    elif loan_to_income <= 0.35:
        add_on = 50
    elif loan_to_income <= 0.50:
        add_on = 125
    else:
        add_on = 250

    return base + add_on


while True:
    # ---- Inputs ----
    try:
        credit_score = int(input("Enter credit score (0-850): ").strip())
        annual_income = float(input("Enter annual income: $").replace(",", "").strip())
        loan_amount = float(input("Enter requested loan amount: $").replace(",", "").strip())
        maturity_years = int(input("Enter loan maturity (years, ex: 1,2,3,5,7,10,20,30): ").strip())
    except ValueError:
        print("Invalid input. Please enter numbers only.\n")
        continue

    # ---- Validation ----
    if credit_score < 0 or credit_score > 850:
        print("Credit score must be between 0 and 850.\n")
        continue
    if annual_income <= 0:
        print("Annual income must be greater than 0.\n")
        continue
    if loan_amount <= 0:
        print("Loan amount must be greater than 0.\n")
        continue
    if maturity_years <= 0:
        print("Maturity must be at least 1 year.\n")
        continue

    # ---- Core calculations ----
    lti = loan_amount / annual_income  # loan-to-income ratio
    risk = risk_category(credit_score, annual_income)

    closest_mat, tsy_rate = closest_treasury_rate(maturity_years)
    spread = spread_bps(credit_score, lti)  # in bps
    expected_yield = tsy_rate + (spread / 10000)  # bps -> decimal rate

    # ---- Output ----
    print("\n" + "=" * 56)
    print("LOAN PRICING SNAPSHOT (Treasury + Spread)")
    print("=" * 56)
    print(f"{'Credit Score:':28}{credit_score:>28}")
    print(f"{'Annual Income:':28}{money(annual_income):>28}")
    print(f"{'Requested Loan Amount:':28}{money(loan_amount):>28}")
    print(f"{'Loan Maturity (Years):':28}{maturity_years:>28}")
    print(f"{'Loan-to-Income (LTI):':28}{pct(lti):>28}")
    print("-" * 56)
    print(f"{'Risk Category:':28}{risk:>28}")
    print(f"{'Closest Treasury Maturity:':28}{str(closest_mat) + 'Y':>28}")
    print(f"{'Treasury Rate:':28}{pct(tsy_rate):>28}")
    print(f"{'Spread (bps):':28}{spread:>28}")
    print("-" * 56)
    print(f"{'Expected Yield:':28}{pct(expected_yield):>28}")
    print("=" * 56 + "\n")

    # ---- Loop option ----
    again = input("Price another loan? (y/n): ").strip().lower()
    if again != "y":
        break
