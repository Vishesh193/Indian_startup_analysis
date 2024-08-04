 Startup Funding Dashboard

An interactive dashboard built with Streamlit to analyze startup funding data. This project provides insights into investment trends, startup performance, and investor activities through various visualizations.

Features

- **Overall Analysis**: 
  - Key metrics on total investments, maximum funding, average ticket size, and number of funded startups.
  - Month-over-Month investment trends.
  - Top sectors and types of funding with visual representations.
  - City-wise funding analysis and heatmaps.

- **Startup Analysis**:
  - Detailed view of individual startups including company details, investment trends, and similar companies based on selected criteria.

- **Investor Analysis**:
  - Insights into investor activities including recent investments, biggest investments, and sectors invested in.
  - Analysis of similar investors based on investment patterns.

**Requirements**

- Python 3.x
- Streamlit
- Pandas
- Matplotlib
- Seaborn

**Installation**

1. Clone the repository:
   git clone https://github.com/Vishesh193/startup-funding-dashboard.git
   
2. Navigate to the project directory:
   cd startup-funding-dashboard
3. Install the required packages:
   pip install -r requirements.txt

**Usage**
1. Place your cleaned startup data in a file named `startup_cleaned.csv`.
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open the provided local URL in your browser to interact with the dashboard.

**Contributing**

Feel free to open issues or submit pull requests to enhance the dashboard's functionality.

**License**

This project is unlicensed.
