# dashboard_trial

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots 
import matplotlib.pyplot as plt

# === SIDEBAR CONFIGURATION ===
# st.sidebar.header("Dashboard Configuration")
# st.sidebar.markdown("Use the options below to customize the visualizations.")
# # Add more sidebar configurations if needed


# === COMPONENT 1 ===

## 1.Challenge problem and solution 
st.title("Lost Souls in the Unknown")
st.markdown("Missing Migrants Project by Bueno Team")
st.image("/Users/pikpes/Downloads/IOM_Migration.jpg", caption="Missing Souls in the Sea", use_column_width=True)


st.markdown("""
In July 2019, a migrant boat carrying approximately 80 people departed from Zarzis, Tunisia, in an attempt to reach Europe. Tragically, the overcrowded vessel sank, resulting in the loss of most passengers, including women and children. Only 16 individuals were rescued by local fishermen and the Tunisian coast guard. This heartbreaking event starkly illustrates the perilous journey migrants undertake when crossing the Mediterranean Sea from North Africa. It serves as a poignant reminder of the urgent need for enhanced safety measures and international cooperation to address the ongoing humanitarian crisis. Alarmingly, Northern Africa ranks second highest globally in migrant deaths across continents.
""")

# === 1st Viz ===

# Load the data
df = pd.read_csv("/Users/pikpes/Downloads/Missing_Migrants_Global_Figures_allData.csv")

# Sidebar for visualization selection
st.sidebar.header("Visualization Configuration")
st.sidebar.subheader("Total Deaths by Continent")
viz_type = st.sidebar.radio(
    "Select Visualization Type for Continent Deaths",
    ("Bar Chart", "Raw Data")
)

# Data processing for visualization
df['Incident Date'] = pd.to_datetime(df['Incident Date'])
df['Month-Year'] = df['Incident Date'].dt.to_period('M').dt.to_timestamp()
continent_deaths = df.groupby('Region of Incident')['Total Number of Dead and Missing'].sum().reset_index()
continent_deaths = continent_deaths.sort_values(by='Total Number of Dead and Missing', ascending=False).head(5)

# Define columns for graph and text side by side
col1, col2 = st.columns([3, 1])  # Adjust column widths as needed

if viz_type == "Bar Chart":
        # Create a bar chart with color distinction
        colors = ['red' if continent == 'Northern Africa' else 'grey' for continent in continent_deaths['Region of Incident']]
        fig = px.bar(continent_deaths, x='Region of Incident', y='Total Number of Dead and Missing',
                     title='Total Deaths by Continent',
                     labels={'Region of Incident': 'Continent', 'Total Number of Dead and Missing': 'Deaths'})
        fig.update_traces(marker_color=colors, selector=dict(type='bar'))
        fig.update_layout(
            legend=dict(
                font=dict(
                    size=10  # Smaller font size for the legend
                ),
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )
        # Display the plot using plotly_chart
        st.plotly_chart(fig, use_container_width=True)
    
elif viz_type == "Raw Data":
    st.write(continent_deaths)
    st.markdown("**Notes:** This table displays the raw data of total deaths and missing by continent, sorted by the highest numbers.")


st.markdown("""
The continent also grapples with a myriad of causes leading to death. From drownings and harsh environmental conditions to vehicle accidents and even unknown factors, Northern Africa faces a range of challenges. Among the top three continents with the highest death tolls, Northern Africa stands out for the diversity of causes contributing to fatalities. This complexity is further compounded by the poor quality of data collection in the region.
""")

# Section for Viz 2 Controls
st.sidebar.subheader("Death Causes")
top_continents_viz2 = st.sidebar.multiselect(
    "Select continents for Death Causes",
    options=df['Region of Incident'].unique(),
    default=['Mediterranean', 'Northern Africa', 'North America']
)

# Section for Viz 3 Controls
st.sidebar.subheader("Data Source Quality")
top_continents_viz3 = st.sidebar.multiselect(
    "Select continents for Data Source",
    options=df['Region of Incident'].unique(),
    default=['Mediterranean', 'Northern Africa', 'North America']
)

# Process data for Viz 2
filtered_data_viz2 = df[df['Region of Incident'].isin(top_continents_viz2)]
death_causes = filtered_data_viz2.groupby(['Region of Incident', 'Cause of Death'])['Total Number of Dead and Missing'].sum().reset_index()
region_totals = death_causes.groupby('Region of Incident')['Total Number of Dead and Missing'].sum().reset_index()
death_causes = death_causes.merge(region_totals, on='Region of Incident', suffixes=('', '_total'))
death_causes['Percentage'] = (death_causes['Total Number of Dead and Missing'] / death_causes['Total Number of Dead and Missing_total']) * 100

# Process data for Viz 3
filtered_data_viz3 = df[df['Region of Incident'].isin(top_continents_viz3)]
source_quality = filtered_data_viz3.groupby(['Region of Incident', 'Source Quality'])['Total Number of Dead and Missing'].sum().reset_index()
region_totals = source_quality.groupby('Region of Incident')['Total Number of Dead and Missing'].sum().reset_index()
source_quality = source_quality.merge(region_totals, on='Region of Incident', suffixes=('', '_total'))
source_quality['Percentage'] = (source_quality['Total Number of Dead and Missing'] / source_quality['Total Number of Dead and Missing_total']) * 100

# Define columns for side by side visualizations
col1, col2 = st.columns(2)

with col1:
    # Visualization Viz 2
    fig_causes = px.bar(death_causes, x='Region of Incident', y='Percentage',
                        color='Cause of Death', title='Death Causes Percentage',
                        labels={'Region of Incident': 'Continent', 'Percentage': 'Percentage (%)'},
                        barmode='stack', color_continuous_scale='RdYlBu')
    fig_causes.update_layout(legend=dict(orientation='h', yanchor='bottom', y=-1, xanchor='right', x=1,
    font=dict(size=10)))
    st.plotly_chart(fig_causes, use_container_width=True)  # use_container_width makes the plot resize according to the column width

with col2:
    # Visualization Viz 3
    fig_quality = px.bar(source_quality, x='Region of Incident', y='Percentage',
                         color='Source Quality', title='Data Source Quality Percentage',
                         labels={'Region of Incident': 'Continent', 'Percentage': 'Percentage (%)'},
                         barmode='stack', color_continuous_scale='RdYlBu')
    fig_quality.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    st.plotly_chart(fig_quality, use_container_width=True)  # Same resizing for consistency

st.markdown("""
Migrants from Northern Africa resort to various measures to cross borders, often navigating through different and perilous routes. Against this backdrop, we offer a route assessment over time, presenting distinct risk profiles.
""")

st.subheader("Incident Assessment")

st.markdown("""
place the route assessment here
""")

st.subheader("Improving Data Acquisition")
st.markdown("Introducing Verify.me, a low-bandwidth web app accessible almost anywhere on Earth, empowering registered and authorized organizations across Europe and Africa to collaborate seamlessly. Tailored specifically to tackle data identification challenges, our platform streamlines data sharing, ensuring vital information is readily available and actionable, regardless of location.")

st.image("/Users/pikpes/Downloads/Blue Modern Mobile Application Presentation/1.png", use_column_width=True)
st.image("/Users/pikpes/Downloads/Blue Modern Mobile Application Presentation/2.png", use_column_width=True)
