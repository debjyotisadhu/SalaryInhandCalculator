import streamlit as st, numpy as np

class inhandCalculator :
    def __init__(self, basic, allowance, er_epf, er_nps, gratuity = False):
        self.basic = basic
        self.allowance = allowance
        self.er_epf = er_epf
        self.gross_income = basic + allowance
        self.new_regime_tax_calculation(self.gross_income - er_nps)
        self.gratuity = 0.0481*basic
        self.monthly_takehome = (self.gross_income - self.total_tax - er_epf - er_nps) / 12
        self.annual_epf = er_epf
        self.annual_nps = er_nps
        self.ctc = self.gross_income + self.annual_epf + self.gratuity*gratuity


    def new_regime_tax_calculation(self, income):
        tax, cess, surcharge = 0, 0, 0

        income = max(0, income - 75000)
        self.taxable_income = income

        tax += max(0, income - 4e5)*0.05
        tax += max(0, income - 8e5)*0.05
        tax += max(0, income - 12e5)*0.05
        tax += max(0, income - 16e5)*0.05
        tax += max(0, income - 20e5)*0.05
        tax += max(0, income - 24e5)*0.05

        # marginal relief
        tax = max(min(income - 12e5, tax), 0)

        # applicable surcharges
        if (income >= 50e5) and (income <= 100e5) :
            surcharge = tax * 0.1
            surcharge = min(surcharge, income - 50e5)
        elif (income >= 100e5) :
            surcharge = tax * 0.15
            surcharge = min(surcharge, income - 100e5)

        tax += surcharge

        # include cess
        cess = tax*0.04

        # professional tax for 12 months
        prof_tax = 2400

        self.total_tax = tax + cess + prof_tax
        self.surcharge = surcharge
        self.cess = cess
        self.prof_tax = prof_tax


st.title("💰 Salary Inhand Calculator (New Tax Regime - India)")
st.header("Enter Yearly Salary Details (CTC)")

st.sidebar.info("""
Taxable Income <= 12L : 0 Tax
Marginal Relief is included.
Standard Deduction 75,000/- 
""")
annual_basic = st.number_input("Basic Salary (₹ / year)", min_value=0.0, value=500000.0, step=1000.0)
annual_allowance = st.number_input("Allowances (HRA + Other) (₹ / year)", min_value=0.0, value=200000.0, step=1000.0)
annual_epf = st.number_input("Employee EPF Contribution (₹ / year)", min_value=0.0, value=annual_basic*0.12, step=500.0)
# ON / OFF switch
feature_on = st.toggle("Enable Employer NPS Benefit (14% of Basic)")
annual_nps = 0.14*annual_basic*feature_on

feature_on = st.toggle("Add Gratuity into CTC")

st.divider()

if annual_basic + annual_allowance == 0 :
    msg = "Please put some Income to Calculate Income Tax"
    st.warning(msg)
    st.stop()

calc = inhandCalculator(annual_basic, annual_allowance, annual_epf, annual_nps, feature_on)

st.header("📊 Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("Annual CTC", f"₹ {calc.ctc:,.0f}")
    st.metric("Annual Gross Income", f"₹ {calc.gross_income:,.0f}")
    st.metric("Taxable Income", f"₹ {calc.taxable_income:,.0f}")
    st.metric("Annual Tax (incl. cess)", f"₹ {calc.total_tax:,.0f}")

with col2:
    st.metric("Monthly Take Home (approx)", f"₹ {calc.monthly_takehome:,.0f}")
    st.metric("Monthly EPF Contribution", f"₹ {calc.annual_epf*2.0/12.0:,.0f}")
    st.metric("Monthly NPS Contribution", f"₹ {calc.annual_nps/12.0:,.0f}")
    st.metric("Monthly Inhand+Retiral Benefits", f"₹ {calc.monthly_takehome + calc.annual_epf*2.0/12.0+calc.annual_nps/12.0:,.0f}")

st.info("Note: Simplified new tax regime calculation. ₹75,000/- Standard Deduction Applied. No other deductions applied. ")


