import pandas as pd
import plotly.graph_objs as go

''' 
Modules to Install:
pip install pipenv
pip install geopandas==0.3.0
pip install pyshp==1.2.10
pip install shapely==1.6.3
pip install requests
pip install folium
'''


# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    # Plotting flu shot locations
    p_clinics = pd.read_json('https://data.cityofchicago.org/resource/kcki-hnch.json')

    # Loading Flu Shot Locations - Current Season Calendar
    flu_loc = pd.read_json('https://data.cityofchicago.org/resource/uks9-jgth.json')

    # Loading locations for Mental Health Clinics
    mental_health_loc = pd.read_json('https://data.cityofchicago.org/resource/g7ng-5vwp.json')

    # Loading Public Health Statistics- Diabetes hospitalizations in Chicago, 2000 - 2011
    diabetes_df = pd.read_json('https://data.cityofchicago.org/resource/vekt-28b5.json')

    # Requestin Mapbox Access Token
    mapbox_access_token = "pk.eyJ1IjoiYWNydWNldHRhIiwiYSI6ImNrOTRvbGxwazBmYjIzaXAzYjVqeXl5dHgifQ.xIYZveielGt7Nm0-ljj_9Q"

    # Flu shot locations
    site_lat = flu_loc['latitude']
    site_lon = flu_loc['longitude']
    locations_name = flu_loc['facility_name']

    # Public health clinics
    clinic_lat = p_clinics['latitude']
    clinic_lon = p_clinics['longitude']
    clinic_name = p_clinics['clinic_type']

    # Mental health clinics
    mental_lat = mental_health_loc['latitude']
    mental_lon = mental_health_loc['longitude']
    mental_name = mental_health_loc['site_name']

    # Plotting Chicago map
    data_one = [go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        legendgroup="Flu Shot Locations",
        name="Flu Shot Locations",
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            color='green',
            opacity=0.6,
            symbol='pharmacy'
        ),
        text=locations_name,
        hoverinfo='text',
    ),
        go.Scattermapbox(
            lat=clinic_lat,
            lon=clinic_lon,
            legendgroup="Public Clinics",
            mode='markers',
            name='Public Clinics',
            marker=go.scattermapbox.Marker(
                size=10,
                color='blue',
                opacity=1,
                symbol="hospital"
            ),
            text=clinic_name,
            hoverinfo='text'
        ),
        go.Scattermapbox(
            lat=mental_lat,
            lon=mental_lon,
            legendgroup="Mental Health Hospitals",
            name='Mental Health Hospitals',
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10,
                color='yellow',
                opacity=1,
                symbol="circle"
            ),
            text=mental_name,
            hoverinfo='text'
        )]

    layout_one = dict(
        title='Community Health Resources in Chicago',
        autosize=True,
        hovermode='closest',
        showlegend=True,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=41.8781,
                lon=-87.6298
            ),
            pitch=0,
            zoom=12,
            style='light'
        ))

    figures = []
    figures.append(dict(data=data_one, layout=layout_one))

    return figures