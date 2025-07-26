from datetime import datetime as dt


def calculate_mortgage_payoff(p: float, i: float, p_as_of: dt,
                               good_through: dt, accrual_basis: int) -> float:
        n = i / 100  # convert interest rate to decimal
        per_diem: float = round((p * n) / accrual_basis, 4)
        number_of_days = (good_through - p_as_of).days
        total_interest = per_diem * number_of_days
        payoff = p + total_interest
        return payoff, per_diem
