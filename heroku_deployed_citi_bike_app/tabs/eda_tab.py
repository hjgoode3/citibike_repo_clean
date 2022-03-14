import dash
from dash import dcc, html
import pickle
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from blurbs.eda_blurbs import rollout_clusters_blurb, pop_density_blurb, transit_location_blurb, usage_plot_blurb, ride_per_minute_blurb, rides_per_month_blurb, rides_per_year_blurb, rides_per_day_blurb, eda_intro_blurb


## START POPULATION DENSITY GRAPHIC --------------------------

pop_data = pickle.load(open('./data/pop_data.pkl', 'rb')) # population density data frame

with open('./data/N_Areas.geojson', 'r') as j: # shape file for neighborhood boundaries, needed for population density plot
    boundaries = json.loads(j.read())


pop_density = go.Figure(go.Choroplethmapbox(geojson=boundaries,
                                    featureidkey='properties.ntacode',
                                    locations=pop_data['Neighborhood Tabulation Area Code (NTA Code)'],
                                    z=pop_data['Population Density (per Sq. Mi.)'],
                                    zmin = 0,
                                    zmax = 100000,
                                    colorscale="Blues",
                                    marker_line_width=0))
pop_density.update_layout(mapbox_style="carto-positron",
                mapbox_zoom=10, mapbox_center = {"lat": 40.747673, "lon" : -73.951292})
pop_density.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

## END POPULATION DENSITY GRAPHIC CHUNK ---------------------------

## START PUBLIC TRANSIT LOCATION GRAPHIC ---------------------------
dock_train_bus_df = pickle.load(open('./data/dock_train_bus_df.pkl', 'rb')) # dataframe with dock locations, bus stop location, and subway station locations
transit_locations = px.scatter_mapbox(dock_train_bus_df,
                lat = 'latitude',
                lon = 'longitude',
                color = 'type',
                mapbox_style = 'carto-positron',
                zoom = 10,
                center = dict(lat = 40.76421, lon = -73.95623)
                )
transit_locations.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

## END PUBLIC TRANSIT LOCATION GRAPHIC -----------------------------------

## START ROLLOUT CLUSTER GRAPHIC ----------------------------------

usage_patterns = pd.read_csv('data/usage_patterns.csv')
usage_trend_plot = go.Figure(go.Heatmap(
                z = usage_patterns['num_rides'],
                x = usage_patterns['hour_of_day'],
                y = usage_patterns['day_of_week'],
                colorscale=[[0, 'white'], [1, 'blue']]))
usage_trend_plot.update_layout(
    yaxis = dict(
        tickmode = 'array',
        tickvals = [1, 2, 3, 4, 5, 6,7],
        ticktext = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']
    ),
    xaxis = dict(
        tickmode = 'array',
        tickvals = list(range(24)),
        ticktext = ['12 AM','','','','4 AM','','','','8 AM','','','','12 PM','','','','4 PM','','','','8 PM','','','11 PM']
        ),
    font = dict(size = 16),
    title = dict(text='Average Number of Rides by Time and Day of Week')

)

## END ROLLOUT CLUSTER GRAPHIC --------------------------------

## START RIDES BY MONTH AND RIDES BY YEAR GRAPHIC ---------------------------

ride_time_data = pickle.load(open('./data/ridesbytime.pkl', 'rb'))

rides_per_year = px.line(pd.DataFrame(ride_time_data.groupby('year')['ridecount'].agg('sum')).reset_index(),
            x='year',
            y='ridecount',
            title="Annual Total Rides",
            labels = dict(total_rides="Total Number of Rides", year="Year"),
            markers=True)
rides_per_year.layout.plot_bgcolor = 'white'
rides_per_year.update_yaxes(nticks=15, ticks = 'outside', showgrid = True)
rides_per_year.update_xaxes(nticks = 10, tickangle=0, ticks = 'outside', showgrid = True)

rides_per_month = px.line(ride_time_data,
            x='ym',
            y='ridecount',
            title="Monthly Total Rides",
            labels = dict(ridecount="Number of Rides", ym="Date"),
            markers=True)
rides_per_month.layout.plot_bgcolor = 'white'
rides_per_month.update_traces(marker={'size': 12,
                        'color': 'blue'}, line = {'color': 'mediumslateblue'})
rides_per_month.update_yaxes(nticks=15, ticks = 'outside', showgrid = False)
rides_per_month.update_xaxes(nticks = 15, tickangle=45, ticks = 'outside', showgrid = False)

## END RIDES BY MONTH AND YEAR GRAPHIC --------------------------------------

## START NUMBER OF RIDES BY MINUTE

rides_by_minute_data = pickle.load(open('./data/countofridesbyminutes.pkl', 'rb'))

rides_by_minute = px.bar(rides_by_minute_data,
            x="durationinmin",
            y="count",
            title="Trip Duration Distribution",
            labels = dict(count="Number of Rides", durationinmin="Time (min)"))
rides_by_minute.update_traces(marker_color='steelblue')
for data in rides_by_minute.data:
    data["width"] = 1.0
    rides_by_minute.layout.plot_bgcolor = 'white'
    rides_by_minute.update_yaxes(nticks = 16, ticks = 'outside', showgrid = False)
    rides_by_minute.update_xaxes(nticks = 14, ticks = 'outside')


## END NUMBER OF RIDES BY MINUTE

## START TOTAL DAILY RIDES AND NUMBER OF DOCKS BY YEAR
dailytotal = pickle.load(open('./data/totaldailyrides.pkl', 'rb'))
yearlytotal = pickle.load(open('./data/numdocksperyear.pkl', 'rb'))

import plotly.graph_objects as go
doubletrouble = go.Figure()

doubletrouble.add_trace(
    go.Scatter(
        name = 'Daily Total Rides (scaled  x0.01)',
        x=dailytotal['newdate'],
        y=dailytotal['numofrides']/100,
        mode = 'markers',
        opacity = 1,
        marker =dict(color='blue', size = 7)
        )
    )

doubletrouble.add_trace(
    go.Bar(
        name = 'Unique Total Docks',
        x=yearlytotal['year'],
        y=yearlytotal['count'],
        opacity = 0.4,
        marker = dict(color = 'red')
        )
    )
doubletrouble.update_layout(
    legend=dict(yanchor = "top", y = 0.85, xanchor = "left", x = 0.01),
    title = 'Daily Total Rides vs. Docks',
    xaxis_title = 'Date (Year)',
    yaxis_title = 'Count'
    )

    ## END TOTAL DAILY RIDES AND NUMBER OF DOCKS BY YEAR
def create_eda_tab():
    eda_tab = dcc.Tab(label='Data Analysis',
                    value='eda',
                    children = [

                    html.H2('EDA Introduction', style={'textAlign': 'center'}),
                    html.Div(eda_intro_blurb, style = {'font-size': '1vw', 'textAlign': 'center'}),
                    html.H1(' '),
                    html.Div(children = [
                                        #Rollout Map Div
                                    html.H4(),
                                    html.Div(children = [dcc.Slider(
                                            id='slider',
                                            marks={i: '{}'.format(i) for i in range(2013, 2022)},
                                            min=2013,
                                            max=2021,
                                            value=2013
                                        ),dcc.Graph(id='rollout_map',
                                            style = {'height' : '100%'})],
                                            style={'width': '60%','height' : '100%', 'display': 'inline-block'}),
                                    html.Div(children = [html.H2('CitiBike Rollout Plan'), html.Div(rollout_clusters_blurb,style = {'font-size': '1vw'})],
                                                    style={'width': '30%', 'display': 'inline-block','vertical-align': 'top','margin-left': '9%'})],
                                                    style = {'height' : '80vh'}),



                            #Pop Density Div
                            html.Div(children = [
                                            html.Div(dcc.Graph(id='pop_density' ,
                                                    figure=pop_density,
                                                    style = {'height' : '100%'}),
                                                    style={'width': '60%','height' : '100%', 'display': 'inline-block'}),
                                            html.Div(children = [html.H2('Population Density in NYC'), html.Div(pop_density_blurb,style = {'font-size': '1vw'})],
                                                            style={'width': '30%', 'display': 'inline-block','vertical-align': 'top','margin-left': '9%'})],
                                                            style = {'height' : '80vh','margin-top':'10px'}),




                            #Transit Location Div
                            html.Div(children = [
                                            html.Div(dcc.Graph(id = 'transit_locations',
                                                    figure = transit_locations,
                                                    style = {'height' : '100%'}),
                                                    style={'width': '60%','height' : '100%', 'display': 'inline-block'}),
                                            html.Div(children = [html.H2('Transit Locations in NYC'), html.Div(transit_location_blurb,style = {'font-size': '1vw'})],
                                                            style={'width': '30%', 'display': 'inline-block','vertical-align': 'top','margin-left': '9%'})],
                                                            style = {'height' : '80vh','margin-top':'10px'}),



                            # Usage Pattern Div
                            html.Div(children = [
                                            html.Div(dcc.Graph(id='usage_pattern',
                                                    figure=usage_trend_plot,
                                                    style = {'height' : '100%'}),
                                                    style={'width': '60%','height' : '100%', 'display': 'inline-block'}),
                                            html.Div(children = [html.H2('CitiBike Usage Patterns'), html.Div(usage_plot_blurb,style = {'font-size': '1vw'})],
                                                            style={'width': '30%', 'display': 'inline-block','vertical-align': 'top','margin-left': '9%'})],
                                                            style = {'height' : '40vh','margin-top':'10px'}),


                            # Rides per year Div
                            html.Div(children = [
                                            html.Div(dcc.Graph(id='rides_per_year',
                                                    figure=rides_per_year,
                                                    style = {'height' : '100%'}),
                                                    style={'width': '60%','height' : '100%', 'display': 'inline-block'}),
                                            html.Div(children = [html.H2('Annual Total Rides'), html.Div(rides_per_year_blurb, style = {'font-size':'1vw'})],
                                                            style={'width': '30%', 'display': 'inline-block','vertical-align': 'top','margin-left': '9%'})],
                                                            style = {'height' : '40vh','margin-top':'10px'}),

                            #Rides per Month Div
                            html.Div(children = [
                                            html.Div(dcc.Graph(id='rides_per_month',figure=rides_per_month,
                                                    style = {'height' : '100%'}),
                                                    style={'width': '60%','height' : '100%', 'display': 'inline-block'}),
                                            html.Div(children = [html.H2('Total Monthly Rides'), html.Div(rides_per_month_blurb,style = {'font-size':'1vw'})],
                                                            style={'width': '30%', 'display': 'inline-block','vertical-align': 'top','margin-left': '9%'})],
                                                            style = {'height' : '40vh','margin-top':'10px'}),

                            # #Rides per Day Div
                            html.Div(children = [
                                            html.Div(dcc.Graph(id='doublethang',figure=doubletrouble,
                                                    style = {'height' : '100%'}),
                                                    style={'width': '60%','height' : '100%', 'display': 'inline-block'}),
                                            html.Div(children = [html.H2('Daily Total Rides'), html.Div(rides_per_day_blurb,style = {'font-size':'1vw'})],
                                                            style={'width': '30%', 'display': 'inline-block','vertical-align': 'top','margin-left': '9%'})],
                                                            style = {'height' : '40vh','margin-top':'10px'}),

                            # Rides by minute Div
                            html.Div(children = [
                                            html.Div(dcc.Graph(id='num_of_rides_by_minute', figure = rides_by_minute,
                                                    style = {'height' : '100%'}),
                                                    style={'width': '60%','height' : '100%', 'display': 'inline-block'}),
                                            html.Div(children = [html.H2('Trip Duration'), html.Div(ride_per_minute_blurb,style = {'font-size':'1vw'})],
                                                            style={'width': '30%', 'display': 'inline-block','vertical-align': 'top','margin-left': '9%'})],
                                                            style = {'height' : '40vh','margin-top':'10px'}),
    ])
    return eda_tab

