import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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
    # Loading public health clinics
    p_clinics = pd.read_json('https://data.cityofchicago.org/resource/kcki-hnch.json')

    # Loading Flu Shot Locations - Current Season Calendar
    flu_loc = pd.read_json('https://data.cityofchicago.org/resource/uks9-jgth.json')

    # Loading locations for Mental Health Clinics
    mental_health_loc = pd.read_json('https://data.cityofchicago.org/resource/g7ng-5vwp.json')

    # NY Times COVID Daily Cases
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    nyt_daily_covid = pd.read_csv(url, error_bad_lines=False)

    # Requesting Mapbox Access Token
    mapbox_access_token = "pk.eyJ1IjoiYWNydWNldHRhIiwiYSI6ImNrOTRvbGxwazBmYjIzaXAzYjVqeXl5dHgifQ.xIYZveielGt7Nm0-ljj_9Q"

    # Flu shot latitude & longitude for Mapbox
    site_lat = flu_loc['latitude']
    site_lon = flu_loc['longitude']
    locations_name = flu_loc['facility_name']

    # Public health clinics latitude & longitude for Mapbox
    clinic_lat = p_clinics['latitude']
    clinic_lon = p_clinics['longitude']
    clinic_name = p_clinics['clinic_type']

    # Mental health clinics latitude & longitude for Mapbox
    mental_lat = mental_health_loc['latitude']
    mental_lon = mental_health_loc['longitude']
    mental_name = mental_health_loc['site_name']

    # Cleaning Chicago COVID daily values from NYT

    # Filtering daily cases for Cook County & Illinois
    chi_nyt_covid = nyt_daily_covid[(nyt_daily_covid.county == "Cook") & (nyt_daily_covid.state == "Illinois")]
    chi_nyt_covid.date = pd.to_datetime(chi_nyt_covid.date)

    # Creating daily difference in cases and moving average for every 7 days
    chi_nyt_covid['new_daily_cases'] = chi_nyt_covid['cases'] - chi_nyt_covid['cases'].shift(+1)
    chi_nyt_covid['new_death_cases'] = chi_nyt_covid['deaths'] - chi_nyt_covid['deaths'].shift(+1)
    chi_nyt_covid['MA5_Cases'] = round(chi_nyt_covid.new_daily_cases.rolling(7).mean())
    chi_nyt_covid['MA5_Deaths'] = round(chi_nyt_covid.new_death_cases.rolling(7).mean())

    # Setting date as index
    chi_nyt_covid.set_index('date')

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
        autosize=True,
        hovermode='closest',
        showlegend=True,
        legend_orientation="h",
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

    # Creating second plot with daily COVID cases
    fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    fig2.add_trace(go.Scatter(name="Daily Cases", x=chi_nyt_covid.date,
                              y=chi_nyt_covid.new_daily_cases), row=1, col=1)

    fig2.add_trace(go.Scatter(name="7-day avg. cases", x=chi_nyt_covid.date,
                              y=chi_nyt_covid['MA5_Cases'], fill='tozeroy', line=dict(color='green', width=1)),
                   row=1, col=1)

    fig2.add_trace(go.Scatter(name="Daily Deaths", x=chi_nyt_covid.date,
                              y=chi_nyt_covid.new_death_cases),
                   row=2, col=1)

    fig2.add_trace(go.Scatter(name="7-day avg. deaths", x=chi_nyt_covid.date,
                              y=chi_nyt_covid['MA5_Deaths'],fill='tozeroy', line=dict(color='black', width=1)),
                   row=2, col=1)

    fig2.update_layout(height=600, width=600,hovermode="x",legend_orientation="h")

    fig2.update_traces(mode="lines", hovertemplate=None)

    fig2.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=14, label="2w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="todate"),
                dict(step="all")])))

    # Converting to dictionary to make it easier for Flask to load
    data_two = fig2.to_dict()

    figures = []
    figures.append(dict(data=data_one, layout=layout_one))
    figures.append(data_two)

    return figures