
def style_mix(*style_list):
    res = {}
    for style in style_list:
        res = {**res, **style}

    return res

theme={
    "background_color": "#242f2f",
    "box_color": "#040f0f",
    "primary_color": "#248232",
    "secondary_color": "#2ba84a",
    "font_color": "#fcfffc"
}
theme2 = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}
plotly_layout={
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': theme["box_color"],
    'font': {
        'color': "white"}}

def grid_row():
    return({"display": "flex", "flex-flow": "row nowrap"})

def grid_column():
    return({"display": "flex", "flex-flow": "column nowrap", "justify-content": "space-around"})

def box(n):
    return({"flex": n})

basic = {
    'padding': 10, 
    "margin": 10,
    "color": "white",
    "font-family": "verdana",
    "font-size": "110%"}

daq_label = {
    "color": "white",
    "left": "0px",
    "width": "100%",
    "font-size": "105%",}

body = {'display': 'flex', 
        'flex-flow': 'row nowrap', 
        "width": "100%", 
        # "height": "96vh",
        "height": "96vh",
        "background-color": theme['background_color']
        }