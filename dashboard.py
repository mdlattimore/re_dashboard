import streamlit as st
import requests
from datetime import datetime as dt
from get_econ_data import get_current_inflation_rate, \
    get_current_thirty_year_conventional_mortgage_rate, \
    get_current_unemployment_rate, get_current_gas_price, \
    get_current_cost_of_eggs
from mtg_pmt_calculator import calculate_payment
from mtg_payoff_calculator import calculate_mortgage_payoff

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
def cached_get_current_cost_of_eggs():
    return get_current_cost_of_eggs()

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
    now = dt.now()
    st.write("#### Today")
    st.write(now.date().__str__())


with col2:
    inflation = cached_get_current_inflation_rate()
    st.write("#### Inflation")
    st.write(f"{inflation[0]}% ({inflation[1]})")

with col3:
    st.write("#### Conv 30 Yr Rate")
    rate = cached_get_current_thirty_year_conventional_mortgage_rate()
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
    st.write("#### Eggs")
    egg_price = cached_get_current_cost_of_eggs()
    st.write(f"${egg_price[0]} ({egg_price[1]})")

st.subheader("Calculators")

tab1, tab2, tab3 = st.tabs(["Mortgage Payment", "Mortgage Payoff",
                                  "Property Tax"])
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
            st.markdown(f"## Monthly Payment")
            st.markdown(f"Principal and interest: ${pi_payment:.2f}")
            st.markdown(f"Monthly tax escrow: ${t / 12:.2f}")
            st.markdown(f"Monthly insurance escrow: ${i / 12:.2f}")
            st.markdown(
                f"Total monthly payment: ${pi_payment + (t / 12) + (i / 12):.2f}")

        except ValueError:
            st.error("Please enter valid numeric values for all fields.")
with tab2:
    st.write("Mortgage Payoff Calculator")

    col1, col2 =st.columns(2)
    with col1:
        principal_balance = st.text_input("Principal balance", value="0")
        p = float(principal_balance)
    with col2:
        principal_as_of_date = st.date_input("As of", key="dt1")
    col3, col4 =st.columns(2)
    with col3:
        interest_rate = st.text_input("Interest rate", value="0")
        n = float(interest_rate)
    with col4:
        good_through_date = st.date_input("Good through", key="dt2")
    col5, col6, col7, col8 =st.columns(4)
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

with tab3:
    st.write("Property Tax")


