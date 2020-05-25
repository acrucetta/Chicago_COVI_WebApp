import pandas as pd
import plotly.graph_objs as go
from datetime import timedelta

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
    # NY Times COVID Daily Cases
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    nyt_daily_covid = pd.read_csv(url, error_bad_lines=False)

    # Chicago Hospital Capacity
    chi_hospitals = pd.read_json('https://data.cityofchicago.org/resource/f3he-c6sv.json')
    chi_hospitals.date = pd.to_datetime(chi_hospitals.date)

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

    # Creating second plot with daily COVID cases
    trace_1 = go.Scatter(name = "Daily Cases", x=chi_nyt_covid.date,y= chi_nyt_covid.new_daily_cases)
    trace_2 = go.Scatter(name="7-day avg. cases", x=chi_nyt_covid.date, y=chi_nyt_covid['MA5_Cases'],
                             fill='tozeroy', line=dict(color='green', width=1))
    data_2 = [trace_1, trace_2]
    layout_2 = go.Layout(title = "Daily Cases", autosize=True,hovermode="x",legend_orientation="h")
    fig2 = go.Figure(data = data_2, layout = layout_2)
    fig2.update_traces(mode="lines", hovertemplate=None)
    fig2.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=14, label="2w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="todate"),
                dict(step="all")])))

    # Creating second plot with daily COVID cases
    trace_3 = go.Scatter(name="Daily Deaths", x=chi_nyt_covid.date, y=chi_nyt_covid.new_death_cases)
    trace_4 = go.Scatter(name = "7-day avg. deaths" , x=chi_nyt_covid.date, y=chi_nyt_covid['MA5_Deaths'],
                                      fill='tozeroy',line=dict(color='black', width=1))
    data_3 = [trace_3, trace_4]

    layout_3 = go.Layout(title = "Daily Deaths", autosize=True, hovermode="x", showlegend = True)

    fig3 = go.Figure(data=data_3, layout=layout_3)

    fig3.update_traces(mode="lines", hovertemplate=None)

    fig3.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=14, label="2w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="todate"),
                dict(step="all")])))

    # Plotting time-lapse
    fig_hospitals = go.Figure()

    fig_hospitals.add_trace(go.Scatter(name="COVID Patients in Ventilators", x=chi_hospitals.date,
                                       y=chi_hospitals.ventilators_in_use_covid_19_patients))

    fig_hospitals.add_trace(go.Scatter(
        x=[min(chi_hospitals.date), max(chi_hospitals.date)],
        y=[450, 450],
        mode="lines+markers+text",
        name="Limit to go to phase 3",
        textposition="bottom center"
    ))

    fig_hospitals.add_annotation(
        x=max(chi_hospitals.date),
        y=chi_hospitals.ventilators_in_use_covid_19_patients[chi_hospitals.date == max(chi_hospitals.date)][0],
        text="Patients in Ventilators")

    fig_hospitals.add_annotation(
        x=max(chi_hospitals.date),
        y=450,
        text="Limit for Phase 3")

    fig_hospitals.update_layout(title="COVID Patients in Ventilators", autosize=True, hovermode="x", showlegend = False)

    fig_hospitals.update_traces(mode="lines", hovertemplate=None)

    fig_hospitals.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=14, label="2w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="todate"),
                dict(step="all")])))

    # Plotting time-lapse
    fig_icu = go.Figure()

    fig_icu.add_trace(go.Scatter(name="COVID Patients in ICU Beds", x=chi_hospitals.date,
                                 y=chi_hospitals.icu_beds_in_use_covid_19))

    fig_icu.add_trace(go.Scatter(
        x=[min(chi_hospitals.date), max(chi_hospitals.date)],
        y=[600, 600],
        mode="lines+markers+text",
        name="Limit to go to phase 3",
        textposition="bottom center"
    ))

    fig_icu.add_annotation(
        x=max(chi_hospitals.date),
        y=chi_hospitals.icu_beds_in_use_covid_19[chi_hospitals.date == max(chi_hospitals.date)][0],
        text="Patients in ICU Beds")

    fig_icu.add_annotation(
        x=max(chi_hospitals.date),
        y=600,
        text="Limit for Phase 3")

    fig_icu.update_layout(title="COVID Patients in ICU Beds", autosize=True, hovermode="x", showlegend = False)

    fig_icu.update_traces(mode="lines", hovertemplate=None)

    fig_icu.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=14, label="2w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="todate"),
                dict(step="all")])))

    # Converting to dictionary to make it easier for Flask to load
    figure_2 = fig2.to_dict()
    figure_3 = fig3.to_dict()
    figure_hospitals = fig_hospitals.to_dict()
    figure_icu = fig_icu.to_dict()

    figures = []
    figures.append(figure_2)
    figures.append(figure_3)
    figures.append(figure_hospitals)
    figures.append(figure_icu)

    return figures