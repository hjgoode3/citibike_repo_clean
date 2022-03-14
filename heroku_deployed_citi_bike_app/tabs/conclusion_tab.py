from dash import dcc, html
from blurbs.conclusion_blurbs import conclusion_blurb, next_steps_blurb

def create_conclusion_tab():
    conclusion_tab = dcc.Tab(
        label = 'Conclusion',
        value = 'conclusion',
        children = [html.H2('Conclusion'),
                    html.Div(conclusion_blurb,style = {'font-size':'1vw'}),
                    html.H2('Next Steps'),
                    html.Div(next_steps_blurb,style = {'font-size':'1vw'})])
    return conclusion_tab
