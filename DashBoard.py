import streamlit as st 
from app import Pages_switch
import json
import re
import matplotlib.pyplot as plt

Pages_switch()

st.title("Dashboard")

if 'response' in st.session_state:
    try:
        # Extract JSON part of response using regex
        json_text_match = re.search(r'\{.*\}', st.session_state.response, re.DOTALL)
        if json_text_match:
            # Extracted JSON string
            json_text = json_text_match.group(0)

            # Remove any percentage symbols and load JSON
            cleaned_response = re.sub(r'(\d+)%', r'\1', json_text)
            response_data = json.loads(cleaned_response)

            # Extract allocation percentages as floats
            allocation = {
                "Stocks": float(response_data.get("Stocks", 0)),
                "Bonds": float(response_data.get("Bonds", 0)),
                "Crypto": float(response_data.get("Crypto", 0))
            }

            # Display allocations as a pie chart
            labels = allocation.keys()
            sizes = allocation.values()
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

            # Display other details
            st.write("Savings Strategy:", response_data.get("Savings Strategy", "Not specified"))
            st.write("Debt Management:", response_data.get("Debt Management", "Not specified"))
            st.write("Emergency Fund Allocation:", response_data.get("Emergency Fund Allocation", "Not specified"))
        else:
            st.error("Could not extract JSON data. Please check the response format.")
    except json.JSONDecodeError:
        st.error("Error decoding JSON response. Please check the output format.")
    except Exception as e:
        st.error(f"An error occurred while processing the response: {e}")
else:
    st.write("Please complete the profile submission on the Questions page first.")
