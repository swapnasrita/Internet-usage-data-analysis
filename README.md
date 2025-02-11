# Internet-usage-data-analysis

Analyzing global internet patterns
📖 Background
We explore a dataset that highlights internet usage for different countries from 2000 to 2023. By conducting a thorough analysis, we dive deeper into how internet usage has changed over time and the countries still widely impacted by lack of internet availability. Apart from the internet usage, I also look at world population and GDP data from World In Data.

💾 Data
Interet Usage (internet_usage.csv)
Column name	Description
Country Name	Name of the country
Country Code	Countries 3 character country code
2000	Contains the % of population of individuals using the internet in 2000
2001	Contains the % of population of individuals using the internet in 2001
2002	Contains the % of population of individuals using the internet in 2002
2003	Contains the % of population of individuals using the internet in 2003
....	...
2023	Contains the % of population of individuals using the internet in 2023
Steps performed before data analysis
I used Power BI to perform all the steps of data analysis.

Cleaning the data: Replacing non-numeric value (e.g. '..') by null.
Determining type of data: Ensuring that all the internet usage data was identified as numeric.
Merging the data based on the key 'Country Code' to add world population and GDP in 2022 to the internet usage data. Using 'Country Code' helped ensure that we were not losing important data based on 'Country Names'. There can be debates about how the country is named or if the country has been renamed. So, country code was helpful in maintaining the connection.
Data Analysis
Early vs Late adopters
Find first year when adoption reached a threshold: I chose the threshold to be 20%. Any internet usage below 20% is low penetration and any usage higher than 90% is high penetration. So, I filtered the internet usage column to be above 20%. Then refiltered for each country to pick the minimum year. = Table.Group(#"Filtered Rows1", {"Country Name"}, {{"First Adoption Year", each List.Min([Year]), type nullable number}})
Adding Rank to the Countries
Ranking the countries according to adoption year helped sort out the countries later according to continent. = Table.AddIndexColumn(#"Sorted Rows", "Index", 1, 1, Int64.Type)
Penetration per Continent
Combining Step 1 and 2, we can plot the first adoption years for each country in a particular continent, giving us an overall view of which continent was an early adopter and which continents lagged.
Global Internet Usage
Taking average of internet usage through the years help us look at the exponential growth in internet usage globally.
YOY change
Create two measures: Previous year usage and this year usage.
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

This helps us look at the adoption in the early years vs now.

Factors influencing internet usage
(This might be my favorite part) I wondered if GDP and population might be reasons why internet usage was low in certain countries. 6. Plotting population versus internet usage and GDP versus internet usage gives us an idea on how correlated these factors are.

Suggestions by Author
Governments and global organizations should focus on targeted investments in underdeveloped regions, particularly in rural areas, to bridge the digital divide.
Tech companies should shift focus to emerging markets where adoption potential is still high, offering affordable solutions like low-cost mobile data and public Wi-Fi.
Countries with lower GDPs can adopt innovative models like public-private partnerships and international funding to prioritize digital infrastructure, accelerating adoption.
Focus on inclusive policies like free or subsidized internet access for underserved populations, particularly in regions with high population densities but low penetration rates.
🧾 Executive summary
GDP significantly influences internet adoption. High-GDP countries invest more in digital infrastructure and accessibility, leading to higher penetration rates. In contrast, low-GDP nations struggle with affordability and infrastructure challenges, slowing adoption rates.

Fluctuations in YoY growth were notable during earlier periods, particularly before 2010, indicating phases of rapid adoption.

After 2015, YoY changes stabilized across most regions, likely due to market saturation in developed nations and steady growth in emerging markets.

All countries shows a clear trajectory of steady internet adoption.
