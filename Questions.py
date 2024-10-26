import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import json
import re
from app import Pages_switch


Pages_switch()

genai.configure(api_key='')  # add api key 

st.title("Personalized Investment Portfolio Builder")

# Create tabs for different sections of the questionnaire
tabs = st.tabs(["Personal Information", "Financial Details", "Investments", "Risk Profile", "Submit"])

# Personal Information Tab
with tabs[0]:
    st.header("Personal Information")
    age = st.selectbox("Enter your age:", list(range(1, 100)))
    currency = st.text_input("Enter the name of your currency (e.g., USD, INR):", value="")
    income = st.text_input("Enter your income per annum:", value="0")
    monthly_expenses = st.text_input("Enter your monthly expenditure:", value="0")

# Financial Details Tab
with tabs[1]:
    st.header("Financial Details")
    savings_goal = st.text_input("Enter the amount of money you want to save:", value="0")
    current_savings = st.text_input("Enter your current savings amount:", value="0")
    total_debts = st.text_input("Enter your total outstanding debts:", value="0")
    monthly_debt_payments = st.text_input("Enter your monthly payments toward these debts:", value="")
    
    # Emergency Fund
    emergency_fund = st.selectbox("Do you have an emergency fund?", ['yes', 'no'])
    if emergency_fund == 'yes':
        emergency_fund_months = st.text_input("How many months of expenses does your emergency fund cover?", value="0")

# Investments Tab
with tabs[2]:
    st.header("Investments")
    investment_amount = st.text_input("Enter the amount already invested:", value="0")
    investment_type = st.text_input("Enter the types of investments made (e.g., stocks, bonds, crypto):", value="")
    expected_returns = st.text_input("Enter the expected return rate of your investments (e.g., 7 for 7%):", value="0.0")
    time_horizon = st.text_input("Enter your investment period in years:", value="1")

# Risk Profile Tab
with tabs[3]:
    st.header("Risk Profile")
    risk_tolerance = st.selectbox("What is your risk tolerance?", ['low', 'medium', 'high'])
    investment_style = st.selectbox("What is your investment style?", ['conservative', 'balanced', 'aggressive'])
    investment_preferences = st.text_input("Do you prefer specific asset classes? (e.g., stocks, bonds, real estate, crypto):", value="")
    financial_goals = st.text_input("List your financial goals (e.g., retirement, buying a home, children's education):", value="")
    target_amounts = st.text_input("Enter target amounts for each financial goal, separated by commas:", value="")

# Submit Tab
with tabs[4]:
    if st.button("Submit Profile"):
        with st.spinner("Processing your profile..."):
            try:
                income = float(income)
                monthly_expenses = float(monthly_expenses)
                savings_goal = float(savings_goal)
                current_savings = float(current_savings)
                time_horizon = int(time_horizon)
                age = int(age)
                investment_amount = float(investment_amount)
                expected_returns = float(expected_returns)
                total_debts = float(total_debts)
                monthly_debt_payments = float(monthly_debt_payments)

                # Add prompt here 
                prompt = (
                    f"My annual income is {income} {currency}, with a monthly expense of {monthly_expenses} {currency}. "
                    f"My savings goal is {savings_goal} {currency}, and I currently have {current_savings} saved. "
                    f"I have already invested {investment_amount} in {investment_type}, aiming for an expected return of {expected_returns}%. "
                    f"My age is {age}, and my investment horizon is {time_horizon} years. "
                    f"My risk tolerance is {risk_tolerance}, with an investment style of {investment_style}. "
                    f"I prefer investments in {investment_preferences}. "
                    f"My financial goals include {financial_goals}, with targets of {target_amounts}. "
                    f"My total debt is {total_debts}, and I pay {monthly_debt_payments} monthly towards it. "
                )

                if emergency_fund == 'yes':
                    emergency_fund_months = float(emergency_fund_months)
                    prompt += f"I also have an emergency fund that covers {emergency_fund_months} months of expenses. "

                prompt += (
                    "Please provide a breakdown of how much I should allocate to Stocks, Bonds, and Crypto, "
                    "as well as a savings and debt management strategy. "
                    "Return the output in JSON format with fields for 'Stocks', 'Bonds', 'Crypto', 'Savings Strategy', "
                    "'Debt Management', and 'Emergency Fund Allocation'."
                )

                # Call Gemini Flash API
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(prompt)
                
                # Access response text directly
                ai_response = response.text  # Use the 'text' attribute directly

                # Display Gemini's response on a new page
                st.session_state.response = ai_response  # Store the response in session state
                st.session_state.show_results = True  # Flag to show results page

                st.experimental_rerun()

            except ValueError as ve:
                st.error(f"Input error: {ve}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
