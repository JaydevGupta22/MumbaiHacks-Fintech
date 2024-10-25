API_KEY = 'AIzaSyCDLa7tmVYMJoUitAikkO_KfGKqJHPG-8U'

import google.generativeai as genai
import os

genai.configure(api_key= API_KEY)

income = int(input('enter your income per annum :'))
currency = input('enter the name of your currency :')
saving_goals = int(input('enter the amount of money you want to save :'))
time_horizon = int(input('enter the period of investment in years :'))
age = input('enter your age :')
amount = input('enter your monthly expenditure :')
investment_amount = int(input('enter the amount already invested :'))
investment_type = input('enter the type of investment made :')

prompt = f'My income is {income} {currency} per anum. My saving goals are to save {saving_goals} {currency}. My time horizon for investment is {time_horizon} years. My age is {age}.I spend {amount} {currency} per month.I have already invested {investment_amount} in {investment_type}.Give me a split on how much should i invest on Stocks , Bonds and Crypto. Give me the output in the form of a JSON file.'

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
print(response.text)

