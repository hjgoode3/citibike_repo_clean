from dash import dcc, html
from blurbs.project_info_blurbs import project_blurb, data_blurb
# from PIL import Image

# cb_photo = Image.open('./data/image/pic1t.jpg')
# charles_photo = Image.open('./data/image/charles_biket.jpg')
def create_intro_tab():
    intro_tab = dcc.Tab(label = 'Project Introduction',
                        value='intro',
                        children = [
    html.Div(children = [
                            html.Div(children = [html.H1('Project Description'),project_blurb],style = {'width': '48vw','display':'inline-block','margin-right': '1vw'}),
                            html.Div(children = [html.H1('Data Description'),data_blurb],style = {'vertical-align' : 'top','width': '48vw','display':'inline-block'})
    ],
             style = {})
]

                        )
    return intro_tab


