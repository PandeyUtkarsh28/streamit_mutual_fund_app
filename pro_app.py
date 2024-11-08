import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_chat import message

# Page Configurations
st.set_page_config(page_title="Mutual Funds Distributor", page_icon=':chart_with_upwards_trend:', layout="centered")

# Sample data: Replace with real mutual fund data
mutual_fund_data = pd.DataFrame({
    'Fund Name': ['Hdfc', 'Tata Elexi', 'Adani Port', 'Hal'],
    'Category': ['Equity', 'Debt', 'Hybrid', 'Equity'],
    '1-Year Return (%)': [12.5, 7.0, 9.5, 15.2],
    '3-Year Return (%)': [10.2, 6.5, 8.1, 14.0],
    '5-Year Return (%)': [11.1, 6.0, 7.8, 13.5]
})

# Custom CSS for styling
st.markdown("""
    <style>
        /* Background color for the main app */
        .stApp { background-color: #0C0909; } /* Light beige */
        
        /* Section styling */
        .section { background-color: #fff7e6; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        
        /* Titles and button styling */
        .main-title { font-size: 2.5em; font-weight: bold; color: #2c3e50; text-align: center; margin-bottom: 20px; }
        .subsection-title { font-size: 1.8em; color: #333; margin-top: 30px; }
        .sidebar-header { font-size: 1.4em; font-weight: bold; color: #4A90E2; }
        .stButton>button { background-color: #4A90E2; color: white; border-radius: 10px; }
        .stNumberInput>input { background-color: #e8f4ff; border-radius: 10px; }
        
        /* Styling for Projected Return result */
        .projected-return { font-size: 1.5em; font-weight: bold; color: #FF5733; }
        
        /* Styling for specific text */
        .custom-label { color: #2c3e50; font-weight: bold; font-size: 1.1em; }
        .investment-label { color: #FF5733; font-weight: bold; font-size: 1.1em; }
    </style>
""", unsafe_allow_html=True)

# Sidebar for Page Navigation
page = st.sidebar.selectbox("Navigate", ["Mutual Funds Distributor", "Customer Details"])

if page == "Mutual Funds Distributor":
    # Mutual Funds Page
    st.markdown('<h1 class="main-title">📊 Mutual Funds Distributor</h1>', unsafe_allow_html=True)
    
    st.sidebar.markdown('<p class="sidebar-header">🔍 Filter Options</p>', unsafe_allow_html=True)
    selected_category = st.sidebar.selectbox("Select Category", mutual_fund_data['Category'].unique())
    min_1y_return = st.sidebar.slider("Minimum 1-Year Return (%)", min_value=0, max_value=20, value=5)
    
    # Filter data based on user input
    filtered_data = mutual_fund_data[
        (mutual_fund_data['Category'] == selected_category) & 
        (mutual_fund_data['1-Year Return (%)'] >= min_1y_return)
    ]
    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3 class="subsection-title">🔍 Filtered Mutual Funds</h3>', unsafe_allow_html=True)
    st.write(filtered_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed info on selected mutual fund
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3 class="subsection-title">📄 Selected Fund Details</h3>', unsafe_allow_html=True)
    st.markdown('<p class="custom-label">Choose a fund for details</p>', unsafe_allow_html=True)
    selected_fund = st.selectbox("", filtered_data['Fund Name'])
    fund_details = mutual_fund_data[mutual_fund_data['Fund Name'] == selected_fund]
    st.write(fund_details)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Projected Returns Calculator
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3 class="subsection-title">💰 Projected Returns Calculator</h3>', unsafe_allow_html=True)
    st.markdown('<p class="investment-label">Investment Amount (in ₹)</p>', unsafe_allow_html=True)
    investment_amount = st.number_input("", min_value=1000, step=500)
    st.markdown('<p class="investment-label">Investment Duration (years)</p>', unsafe_allow_html=True)
    selected_years = st.selectbox("", [1, 3, 5])
    
    if selected_years == 1:
        projected_return = investment_amount * (1 + fund_details['1-Year Return (%)'].values[0] / 100)
    elif selected_years == 3:
        projected_return = investment_amount * (1 + fund_details['3-Year Return (%)'].values[0] / 100)
    elif selected_years == 5:
        projected_return = investment_amount * (1 + fund_details['5-Year Return (%)'].values[0] / 100)
    
    # Display projected return with custom color
    st.markdown(f'<p class="projected-return">Projected Return after {selected_years} years: ₹{projected_return:.2f}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Customized Fund Performance Chart using Matplotlib
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3 class="subsection-title">📈 Fund Performance Chart</h3>', unsafe_allow_html=True)
    returns = fund_details[['1-Year Return (%)', '3-Year Return (%)', '5-Year Return (%)']].values.flatten()
    years = ['1-Year Return', '3-Year Return', '5-Year Return']
    
    fig, ax = plt.subplots()
    ax.plot(years, returns, marker='o', linestyle='-', color='#FF5733', linewidth=2, 
            markerfacecolor='#33FFBD', markeredgewidth=2, markeredgecolor='#FF5733')
    ax.set_title(f"{selected_fund} Fund Performance")
    ax.set_xlabel("Duration")
    ax.set_ylabel("Return (%)")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Pie Chart of Fund Categories
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3 class="subsection-title">📊 Fund Category Distribution</h3>', unsafe_allow_html=True)
    category_counts = mutual_fund_data['Category'].value_counts()
    
    fig, ax = plt.subplots()
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=['#FF5733', '#33FFBD', '#4A90E2'])
    ax.set_title("Distribution of Fund Categories")
    
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chatbot Section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3 class="subsection-title">🤖 Chatbot</h3>', unsafe_allow_html=True)
    
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    user_message = st.text_input("You: ", key="user_input")
    if user_message:
        st.session_state['messages'].append({"role": "user", "content": user_message})
        
        if "return" in user_message.lower():
            bot_message = "Our funds have historically performed well. You can use the calculator above for projected returns!"
        elif "fund" in user_message.lower():
            bot_message = "We offer various categories of funds. You can filter them on the sidebar!"
        else:
            bot_message = "I'm here to assist you with mutual fund details and projections."
    
        st.session_state['messages'].append({"role": "bot", "content": bot_message})
    
    for msg in st.session_state['messages']:
        if msg["role"] == "user":
            message(msg["content"], is_user=True)
        else:
            message(msg["content"], is_user=False)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Customer Details":
    # Customer Details Page
    st.markdown('<h1 class="main-title">📋 Customer Details</h1>', unsafe_allow_html=True)
    
    # Input fields for customer details
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3 class="subsection-title">👤 Enter Customer Information</h3>', unsafe_allow_html=True)
    name = st.text_input("Customer Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    st.markdown('<p class="investment-label">Investment Amount (₹)</p>', unsafe_allow_html=True)
    investment_amount = st.number_input("", min_value=1000, step=500)
    st.markdown('<p class="custom-label">Preferred Fund</p>', unsafe_allow_html=True)
    preferred_fund = st.selectbox("", mutual_fund_data['Fund Name'])
    
    # Button to submit details
    if st.button("Submit"):
        st.success(f"Details for {name} have been submitted!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Displaying entered information
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h3 class="subsection-title">📄 Customer Summary</h3>', unsafe_allow_html=True)
    if name and email and phone:
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Phone:** {phone}")
        st.write(f"**Investment Amount:** ₹{investment_amount}")
        st.write(f"**Preferred Fund:** {preferred_fund}")
    else:
        st.write("Please fill in all details.")
    st.markdown('</div>', unsafe_allow_html=True)
