def amortization(loan_amount, interest_rate, term):
    """ Takes a loan amount, interest rate, and loan term (in months) and
        returns a list of tuples containing index(pmt number), payment, 
        interest, principal, and balance. Makes use of a helper function
        `monthly_payment` to calculate the monthly principal and interest
        payment on the loan.
    """
    pmt = monthly_payment(loan_amount, interest_rate, term)
    pb = loan_amount
    rnd = 2  # Set the number of rounded digits

    # Empty list to hold the tuples returned by this function
    output = []

    # Iterate through the values a number of times equal to the term of the loan
    # (in months) to build the data that will be output as a list of tuples
    for index in range(1, term + 1):
        monthly_interest = round(((interest_rate / 100) * pb) / 12, rnd)
        monthly_principal = round(pmt - monthly_interest, rnd)
        
        
        #------------------------------
        #-This block checks to see if the payment amount exceeds the remaining
        # principal balance plus the interest due on that balance. If it does (which 
        # will always occur, if at all, on the final payment), it adjusts the final 
        # payment to an amount that will pay the balance (including interest) to zero.
        if pmt > pb + monthly_interest:
            pmt = round(pb + monthly_interest, rnd)
            monthly_interest = round(((interest_rate / 100) * pb) / 12, rnd)
            monthly_principal = round(pmt - monthly_interest, rnd)
            pb = round(pb - monthly_principal, rnd)
            output.append((index, pmt, monthly_interest, monthly_principal, pb))
            return output
        #------------------------------
            
        pb = round(pb - monthly_principal, rnd)
        output.append((index, pmt, monthly_interest, monthly_principal, pb))
    return output
    

def monthly_payment(loan_amount, interest_rate, term):
    """ A helper function to the amortization function. """
    l = loan_amount
    i = (float(interest_rate) / 12) / 100 
    t = term
    # Formula for calculating the principal and interest payment for an 
    # amortized loan
    payment = (l * (i * (1 + i) ** t) / ((1 + i) ** t - 1)) 
    return round(payment, 2)


if __name__ == "__main__":
    # Insert diagnostic code here
    pass

