# Internet-usage-data-analysis

📊 Analyzing Global Internet Patterns

📖 Background
This project explores a dataset that highlights internet usage across different countries from 2000 to 2023. By conducting a thorough analysis, we examine internet adoption trends over time and identify countries still struggling with low penetration. Additionally, we incorporate world population and GDP data from World In Data to assess key influencing factors.

💾 Data Sources
📌 Internet Usage Data (internet_usage.csv)

Column Name	Description
Country Name	Name of the country
Country Code	Three-character country code
2000-2023	Percentage of the population using the internet in each year

Additional data was merged from World In Data to include:

Population (2022)

GDP per capita (2022)

🛠️ Data Preparation

The analysis was performed entirely in Power BI, following these preprocessing steps:

Data Cleaning:

Replaced non-numeric values ('..') with null values.
Ensured that all internet usage data was correctly typed as numeric.

Merging External Data:

Used Country Code as a key identifier to merge population and GDP data.

This approach ensured accuracy, preventing mismatches due to country name variations.

📊 Data Analysis & Key Insights

1️⃣ Early vs. Late Adopters

First Adoption Year Calculation (Threshold: 20% Internet Usage)

Countries were classified based on when they first surpassed 20% penetration.
Countries exceeding 90% penetration were considered high adopters.

DAX Query (Power BI)


First Adoption Year = 
    Table.Group(#"Filtered Rows1", {"Country Name"}, 
    {{"First Adoption Year", each List.Min([Year]), type nullable number}})
    
Ranking Countries by Adoption Year

Countries were ranked by adoption year for better sorting and visualization.


Adoption Rank = 
    Table.AddIndexColumn(#"Sorted Rows", "Index", 1, 1, Int64.Type)
    
2️⃣ Internet Penetration per Continent

By combining First Adoption Year and Rankings, we visualized internet penetration trends for each continent, showing:

✅ Early Adopters: North America & Europe

❌ Late Adopters: Africa & South Asia

3️⃣ Global Internet Usage Trends

Taking the average internet usage per year reveals exponential growth globally.
Some countries rapidly progressed, while others lagged due to economic or policy constraints.

4️⃣ Year-over-Year (YoY) Change in Internet Adoption

To analyze annual growth trends, we calculated YoY change for each country:

DAX

YoY_Change = 
VAR PrevYearUsage = 
    CALCULATE(
        SUM(internet_usage[Internet Usage]),
        internet_usage[Year] = MAX(internet_usage[Year]) - 1,
        ALLEXCEPT(internet_usage, internet_usage[Country Name])
    )

VAR CurrentYearUsage = 
    SUM(internet_usage[Internet Usage])

RETURN 
    IF(
        NOT(ISBLANK(PrevYearUsage)), 
        (CurrentYearUsage - PrevYearUsage) / PrevYearUsage * 100, 
        BLANK()
    )
    
✅ Key Findings:

Pre-2010: High YoY fluctuations, indicating rapid adoption in some regions.
Post-2015: Stabilized growth, suggesting market saturation in developed economies.

5️⃣ Factors Influencing Internet Usage

📌 GDP vs. Internet Usage

Strong correlation observed: Higher GDP leads to greater internet penetration.
Developed nations invest more in digital infrastructure, making the internet more accessible.

📌 Population vs. Internet Usage

Surprisingly weak correlation!
Some high-population countries (e.g., India) still have low penetration.
Other small nations have nearly 100% connectivity.

📢 Suggestions & Recommendations

1️⃣ Bridging the Digital Divide

Governments should invest in rural connectivity projects, particularly in Africa & South Asia.
Focus on affordable mobile data solutions and public Wi-Fi in underserved areas.

2️⃣ Encouraging Market Expansion

Tech companies should prioritize emerging markets, where adoption potential remains high.
Low-cost internet plans and 5G expansion can accelerate connectivity.

3️⃣ Leveraging Public-Private Partnerships

Countries with lower GDP can adopt PPP models to improve infrastructure.
International funding & investments in broadband expansion can help boost connectivity.

4️⃣ Inclusive Digital Policies

Implement subsidized internet plans for low-income populations.
Provide digital literacy programs to encourage effective internet usage.

📌 Executive Summary

Global internet penetration is 71.29%, with ~2.3 billion people still unconnected.

GDP strongly influences adoption, but population size alone does not.

Internet usage saw rapid early growth, stabilizing post-2015.

Developed countries adopted the internet earlier, while low-GDP nations face infrastructure challenges.

Strategic investments in infrastructure, affordability, and digital literacy can accelerate global adoption.

📁 Repository Structure

📂 Global-Internet-Analysis
│── 📄 README.md   # Project documentation
│── 📊 internet_usage.csv  # Internet penetration dataset
│── 📊 world_population.csv  # Population dataset
│── 📊 gdp_data.csv  # GDP dataset
│── 📜 data_analysis.pbix  # Power BI file (too big! Email me directly for file.)
│── 📜 report.ipynb  # Jupyter Notebook with additional insights
│── 📂 visualizations
│   ├── adoption_trends.png
│   ├── global_usage.png
│   ├── yoy_change.png
│── 📜 LICENSE

📌 Future Work

Expand analysis to mobile vs broadband penetration.
Predict future internet penetration rates using machine learning.
Compare government policies vs internet growth rates.

🙌 Acknowledgments

World In Data for GDP & Population Data.
Power BI & Jupyter Notebook for data analysis & visualization.
