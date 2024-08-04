import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up page configuration
st.set_page_config(layout="wide", page_title='Startup Dashboard')

# Load and prepare data
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Initialize session state for option if it does not exist
if 'option' not in st.session_state:
    st.session_state.option = 'Overall Analysis'

# Sidebar for selection
st.sidebar.title("Navigation")
st.session_state.option = st.sidebar.selectbox('Select One',
    ['Overall Analysis', 'Startup', 'Investor'], key='analysis')
option = st.session_state.option

def load_overall_analysis():
    st.title('Overall Analysis')

    # Total invested amount
    total = round(df['amount'].sum())
    # Max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # Avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # Total funded startups
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total Investment', f'{total} Cr')
    with col2:
        st.metric('Max Investment in a Startup', f'{max_funding} Cr')
    with col3:
        st.metric('Average Ticket Size', f'{round(avg_funding)} Cr')
    with col4:
        st.metric('Total Funded Startups', num_startups)

    st.markdown("---")

    # Additional Metrics
    st.header('Additional Metrics')

    verticals = df['vertical'].nunique() if 'vertical' in df.columns else 'N/A'
    subverticals = df['subvertical'].nunique() if 'subvertical' in df.columns else 'N/A'
    cities = df['city'].nunique() if 'city' in df.columns else 'N/A'
    rounds = df['round'].nunique() if 'round' in df.columns else 'N/A'
    investors = df['investors'].nunique() if 'investors' in df.columns else 'N/A'
    dates = df['date'].nunique() if 'date' in df.columns else 'N/A'

    col5, col6, col7, col8, col9, col10 = st.columns(6)

    with col5:
        st.metric('Unique Verticals', verticals)
    with col6:
        st.metric('Unique Subverticals', subverticals)
    with col7:
        st.metric('Unique Cities', cities)
    with col8:
        st.metric('Unique Funding Rounds', rounds)
    with col9:
        st.metric('Unique Investors', investors)
    with col10:
        st.metric('Unique Dates', dates)

    st.markdown("---")

    # Month-over-Month Graph
    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots(figsize=(15, 6))
    ax3.plot(temp_df['x_axis'], temp_df['amount'], marker='o', linestyle='-')
    plt.xticks(rotation=90, ha='right')
    plt.tight_layout()

    st.pyplot(fig3)

    st.markdown("---")

    # Top Startups and Top Investors
    st.header('Top Startups and Investors')
    top_startups = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
    top_investors = df['investors'].str.split(',', expand=True).stack().value_counts().head(10)

    fig_top_startups, ax_top_startups = plt.subplots(figsize=(12, 8))
    top_startups.plot(kind='bar', ax=ax_top_startups, color='skyblue')
    ax_top_startups.set_title('Top Startups by Investment Amount')
    ax_top_startups.set_xlabel('Startup')
    ax_top_startups.set_ylabel('Amount')
    plt.xticks(rotation=45)
    st.pyplot(fig_top_startups)

    fig_top_investors, ax_top_investors = plt.subplots(figsize=(12, 8))
    top_investors.plot(kind='bar', ax=ax_top_investors, color='coral')
    ax_top_investors.set_title('Top Investors by Count')
    ax_top_investors.set_xlabel('Investor')
    ax_top_investors.set_ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(fig_top_investors)

    st.markdown("---")

    # Funding Heatmap
    st.header('Funding Heatmap')
    heatmap_data = df.groupby(['year', 'month'])['amount'].sum().unstack()
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', ax=ax_heatmap)
    ax_heatmap.set_title('Funding Heatmap')
    st.pyplot(fig_heatmap)

def load_startup_analysis(startup):
    st.title(f'Analysis for {startup}')

    # Filter data for the selected startup
    startup_data = df[df['startup'] == startup]

    if startup_data.empty:
        st.write("No data available for this startup.")
        return

    st.subheader('Company POV')
    st.write(f"**Name:** {startup}")
    st.write(f"**Founders:** {startup_data['founders'].iloc[0] if 'founders' in startup_data.columns else 'N/A'}")
    st.write(f"**Industry:** {startup_data['vertical'].iloc[0] if 'vertical' in startup_data.columns else 'N/A'}")
    st.write(f"**Subindustry:** {startup_data['subvertical'].iloc[0] if 'subvertical' in startup_data.columns else 'N/A'}")
    st.write(f"**Location:** {startup_data['city'].iloc[0] if 'city' in startup_data.columns else 'N/A'}")
    st.write(f"**Funding Rounds:** {startup_data['round'].nunique() if 'round' in startup_data.columns else 'N/A'}")
    st.write(f"**Stage:** {startup_data['stage'].iloc[0] if 'stage' in startup_data.columns else 'N/A'}")
    st.write(f"**Investors:** {startup_data['investors'].iloc[0] if 'investors' in startup_data.columns else 'N/A'}")
    st.write(f"**Date:** {startup_data['date'].iloc[0] if 'date' in startup_data.columns else 'N/A'}")

    st.markdown("---")

    # Investment Trend
    st.header('Investment Trend')
    investment_trend = startup_data.groupby('date')['amount'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(investment_trend['date'], investment_trend['amount'], marker='o', linestyle='-')
    ax1.set_title(f'Investment Trend for {startup}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Amount (in Cr)')
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    st.markdown("---")

    # Similar Companies
    st.header('Similar Companies')
    st.write("Select a criterion to find similar companies to this startup.")

    criterion = st.selectbox('Select Criterion', ['Vertical', 'Subvertical', 'City', 'Amount'])

    if criterion == 'Vertical':
        selected_vertical = startup_data['vertical'].iloc[0] if 'vertical' in startup_data.columns else 'N/A'
        similar_companies = df[df['vertical'] == selected_vertical]
    elif criterion == 'Subvertical':
        selected_subvertical = startup_data['subvertical'].iloc[0] if 'subvertical' in startup_data.columns else 'N/A'
        similar_companies = df[df['subvertical'] == selected_subvertical]
    elif criterion == 'City':
        selected_city = startup_data['city'].iloc[0] if 'city' in startup_data.columns else 'N/A'
        similar_companies = df[df['city'] == selected_city]
    elif criterion == 'Amount':
        selected_amount_range = st.slider('Select Amount Range (in Cr)', min_value=0, max_value=int(df['amount'].max()), value=(0, int(df['amount'].max())))
        similar_companies = df[(df['amount'] >= selected_amount_range[0]) & (df['amount'] <= selected_amount_range[1])]

    st.dataframe(similar_companies)

def load_investor_details(investor):
    st.title(f'Analysis for {investor}')

    # Load the recent five investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'amount']]
    st.write(f"**Recent Investments by {investor}:**")
    st.dataframe(last5_df)

    st.markdown("---")

    # Load the top five investments by amount
    top5_investments = df[df['investors'].str.contains(investor)].sort_values(by='amount', ascending=False).head(5)
    fig_top5, ax_top5 = plt.subplots(figsize=(12, 6))
    sns.barplot(x='startup', y='amount', data=top5_investments, ax=ax_top5, palette='viridis')
    ax_top5.set_title(f'Top 5 Investments by {investor}')
    ax_top5.set_xlabel('Startup')
    ax_top5.set_ylabel('Amount (in Cr)')
    plt.xticks(rotation=45)
    st.pyplot(fig_top5)

    st.markdown("---")

    # Sectors Invested In
    st.header('Sectors Invested In')
    sector_invested = df[df['investors'].str.contains(investor)]['vertical'].value_counts()
    fig_sectors, ax_sectors = plt.subplots(figsize=(12, 6))
    sector_invested.plot(kind='pie', ax=ax_sectors, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    ax_sectors.set_title(f'Sectors Invested In by {investor}')
    st.pyplot(fig_sectors)

    st.markdown("---")

    # Funding Rounds
    st.header('Funding Rounds')
    funding_rounds = df[df['investors'].str.contains(investor)]['round'].value_counts()
    fig_rounds, ax_rounds = plt.subplots(figsize=(12, 6))
    funding_rounds.plot(kind='pie', ax=ax_rounds, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    ax_rounds.set_title(f'Funding Rounds Participated by {investor}')
    st.pyplot(fig_rounds)

    st.markdown("---")

    # Cities Invested In
    st.header('Cities Invested In')
    cities_invested = df[df['investors'].str.contains(investor)]['city'].value_counts()
    fig_cities, ax_cities = plt.subplots(figsize=(12, 6))
    cities_invested.plot(kind='pie', ax=ax_cities, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    ax_cities.set_title(f'Cities Invested In by {investor}')
    st.pyplot(fig_cities)

    st.markdown("---")

    # YOY Investment
    st.header('YOY Investment')
    yoy_investment = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum().reset_index()
    fig_yoy, ax_yoy = plt.subplots(figsize=(12, 6))
    ax_yoy.plot(yoy_investment['year'], yoy_investment['amount'], marker='o', linestyle='-')
    ax_yoy.set_title(f'Yearly Investment Trend for {investor}')
    ax_yoy.set_xlabel('Year')
    ax_yoy.set_ylabel('Amount (in Cr)')
    st.pyplot(fig_yoy)

    st.markdown("---")

    # Similar Investors
    st.header('Similar Investors')
    st.write("Showing top 5 similar investors based on investment patterns.")

    similar_investors = df[df['investors'].str.contains(investor)]['investors'].str.split(',', expand=True).stack().value_counts().head(5)
    fig_similar, ax_similar = plt.subplots(figsize=(12, 6))
    similar_investors.plot(kind='bar', ax=ax_similar, color='teal')
    ax_similar.set_title(f'Top 5 Similar Investors')
    ax_similar.set_xlabel('Investor')
    ax_similar.set_ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(fig_similar)

# Load the content based on the selected option
if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Startup':
    startups = df['startup'].unique()
    selected_startup = st.selectbox('Select Startup', startups)
    load_startup_analysis(selected_startup)
elif option == 'Investor':
    investors = df['investors'].str.split(',', expand=True).stack().unique()
    selected_investor = st.selectbox('Select Investor', investors)
    load_investor_details(selected_investor)
