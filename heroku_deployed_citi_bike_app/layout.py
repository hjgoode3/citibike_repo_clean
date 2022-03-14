from dash import html,dcc


b1 = html.Button('Button1', id = 'play-button')
tabs = dcc.Tabs(id = 'tab_bar',value = 'intro_tab', children = [
                                                                dcc.Tab(label = 'Introduction', value = 'intro_tab'),
                                                                dcc.Tab(label = 'Data Analysis', value = 'eda_tab'),
                                                                dcc.Tab(label = 'Usage Patterns', value = 'clustering_tab'),
                                                                dcc.Tab(label = 'Current Rebalancing', value = 'rebalancing_tab'),
                                                                dcc.Tab(label = 'Rebalancing Forecasting Tool', value = 'rebalancing_strategy_tab'),
                                                                dcc.Tab(label = 'Conclusion', value = 'conclusion_tab'),
                                                                dcc.Tab(label = 'About Us', value = 'about_us_tab')


    ])


layout = html.Div([
    html.H1('Citi Bike Capstone Project'),
    tabs,
    dcc.Loading(id = 'loading',
                type = 'default',
                style = {'position' : 'absolute','top': '50px'},
                children = [html.Div(id='content')])

])
