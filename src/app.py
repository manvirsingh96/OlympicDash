from dash import dash, html, dcc, dash_table, Input, Output
from datetime import date
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go


data = pd.read_csv('https://raw.githubusercontent.com/UBC-MDS/OlymPulse/main/data/clean/olympic_clean.csv')
# data = df.drop(columns=['id','name','sex','age','height','weight'])
# data = df.dropna()
# data['year'] =pd.to_numeric(data['year'])

def df_filtering(data_original,cntry,mdl,yr):
    df_filtered = data_original.copy()
    if type(cntry)!= list:
        df_filtered = df_filtered[(df_filtered['medal'].isin(mdl)) &
                              (df_filtered['team'].isin([cntry]))]
    else:
        df_filtered = df_filtered[(df_filtered['medal'].isin(mdl)) &
                              (df_filtered['team'].isin(cntry))]
        
    
    df_filtered = df_filtered[(df_filtered['year'] >= yr[0]) &
                              (df_filtered['year'] <= yr[1])]
    return df_filtered
    
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

server = app.server

controls = dbc.Card(
    [
        html.Div(
            [
                html.Label(['Select Year Range'],style={'font-weight': 'bold', "text-align": "center"}),
                dcc.RangeSlider(id='year_slider', 
                                min= data['year'].min(),
                                max= data['year'].max(),
                                marks={int(data['year'].min()):f"{data['year'].min()}",
                                        int(data['year'].max()):f"{data['year'].max()}"},
                                value=[data['year'].min(), data['year'].max()]),
            ]
        ),
        
        html.Br(),
        
        html.Div(
            [
                html.Label(['Select Country'],style={'font-weight': 'bold', "text-align": "center"}),
                dcc.Dropdown(id='dd_countries',
                            options=np.sort(data['team'].unique()),
                            value = 'Canada' ,
                            placeholder='Select a country'),
            ]
        ),
       html.Br(),
        
       html.Div(
            [
                html.Label(['Select Medal Type'],style={'font-weight': 'bold', "text-align": "left"}),
                dcc.Checklist(id='medals_checkbox',
                            options=np.sort(data['medal'].unique()),
                            value=['Gold','Silver','Bronze'],
                            labelStyle={'display': 'block','text-align':'left'}),
            ]
        ),
    ],
    body=True,
)


app.layout = dbc.Container(
    [
        html.H1('OlymPulse', style={'color': 'black', 'fontSize': 60,'textAlign':'center','fontFace':'bold'}),
        html.Br(),
        html.H3('Stats about teams in the Olympics',style={'color': 'blue', 'fontSize': 30,'textAlign':'center'}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls,width=3),
                dbc.Col(dcc.Graph(id='barchart'), width=9),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id = 'age_hist'),width=4),
                dbc.Col(dcc.Graph(id='height_hist'), width=4),
                dbc.Col(dcc.Graph(id='weight_hist'), width=4)
            ],
            align="center",
        ),
    ],
    fluid=True,
)


    # dcc.DatePickerRange(id='Year', min_date_allowed=data['year'].min(),
    #     max_date_allowed=(data['year'].max())),
@app.callback(
        Output('barchart', 'figure'),
        Input('dd_countries', 'value'),
        Input('medals_checkbox', 'value'),
        Input('year_slider', 'value'))
    
def update_barchart(country,medal_type,year):
   
    df_filtered = df_filtering(data,country,medal_type,year)
    df_grouped = df_filtered[['team','medal','sex','event']].groupby(['team','medal','sex']).count().reset_index().rename(columns={'event':'Count',
                                                                                                                                     'team':'Country',
                                                                                                                                     'medal':'Medal',
                                                                                                                                     'sex':'Sex'})
    # bar_chart = alt.Chart(df_filtered).mark_bar().encode(
    #     y= alt.Y('medal',title='Medal Type'),
    #     x=alt.X ('count()',title='No. of medals'),
    #     color = alt.Color('medal'),
    #     tooltip = [alt.Tooltip('team',title = "Country"),
    #                alt.Tooltip('medal',title = "Medal Type"),
    #                alt.Tooltip('count()',title = "Medals") ]).interactive()
    bar_chart = px.bar(data_frame = df_grouped,
                       x='Medal',
                       y='Count',
                       color= 'Sex',
                       hover_data=['Country'],
                       labels={'Count':'No. of medals'},
                       category_orders={"Medal": ["Gold", "Silver", "Bronze"]},
                       barmode='group',
                       title='Medal Count by Sex',
                       facet_col=  "Country"
                       )

    bar_chart.update_layout(showlegend=True,title_x = 0.5,title_font_size=30,title_font_family="Arial Black")

    return bar_chart


@app.callback(
        Output('age_hist', 'figure'),
        Input('dd_countries', 'value'),
        Input('medals_checkbox', 'value'),
        Input('year_slider', 'value'))
    
def update_agehist(country,medal_type,year):
    df_filtered = df_filtering(data,country,medal_type,year)
    
    df_grouped = df_filtered[['age','medal','event','sex']].dropna().groupby(['age','medal','sex']).count().reset_index().rename(columns={'event':'Count',
                                                                                                                                     'medal':'Medal',
                                                                                                                                     'age':'Age',
                                                                                                                                     'sex':'Sex'})
    
    # df_grouped = df_filtered[['age','medal']].dropna().groupby(['age']).count().reset_index().rename(columns={'medal':'Count','age':'Age'})
    
    
    hist_age = px.histogram(data_frame = df_grouped,
                       x='Age',
                       y='Count',
                      color= 'Sex',
                        opacity=0.6,
                    color_discrete_sequence=['green','red'], 
                       labels={'Count':'No. of medals'},
                       title='Age vs Count of Medals'
                       )
    # bar_chart.layout.update(showlegend=True,
    #                         title={'font': {'size': 20},'textAlign':'center'}) 
    hist_age.update_layout(showlegend=False,title_x = 0.5,title_font_size=20,title_font_family="Arial Black")
    hist_age.update_traces(marker_line_width=1,marker_line_color="black")
    hist_age.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of", "")))


    return hist_age


@app.callback(
        Output('height_hist', 'figure'),
        Input('dd_countries', 'value'),
        Input('medals_checkbox', 'value'),
        Input('year_slider', 'value'))
    
def update_heighthist(country,medal_type,year):
    df_filtered = df_filtering(data,country,medal_type,year)
    
    df_grouped = df_filtered[['height','medal','event','sex']].dropna().groupby(['height','medal','sex']).count().reset_index().rename(columns={'event':'Count',
                                                                                                                                     'medal':'Medal',
                                                                                                                                     'height':'Height',
                                                                                                                                     'sex':'Sex'})
    
    # df_grouped = df_filtered[['age','medal']].dropna().groupby(['age']).count().reset_index().rename(columns={'medal':'Count','age':'Age'})
    
    
    hist_height = px.histogram(data_frame = df_grouped,
                       x='Height',
                       y='Count',
                       color= 'Sex',
                        opacity=0.6,
                    color_discrete_sequence=['green','red'], 
                       labels={'Count':'No. of medals'},
                       title='Height vs Count of Medals'
                       )
    # bar_chart.layout.update(showlegend=True,
    #                         title={'font': {'size': 20},'textAlign':'center'}) 
    hist_height.update_layout(showlegend=False,title_x = 0.5,title_font_size=20,title_font_family="Arial Black")
    hist_height.update_traces(marker_line_width=1,marker_line_color="black")
    hist_height.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of", "")))


    return hist_height

@app.callback(
        Output('weight_hist', 'figure'),
        Input('dd_countries', 'value'),
        Input('medals_checkbox', 'value'),
        Input('year_slider', 'value'))
    
def update_weighthist(country,medal_type,year):
    df_filtered = df_filtering(data,country,medal_type,year)
    
    df_grouped = df_filtered[['weight','medal','event','sex']].dropna().groupby(['weight','medal','sex']).count().reset_index().rename(columns={'event':'Count',
                                                                                                                                     'medal':'Medal',
                                                                                                                                     'weight':'Weight',
                                                                                                                                     'sex':'Sex'})
    
    # df_grouped = df_filtered[['age','medal']].dropna().groupby(['age']).count().reset_index().rename(columns={'medal':'Count','age':'Age'})
    
    
    hist_weight = px.histogram(data_frame = df_grouped,
                       x='Weight',
                       y='Count',
                        color= 'Sex',
                        opacity=0.6,
                    color_discrete_sequence=['green','red'], 
                       labels={'Count':'No. of medals'},
                       title='Weight vs Count of Medals'
                       )
    # bar_chart.layout.update(showlegend=True,
    #                         title={'font': {'size': 20},'textAlign':'center'}) 
    hist_weight.update_layout(showlegend=True,title_x = 0.5,title_font_size=20,title_font_family="Arial Black")
    hist_weight.update_traces(marker_line_width=1,marker_line_color="black")
    hist_weight.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of", "")))


    return hist_weight

if __name__ == '__main__':
    app.run_server(debug=True)