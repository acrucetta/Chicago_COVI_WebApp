import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
import folium

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

def load_data():
    #Loading Chicago Department of Public Health Clinic Locations
    p_clinics = pd.read_json('https://data.cityofchicago.org/resource/kcki-hnch.json')

    #Loading Flu Shot Locations - Current Season Calendar
    flu_loc = pd.read_json('https://data.cityofchicago.org/resource/uks9-jgth.json')

    #Loading COVID Cases for Chicago by Zip Code
    covid_df = pd.read_csv('data/il-covid-counts-by-zipcode-4_21_2020.csv')

    #Loading locations for Mental Health Clinics
    mental_health_loc = pd.read_json('https://data.cityofchicago.org/resource/g7ng-5vwp.json')

    #Loading Public Health Statistics- Diabetes hospitalizations in Chicago, 2000 - 2011
    diabetes_df = pd.read_json('https://data.cityofchicago.org/resource/vekt-28b5.json')
    
    

def cleandata():
    # Plotting flu shot locations
    mapbox_access_token = "pk.eyJ1IjoiYWNydWNldHRhIiwiYSI6ImNrOTRvbGxwazBmYjIzaXAzYjVqeXl5dHgifQ.xIYZveielGt7Nm0-ljj_9Q"

    # Flu shot locations
    site_lat = flu_loc.latitude
    site_lon = flu_loc.longitude
    locations_name = flu_loc.facility_name

    # Public health clinics
    clinic_lat = p_clinics.latitude
    clinic_lon = p_clinics.longitude
    clinic_name = p_clinics.clinic_type

    # Mental health clinics
    mental_lat = mental_health_loc.latitude
    mental_lon = mental_health_loc.longitude
    mental_name = mental_health_loc.site_name

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    load_data()
    cleandata()
    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    
    graph_one = []    
    graph_one.add_trace(go.Scattermapbox(
        lat=site_lat,
        lon=site_lon,
        legendgroup="Flu Shot Locations",
        name = "Flu Shot Locations",
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            color='green',
            opacity=0.6,
            symbol = 'pharmacy'
        ),
        text=locations_name,
        hoverinfo='text',
    ))

    graph_one.add_trace(go.Scattermapbox(
            lat=clinic_lat,
            lon=clinic_lon,
            legendgroup="Public Clinics",
            mode='markers',
            name = 'Public Clinics',
            marker=go.scattermapbox.Marker(
                size=10,
                color='blue',
                opacity=1,
                symbol = "hospital"
            ),
            text=clinic_name,
            hoverinfo='text'
        ))

    graph_one.add_trace(go.Scattermapbox(
            lat=mental_lat,
            lon=mental_lon,
            legendgroup="Mental Health Hospitals",
            name = 'Mental Health Hospitals',
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10,
                color='yellow',
                opacity=1,
                symbol = "circle"
            ),
            text=mental_name,
            hoverinfo='text'
        ))

    graph_one.update_layout(
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
        ),
    )


# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []

    graph_two.append(
      go.Bar(
      x = ['a', 'b', 'c', 'd', 'e'],
      y = [12, 9, 7, 5, 1],
      )
    )

    layout_two = dict(title = 'Chart Two',
                xaxis = dict(title = 'x-axis label',),
                yaxis = dict(title = 'y-axis label'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    graph_three.append(
      go.Scatter(
      x = [5, 4, 3, 2, 1, 0],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_three = dict(title = 'Chart Three',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label')
                       )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    
    graph_four.append(
      go.Scatter(
      x = [20, 40, 60, 80],
      y = [10, 20, 30, 40],
      mode = 'markers'
      )
    )

    layout_four = dict(title = 'Chart Four',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures
