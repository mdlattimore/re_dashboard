import math


def estimate_title_insurance(purchase_price: float = 0, loan_amount: float =
0, number_of_endorsements: int = 0) -> float:
    coverage = max(purchase_price, loan_amount)
    total = 15  # base fee is commitment fee
    if purchase_price and loan_amount:
        total += 26  # simultaneous issue
    cpl = 0
    if loan_amount:
        loan_coverage_thousands = math.ceil(loan_amount / 1000)
        if loan_coverage_thousands <= 100:
            cpl = loan_coverage_thousands * .63
        else:
            cpl = (math.ceil((loan_amount - 100000) / 1000) * .12) + 63
        number_of_endorsements = max(number_of_endorsements, 2)

        total += (number_of_endorsements * 21) + cpl

    brackets = [
        (100, 2.54),
        (400, 1.98),
        (1500, 1.29),
        (5000, 0.99),
        (math.inf, 0.69)
    ]

    thousands = math.ceil(coverage / 1000)
    remaining = thousands

    for limit, rate in brackets:
        chunk = min(remaining, limit)
        total += chunk * rate
        remaining -= chunk
        if remaining <= 0:
            break
    print(cpl)
    return total




