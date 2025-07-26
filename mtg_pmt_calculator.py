def calculate_payment(p, r, n):
    i = (r / 100) / 12
    payment = p * (i * (1 + i)**n) / ((1 + i)**n - 1)
    return payment