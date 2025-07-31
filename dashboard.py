import json

import streamlit as st

from get_econ_data import get_current_inflation_rate, \
    get_current_thirty_year_conventional_mortgage_rate, \
    get_current_unemployment_rate, get_current_gas_price, \
    get_current_fifteen_year_conventional_mortgage_rate
from mtg_payoff_calculator import calculate_mortgage_payoff
from mtg_pmt_calculator import calculate_payment
from property_tax_calculator import calculate_property_tax
from title_insurance_estimator import estimate_title_insurance
from amortization_function import amortization
import pandas as pd


# ---------- Cached API wrappers ----------

@st.cache_data(ttl=3600)
def cached_get_current_inflation_rate():
    return get_current_inflation_rate()


@st.cache_data(ttl=3600)
def cached_get_current_thirty_year_conventional_mortgage_rate():
    return get_current_thirty_year_conventional_mortgage_rate()


@st.cache_data(ttl=3600)
def cached_get_current_unemployment_rate():
    return get_current_unemployment_rate()


@st.cache_data(ttl=3600)
def cached_get_current_gas_price():
    return get_current_gas_price()


@st.cache_data(ttl=3600)
def cached_get_current_fifteen_year_conventional_mortgage_rate():
    return get_current_fifteen_year_conventional_mortgage_rate()


st.set_page_config(page_title="RE Dashboard")

st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem;
            # max-width: 1000px;
            # padding-left: 2rem;
            # padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.header("RE Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    inflation = cached_get_current_inflation_rate()
    st.write("#### Inflation")
    st.write(f"{inflation[0]}% ({inflation[1]})")

with col2:
    st.write("#### Conv 30 Yr Rate")
    rate = cached_get_current_thirty_year_conventional_mortgage_rate()
    st.write(f"{rate[0]}% ({rate[1]})")

with col3:
    st.write("#### Conv 15 Yr Rate")
    rate = cached_get_current_fifteen_year_conventional_mortgage_rate()
    st.write(f"{rate[0]}% ({rate[1]})")

col4, col5, col6 = st.columns(3)

with col4:
    st.write("#### Unemployment")
    unemployment_rate = cached_get_current_unemployment_rate()
    st.write(f"{unemployment_rate[0]}% ({unemployment_rate[1]})")

with col5:
    st.write("#### Gas")
    gas_price = cached_get_current_gas_price()
    st.write(f"${gas_price[0]} ({gas_price[1]})")

with col6:
    st.write("#### Place Holder")

# CALCULATORS
st.subheader("Calculators")

tab1, tab2, tab3, tab4 = st.tabs(["Mortgage Payment", "Mortgage Payoff",
                                     "Property Tax", "Closing Costs (Title)"])

# Mortgage payment calculator
# with tab1:
#     st.write("Mortgage Payment Calculator")
#
#     # Get raw string inputs
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         p_input = st.text_input("Principal amount of loan")
#     with col2:
#         r_input = st.text_input("Interest rate (annual)")
#     with col3:
#         n_input = st.text_input("Term of loan (in months)")
#     col4, col5, col6 = st.columns(3)
#     with col4:
#         t_input = st.text_input("Annual taxes", value="0")
#     with col5:
#         i_input = st.text_input("Annual insurance", value="0")
#
#     if st.button("Calculate Payment"):
#         try:
#             p = float(p_input)
#             r = float(r_input)
#             n = int(n_input)
#             t = float(t_input)
#             i = float(i_input)
#
#             pi_payment = calculate_payment(p, r, n)
#             st.markdown(f"## Monthly Payment")
#             st.markdown(f"Principal and interest: ${pi_payment:.2f}")
#             st.markdown(f"Monthly tax escrow: ${t / 12:.2f}")
#             st.markdown(f"Monthly insurance escrow: ${i / 12:.2f}")
#             st.markdown(f"Total monthly payment: ${pi_payment + (t / 12) + (i / 12):.2f}")
#             am_table = amortization(p, r, n)
#
#         except ValueError:
#             st.error("Please enter valid numeric values for all fields.")
#
#         display_amortization = st.checkbox("Display Amortization")
#         if display_amortization:
#             st.write(am_table)

with tab1:
    st.write("Mortgage Payment Calculator")

    # Get raw string inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        p_input = st.text_input("Principal amount of loan")
    with col2:
        r_input = st.text_input("Interest rate (annual)")
    with col3:
        n_input = st.text_input("Term of loan (in months)")
    col4, col5, col6 = st.columns(3)
    with col4:
        t_input = st.text_input("Annual taxes", value="0")
    with col5:
        i_input = st.text_input("Annual insurance", value="0")

    if st.button("Calculate Payment"):
        try:
            p = float(p_input)
            r = float(r_input)
            n = int(n_input)
            t = float(t_input)
            i = float(i_input)

            pi_payment = calculate_payment(p, r, n)
            am_table = amortization(p, r, n)

            # Store results in session state
            st.session_state['pi_payment'] = pi_payment
            st.session_state['t'] = t
            st.session_state['i'] = i
            st.session_state['am_table'] = am_table
            st.session_state['payment_calculated'] = True

        except ValueError:
            st.error("Please enter valid numeric values for all fields.")
            st.session_state['payment_calculated'] = False

    # Display results if calculated
    if st.session_state.get('payment_calculated'):
        st.markdown(f"## Monthly Payment")
        st.markdown(f"Principal and interest: ${st.session_state['pi_payment']:.2f}")
        st.markdown(f"Monthly tax escrow: ${st.session_state['t'] / 12:.2f}")
        st.markdown(f"Monthly insurance escrow: ${st.session_state['i'] / 12:.2f}")
        st.markdown(f"Total monthly payment: ${st.session_state['pi_payment'] + (st.session_state['t'] / 12) + (st.session_state['i'] / 12):.2f}")

        display_amortization = st.checkbox("Display Amortization")
        if display_amortization:
            df = pd.DataFrame(st.session_state['am_table'], columns=["Month",
                "Payment", "Interest", "Principal", "Balance"])
            df = df.reset_index(drop=True)  # <- This hides the default index

            df.index = [""] * len(df)
            st.dataframe(
                df.style.format({
                    "Payment": "${:,.2f}",
                    "Interest": "${:,.2f}",
                    "Principal": "${:,.2f}",
                    "Balance": "${:,.2f}"
                })
            )




# Mortgage Payoff Calculator
with tab2:
    st.write("Mortgage Payoff Calculator")

    col1, col2 = st.columns(2)
    with col1:
        principal_balance = st.text_input("Principal balance", value="0")
        p = float(principal_balance)
    with col2:
        principal_as_of_date = st.date_input("As of", key="dt1")
    col3, col4 = st.columns(2)
    with col3:
        interest_rate = st.text_input("Interest rate", value="0")
        n = float(interest_rate)
    with col4:
        good_through_date = st.date_input("Good through", key="dt2")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        accrual_basis = st.selectbox("Accrual Basis", [365, 366, 360])
    if st.button("Calculate Payoff"):
        payoff = calculate_mortgage_payoff(p, n, principal_as_of_date,
                                           good_through_date, accrual_basis)
        number_of_days = (good_through_date - principal_as_of_date).days
        per_diem = payoff[1]
        total_payoff = payoff[0]
        total_interest = per_diem * number_of_days
        st.write(f"###### \${float(principal_balance):,.2f} \+"
                 f" {number_of_days} days interest at \${per_diem} per day ("
                 f"\${total_interest:.2f})")
        st.write(f"#### Total Payoff: ${total_payoff:,.2f}")

# Property Tax Estimator
with tab3:
    col1, col2, col3 = st.columns(3)
    with col1:
        assessed_value = st.text_input("Assessed Value", value="0")
        assessed_value = float(assessed_value)
    col4, col5, col6 = st.columns(3)
    # with col4:
    #     with open("tax_rates.json", "r") as file:
    #         counties = json.load(file)
    #     county_select = st.selectbox("County", [county for county in counties])
    #     city = st.checkbox("City")
    #     if city:
    #         city_select = st.selectbox("City", [city for city in counties[
    #             county_select]["cities"]])
    with col4:
        with open("tax_rates.json", "r") as file:
            counties = json.load(file)
        county_select = st.selectbox("County", [county for county in counties])
        city = st.checkbox("City")
        if city:
            city_select = st.selectbox("City", [city for city in
                counties[county_select]["cities"]])
        else:
            # Spacer to align with city_millage_rate in col5
            st.markdown("<div style='height: 38px'></div>",
                        unsafe_allow_html=True)

    with col5:
        default_county_rate = counties[county_select]["county"]
        county_millage_rate = st.text_input("County Millage Rate",
                                            value=default_county_rate)
        county_millage_rate = float(county_millage_rate)
        if city:
            st.markdown("<div style='height: 38px'></div>",
                        unsafe_allow_html=True)
            default_city_rate = counties[county_select]["cities"][city_select]
            city_millage_rate = st.text_input("City Millage Rate",
                                              value=default_city_rate)
            city_millage_rate = float(city_millage_rate)
            combined = st.checkbox("Combine County and City Tax")

    col7, col8, col9 = st.columns(3)
    with col7:
        fees = st.text_input("Fees", value="0")
        fees = float(fees)
    if st.button("Estimate Property Tax"):
        county_tax = calculate_property_tax(assessed_value,
                                            county_millage_rate, fees)
        if city:
            city_tax = calculate_property_tax(assessed_value,
                                             city_millage_rate,
                                       0)
            if combined:
                st.write(f"Property Tax Estimate: ${county_tax + city_tax:,.2f}")
            else:
                st.write(f"City Property Tax Estimate: ${city_tax:,.2f}")
                st.write(f"County Property Tax Estimate: ${county_tax:,.2f}")
        else:
            st.write(f"Property Tax Estimate: ${county_tax:,.2f}")

# Closing Cost (Title) Estimator
with tab4:
    col1, col2, col3 = st.columns(3)
    with col1:
        purchase_price = st.text_input("Purchase Price", value="0")
        purchase_price = float(purchase_price)
    with col2:
        loan_amount = st.text_input("Loan Amount", value="0")
        loan_amount = float(loan_amount)
    with col3:
        number_of_endorsements = st.text_input("Number of endorsements",
                                               value="0")
        number_of_endorsements = int(number_of_endorsements)
    col4, col5, col6 = st.columns(3)
    with col4:
        settlement_fee = st.text_input("Settlement Fee", value="865")
        settlement_fee = float(settlement_fee)
    with col5:
        title_search = st.text_input("Title Search", value="225")
        title_search = float(title_search)
    with col6:
        courier_wire = st.text_input("Courier/Wire", value="95")
        courier_wire = float(courier_wire)
    col7, col8, col9 = st.columns(3)
    with col7:
        if loan_amount and purchase_price:
            recording_fee = 90
            e_recording_fee = 10
        elif purchase_price:
            recording_fee = 26
            e_recording_fee = 5
        else:
            recording_fee = 64
            e_recording_fee = 5

    if st.button("Estimate Title Closing Costs"):
        title_insurance = estimate_title_insurance(purchase_price,
                                                   loan_amount,
                                                   number_of_endorsements)
        total_closing_costs = settlement_fee + title_search + courier_wire \
                              + recording_fee + e_recording_fee + title_insurance

        st.write(f"Purchase price: ${purchase_price:,.2f}")
        st.write(f"Loan Amount: ${loan_amount:,.2f}")
        st.write(f"Settlement Fee: ${settlement_fee:,.2f}")
        st.write(f"Title Search: ${title_search:,.2f}")
        st.write(f"Courier Wire: ${courier_wire:,.2f}")
        st.write(f"Title Insurance: ${title_insurance:,.2f}")
        st.write(f"Recording Fee: ${recording_fee:,.2f}")
        st.write(f"E-Recording Fee: ${e_recording_fee:,.2f}")

        st.write(f"#### Total Title Closing Costs: ${total_closing_costs:,.2f}")

        st.caption("Default Assumes: CPL only on loans, recording one deed on "
                   "cash transactions, recording one deed and one deed of "
                   "trust on financed transactions, 8.1 and 9 endorsements on "
                   "loan policies.")
