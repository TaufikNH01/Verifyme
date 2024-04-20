import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import data_munging as dm
import plot_migration

# Set page configuration
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"  # Ensures the sidebar is always open by default
)


# Function name and logo
#st.title("Migration Visualization")
col1, col2, col3 = st.columns(3)

with col1:
   st.image("hertie2.jpg", width=400, caption="")  # Replace 'path_to_your_logo.png' with the path to your logo

with col2:
   st.write("")

with col3:
   st.image("logo.jpg", width=200, caption="")

st.subheader("Incident Visualization")  


incidents_data = dm.get_incidents_data()
cause_of_death_choices = ['All'] + list(incidents_data["CauseDeath"].unique())
incident_year_choices = dm.get_unique_years()
migration_route_choices = ['All'] + list(dm.get_unique_migration_routes())


with st.sidebar: 
    st.image("data5.jpg", width=250)
    selectbox_cause_of_death = st.selectbox("Choose a Cause of Death", cause_of_death_choices)
    selectbox_migration_route = st.selectbox("Choose a Migration Route", migration_route_choices)
    selected_years = st.multiselect("Choose Years", incident_year_choices)


filtered_data = incidents_data[(incidents_data['CauseDeath'] == selectbox_cause_of_death) & (incidents_data['MigrationRoute'] == selectbox_migration_route)  &
    (incidents_data['IncidentYear'].isin(selected_years))]



if selectbox_cause_of_death == 'All' and selectbox_migration_route == 'All':
    filtered_data = incidents_data[
        incidents_data['IncidentYear'].isin(selected_years)
    ]
elif selectbox_cause_of_death == 'All':
     filtered_data = incidents_data[(incidents_data['MigrationRoute'] == selectbox_migration_route) & (incidents_data['IncidentYear'].isin(selected_years))]
     
elif selectbox_migration_route == 'All':
    filtered_data = incidents_data[
        (incidents_data['CauseDeath'] == selectbox_cause_of_death) &
        (incidents_data['IncidentYear'].isin(selected_years))
    ]
else:
    filtered_data = incidents_data[(incidents_data['CauseDeath'] == selectbox_cause_of_death) & (incidents_data['MigrationRoute'] == selectbox_migration_route)  &
    (incidents_data['IncidentYear'].isin(selected_years))]
    

if filtered_data.empty:
    st.write(f"No incident happened because of the {selectbox_cause_of_death} on {selectbox_migration_route}.")
else:
    migration_plot = plot_migration.build_migration_chart(incidents_data, selectbox_cause_of_death, selectbox_migration_route, selected_years)
    st.plotly_chart(migration_plot)
   # migration_plot = plot_migration.build_migration_chart(filtered_data)
   # st.plotly_chart(migration_plot)





st.write(
    """
    Team Combined Force:
    Saakshi Malhotra (RWTH Aachen) |
    Dhruvkumar Sathawara (RWTH Aachen) |
    Taufik |
    Isabel
    """
)
