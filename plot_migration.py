import plotly.graph_objects as go
import numpy as np
import geopandas as gpd
import json
import streamlit as st

def build_migration_chart(incidents_data, selectbox_cause_of_death, selectbox_migration_route, selected_years):
    
    filtered_data = incidents_data[(incidents_data['CauseDeath'] == selectbox_cause_of_death) & (incidents_data['MigrationRoute'] == selectbox_migration_route)  &
        (incidents_data['IncidentYear'].isin(selected_years))]
    
    

    # Filter incidents based on selected cause of death
    #filtered_data = incidents_data[incidents_data['CauseDeath'] == selectbox_cause_of_death]
    #filtered_data = incidents_data[(incidents_data['CauseDeath'] == selectbox_cause_of_death) & (incidents_data['MigrationRoute'] == selectbox_migration_route)]

 

   
    if selectbox_cause_of_death == 'All' and selectbox_migration_route == 'All':
        filtered_data = incidents_data[
        incidents_data['IncidentYear'].isin(selected_years)
    ]
    elif selectbox_cause_of_death == 'All':
         filtered_data = incidents_data[(incidents_data['MigrationRoute'] == selectbox_migration_route) &(incidents_data['IncidentYear'].isin(selected_years))]
     #st.write(incidents_data)
    elif selectbox_migration_route == 'All':
        filtered_data = incidents_data[
        (incidents_data['CauseDeath'] == selectbox_cause_of_death) &
        (incidents_data['IncidentYear'].isin(selected_years))
    ]
    else:
        filtered_data = incidents_data[(incidents_data['CauseDeath'] == selectbox_cause_of_death) & (incidents_data['MigrationRoute'] == selectbox_migration_route)  &
        (incidents_data['IncidentYear'].isin(selected_years))]
    
    # Create a color mapping for each unique cause of death
    unique_causes = filtered_data['CauseDeath'].unique()
    color_map = {cause: f'rgb({np.random.randint(0, 256)}, {np.random.randint(0, 256)}, {np.random.randint(0, 256)})' for cause in unique_causes}


    fig = go.Figure()

    for cause, color in color_map.items():
        subset_data = filtered_data[filtered_data['CauseDeath'] == cause]
        
        fig.add_trace(
            go.Scattergeo(
                lon=subset_data['Longitude'],
                lat=subset_data['Latitude'],
                #hoverinfo='text',
                text=subset_data['CauseDeath'],
                mode='markers',
                marker=dict(
                    size=5,
                    opacity=0.8,
                    color=color,
                    line=dict(width=1, color='black'),
                ),
                name=cause,
                hovertemplate='%{text}<br>' + 
                              'Location of Incident: %{customdata}',
                customdata=subset_data['CauseDeath'] + subset_data ['LocationIncident']
            )
        )


    fig = fig.update_layout(
        title=f"Incidents of {filtered_data['CauseDeath'].iloc[0]} on route {filtered_data['MigrationRoute'].iloc[0]} in {selected_years}",
        title_pad_l=0,
        title_pad_r=10,
        showlegend=False,
        geo=go.layout.Geo(
            scope="world",
            projection_type="natural earth",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
        ),
        margin={"r":0,"t":30,"l":0,"b":0},
        height=450,  # Set the height of the plot
        width=1000    # Set the width of the plot
    )

    #st.plotly_chart(fig)
    return fig

''' mapbox=dict(
            style="open-street-map",
            layers=[
                {
                    "source": json.loads(json.dumps(world_map_geojson)),
                    "type": "fill",
                    "color": "rgb(243, 243, 243)"
                }
            ],
            zoom=100
        )'''