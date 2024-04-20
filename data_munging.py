import pandas as pd

def get_incidents_data():
    incidents_data = pd.read_csv("Coordinates_Filtered_Missing_Migrants_Northern_Africa_with_Coordinates1.csv")
    # Filter incidents for the year 2024
    #incidents_data = incidents_data[incidents_data['Incident Year'] == 2024]
    return incidents_data

def get_unique_migration_routes():
    incidents_data = pd.read_csv("Coordinates_Filtered_Missing_Migrants_Northern_Africa_with_Coordinates1.csv")
    unique_routes = incidents_data["MigrationRoute"].dropna().unique().tolist()
    return unique_routes

def get_unique_years():
    incidents_data = pd.read_csv("Coordinates_Filtered_Missing_Migrants_Northern_Africa_with_Coordinates1.csv")
    unique_years = incidents_data["IncidentYear"].dropna().unique().tolist()
    return unique_years
