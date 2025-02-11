# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:49:44 2025

@author: P70073624
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import string
import seaborn as sns
from matplotlib.widgets import RadioButtons
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'



df = pd.read_csv('internet_usage.csv')
world_population = pd.read_csv('world_population.csv')
world_population.rename(columns = {'Country/Territory':'Country Name'}, inplace = True)
df.replace(to_replace='..', value = np.nan, inplace = True)
data = df.copy()

# Create a dictionary to store countries by their starting letter
continents = {continent: [] for continent in world_population['Continent'].unique()}
continents['Unknown'] = []
# Group columns by their starting letter
for code in df['Country Code']:
    try:
        continent = world_population.loc[world_population['CCA3'] == code, 'Continent'].values[0]
    except IndexError:
        continent = "Unknown"  # or handle it differently

    continents[continent].append(df.loc[df['Country Code'] == code, 'Country Name'].values[0])
    
continents['Europe'].append('Channel Islands')
continents['Europe'].append('Kosovo')
continents['North America'].append('Northern Mariana Islands')
continents.pop('Unknown')

country_mapping = {
    "Bahamas": "Bahamas, The",
    "Brunei":"Brunei Darussalam",
    "Cape Verde": "Cabo Verde",
    "Egypt": "Egypt, Arab Rep.",
    "Gambia": "Gambia, The",
    "Hong Kong": "Hong Kong SAR, China",
    "Iran": "Iran, Islamic Rep.",
    "Kyrgyzstan":"Kyrgyz Republic",
    "Russia": "Russian Federation",
    "Slovakia": "Slovak Republic",
    "Saint Kitts and Nevis":"St. Kitts and Nevis",
    "Saint Lucia": "St. Lucia",
    "Saint Vincent and the Grenadines": "St. Vincent and the Grenadines",
    "Syria": "Syrian Arab Republic",
    "Venezuela":"Venezuela, RB",
    "Yemen": "Yemen, Rep.",
    "Czech Republic": "Czechia",
    "DR Congo": "Congo, Dem. Rep.",
    "Ivory Coast": "Cote d'Ivoire",
    "Laos": "Lao PDR",
    "Libya": "Libya",
    "Macau": "Macao SAR, China",
    "Micronesia": "Micronesia, Fed. Sts.",
    "North Korea": "Korea, Dem. People's Rep.",
    "South Korea": "Korea, Rep.",
    "Palestine": "West Bank and Gaza",
    "Republic of the Congo": "Congo, Rep.",
    "Saint Martin": "St. Martin (French part)",
    "Sint Maarten": "Sint Maarten (Dutch part)",
    "Turkey": "Turkiye",
    "United States Virgin Islands": "Virgin Islands (U.S.)",
    "Vietnam": "Viet Nam",

    # Combining into "Channel Islands"
    "Jersey": "Channel Islands",
    "Guernsey": "Channel Islands",
    "Isle of Man": "Channel Islands",
    
    # Excluding irrelevant territories
    "Mayotte": None,
    "Niue": None,
    "Tokelau": None,
    "Wallis and Futuna": None,
    "Vatican City": None,
    "Falkland Islands": None,
    "Saint Barthelemy": None,
    "Saint Pierre and Miquelon": None,
    "Reunion": None,
}

gdp = pd.read_csv('GDP.csv', skiprows = 4)
gdp = gdp[['Country Name', 'Country Code', '2022']]
gdp['adoption'] = gdp['Country Code'].map(data.set_index('Country Code')['2022'])
gdp['Continent'] = gdp['Country Code'].map(world_population.set_index('CCA3')['Continent'])

world_population["Country Name"] = world_population["Country Name"].replace(country_mapping)
world_population = world_population.groupby("Country Name", as_index=False).mean()


#clean up dataframe
df.drop('Country Code', axis = 1, inplace=True)
df.set_index('Country Name', inplace=True)
df = df.astype('float64', errors='raise')
df= df.transpose()
df.index.names = ['Date']



#%%
###################################################
###### Region specific Internet usage evolution####
###################################################

# Initialize subplots (6 rows, 4 columns)
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

# Plot each group in the corresponding subplot

plot_index = 0
for continent, countries in continents.items():
    df_mean = df[countries].mean(axis = 1)
    axes[plot_index].plot(df_mean, color = 'k', linewidth = 2)
    if countries:  # Only plot if there are countries for this letter
        ax = axes[plot_index]
        df[countries].plot(ax=ax, legend=False, alpha = 0.2)
        ax.set_title(f'{continent}')
        plot_index += 1  # Move to the next subplot
        xticks_positions = [2000, 2023]
        ax.set_xticks([0, 23]) 
        ax.set_xticklabels(xticks_positions) 
        ax.spines[['right', 'top']].set_visible(False)

# Remove unused subplots
for i in range(plot_index, len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.show()


#%%
###################################################
######                YOY change               ####
###################################################

df.index.names = ['Date']
df_YOY = pd.DataFrame(columns=df.columns, index = df.index) 
df_YOY[df_YOY.columns] = df[df.columns].pct_change()*100

# Initialize subplots (6 rows, 4 columns)
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

# Plot each group in the corresponding subplot

plot_index = 0
for continent, countries in continents.items():
    if countries:  # Only plot if there are countries for this letter
        ax = axes[plot_index]
        df_YOY[countries].plot(ax=ax, legend=False, alpha = 0.2)
        ax.set_title(f'{continent}')
        plot_index += 1  # Move to the next subplot
        xticks_positions = [2000, 2023]
        ax.set_xticks([0, 23]) 
        ax.set_xticklabels(xticks_positions) 
        ax.spines[['right', 'top']].set_visible(False)
fig.suptitle('YOY change')
# Remove unused subplots
for i in range(plot_index, len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.show()

#%%
###################################################
######           20% adoption year        #########
###################################################
#threshold for early adoption
threshold  = 20
first_adoption_year = (df > threshold).idxmax(axis=0)
for country in df.columns:
    if (df[country] > threshold).any():   
        first_adoption_year.loc[country] = (df[country] > threshold).idxmax(axis=0)
    else:
        first_adoption_year.loc[country] = 1999
    
first_adoption_year = first_adoption_year.to_frame(name='Adoption Year')  # Convert Series to DataFrame
first_adoption_year['Adoption Year'] = first_adoption_year['Adoption Year'].astype('int')
first_adoption_year.reset_index(inplace = True)

# Merge adoption year with world population data
first_adoption_year = first_adoption_year.merge(world_population[['Country Name', '2022 Population']], on='Country Name', how='left')
first_adoption_year['2022 Population'] /= 1e7
first_adoption_year = first_adoption_year.sort_values(by="Adoption Year")



# Add continent information to the dataframe
first_adoption_year["Continent"] = first_adoption_year["Country Name"].map(lambda x: next((k for k, v in continents.items() if x in v), None))
first_adoption_year.dropna(inplace = True)
# Create interactive Plotly scatter plot
# Initialize figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.3)  # Adjust for widget space

# Normalize population for color mapping
norm = mcolors.Normalize(vmin=first_adoption_year["2022 Population"].min(),
                         vmax=first_adoption_year["2022 Population"].max())
cmap = cm.viridis  # Use viridis colormap

fig, ax = plt.subplots(figsize=(10, 6))

cax = fig.add_axes([0.92, 0.2, 0.02, 0.6])
cbar = None
def update_plot(continent):
    ax.clear()
    global cbar
    if continent == "All":
        fay = first_adoption_year
    else:
        fay = first_adoption_year[first_adoption_year["Country Name"].isin(continents[continent])]
    norm = mcolors.Normalize(vmin=fay["2022 Population"].min(),
                             vmax=fay["2022 Population"].max())
    fay_normal = fay[fay["Adoption Year"] != 1999]
    fay_1999 = fay[fay["Adoption Year"] == 1999]

    # Scatter plot for normal points (colored by population)
    sc = ax.scatter(
        fay_normal["Country Name"], fay_normal["Adoption Year"],
        s=100,  # Fixed marker size
        c=fay_normal["2022 Population"], cmap=cmap, norm=norm, edgecolors="black"
    )

    # Scatter plot for 1999 points with red 'X'
    ax.scatter(
        fay_1999["Country Name"], [max(fay["Adoption Year"])] * len(fay_1999),
        s=100, color="red", marker="x", label="Adopted Before 2000"
    )

    combined_countries = fay_normal["Country Name"].tolist() + fay_1999["Country Name"].tolist()

    # Set x-ticks for the countries
    ax.set_xticks(range(len(fay)))
    ax.set_xticklabels(combined_countries, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Adoption Year")
    ax.set_title(f"Internet Adoption Year - {continent}")
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_ylim(1999, 2023)
    
    # Add colorbar
    cax.clear()

    cbar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax)
    cbar.set_label("Population (millions)")

    plt.draw()

# Create interactive widget (RadioButtons)
axcolor = "lightgoldenrodyellow"
ax_radio = plt.axes([0.02, 0.4, 0.1, 0.2], facecolor=axcolor)
radio = RadioButtons(ax_radio, ["Asia"] + list(continents.keys())[1:])
for label in radio.labels:
    label.set_fontsize(12)  
    label.set_color("black") 

# Connect widget to update function
radio.on_clicked(update_plot)

# Initial plot (show all)
update_plot("Asia")

plt.show()

#%%
###################################################
######           Early vs Late adopters        ####
###################################################


# Define adoption year bins
bins = [1995, 2000, 2005, 2010, 2015, 2020, 2025]  # Adjust as needed
labels = ["NOT YET", "2000-2005", "2006-2010", "2011-2015", "2016-2020", "2021-2025"]

# Create a new column that categorizes countries into year ranges
first_adoption_year["Adoption Range"] = None 
first_adoption_year["Adoption Range"] = pd.cut(first_adoption_year["Adoption Year"], bins=bins, labels=labels, include_lowest=True, right = False)

# Create Scatter Plot (Bubble Chart)


# Add jitter to x and y positions
np.random.seed(42)  # For reproducibility
first_adoption_year["y_pos"] = 1 + np.random.uniform(-0.1, 0.1, size=len(first_adoption_year))  # Y-jitter around 1
first_adoption_year["x_jitter"] = np.random.uniform(-0.3, 0.3, size=len(first_adoption_year))  # X-jitter

# Convert x-axis categories to numerical values for jittering
x_mapping = {label: i for i, label in enumerate(labels)}
y_mapping = {label: i for i, label in enumerate(continents.keys())}

first_adoption_year["x_pos"] = first_adoption_year["Adoption Range"].map(x_mapping).astype('int64') + first_adoption_year["x_jitter"]
first_adoption_year["y_pos"] = first_adoption_year["Continent"].map(y_mapping).astype('int64') + first_adoption_year["y_pos"]

fig = px.scatter(
    first_adoption_year,
    x="x_pos",
    y="y_pos",
    color="Continent",
    hover_name="Country Name",
    hover_data={"2022 Population": False, "Adoption Year": True, "x_pos": False, "y_pos": False},
    title="Internet Adoption by Country and Year Range",
    labels={"Adoption Range": "Year Range", "Country Name": "Country"},
)

# Update layout for better readability
fig.update_traces(marker=dict(size=10, line=dict(width=1, color="black")))  # Set marker size and add outline
fig.update_layout(
    xaxis_title="Year Range",
    yaxis_title="",
    yaxis=dict(categoryorder="category ascending", showticklabels = False),  # Sort y-axis by country names
    xaxis=dict(tickmode="array", tickvals=list(x_mapping.values()), ticktext=list(x_mapping.keys()),),
)

# Show interactive plot
fig.show()


#%%
###################################################
######           Regional Comparison       ########
###################################################

region_df = pd.DataFrame(columns = [ 'Min', 'Max'])
for continent, countries in continents.items():
    if countries:  # Only plot if there are countries for this letter
        region_df.loc[continent, 'Max'] = f'{df[countries].max().idxmax()} ({df[countries].max().max():.2f}%)'
        region_df.loc[continent,'Min'] = f'{df[countries].min().idxmin()} ({df[countries].min().min():.2f}%)'
        
        
#%%
###################################################
######           Regional Comparison       ########
###################################################


fig, axes = plt.subplots(1, 1, figsize=(15, 10))


# Plot each group in the corresponding subplot
for continent, countries in continents.items():
    df_mean = df[countries].mean(axis = 1)
    axes.plot(df_mean, linewidth = 2, label = continent,marker = 'o')
    xticks_positions = [2000, 2023]
    axes.set_xticks([0, 23]) 
    axes.set_xticklabels(xticks_positions) 
    axes.spines[['right', 'top']].set_visible(False)
    axes.legend()

#%%
###################################################
######           GDP correlation           ########
###################################################

gdp.dropna(inplace = True)
gdp[['2022', 'adoption']] = gdp[['2022', 'adoption']].astype('float64')
fig = px.scatter(gdp, x = '2022', y = 'adoption', color = 'Continent',
                 hover_name = 'Country Name', title="Internet Adoption by Country and Year Range")
fig.show()