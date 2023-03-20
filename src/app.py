from dash import dash, html, dcc, dash_table, Input, Output
from datetime import date
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go


data = pd.read_csv('https://raw.githubusercontent.com/UBC-MDS/OlymPulse/main/data/clean/olympic_clean.csv')
data = data.drop(columns=['id','name','noc','games'])
# data = df.dropna()
# data['year'] =pd.to_numeric(data['year'])

def df_filtering(data_original,cntry,mdl,yr,sprt):
    df_filtered = data_original.copy()
    if type(cntry)!= list:
        df_filtered = df_filtered[(df_filtered['medal'].isin(mdl)) &
                              (df_filtered['team'].isin([cntry]))]
    else:
        df_filtered = df_filtered[(df_filtered['medal'].isin(mdl)) &
                              (df_filtered['team'].isin(cntry))]
        
    
    df_filtered = df_filtered[(df_filtered['year'] >= yr[0]) &
                              (df_filtered['year'] <= yr[1])]
  
    if type(sprt)!= list:
        df_filtered = df_filtered[(df_filtered['sport'].isin([sprt]))]
    else:
        df_filtered = df_filtered[(df_filtered['sport'].isin(sprt))]
        
    df_filtered = df_filtered.rename(columns = {'age':'Age',
                                                'height':'Height',
                                                'weight':'Weight'})
      
    
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
                            multi=True,
                            value = 'Canada' ,
                            placeholder='Select a country'),
            ]
        ),
       html.Br(),
       
       html.Div(
            [
                html.Label(['Select Sport'],style={'font-weight': 'bold', "text-align": "center"}),
                dcc.Dropdown(id='dd_sport',
                            options=np.sort(data['sport'].unique()),
                            multi=True,
                            value = 'Ice Hockey' ,
                            placeholder='Select a sport'),
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
        html.H1('OlympicDash', style={'color': 'black', 'fontSize': 60,'textAlign':'center','fontFace':'bold'}),
        html.Br(),
        html.H3('Olympic Medal Stats by Demographics',style={'color': 'blue', 'fontSize': 30,'textAlign':'center'}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls,width=3),
                dbc.Col(dcc.Graph(id='barchart'), width=9),
            ],
            align="center",
        ),
        
        html.Hr(),
        
        dbc.Row(
            [
                
                dbc.Col(dcc.Graph(id = 'hist'),width={"size": 9,"offset":3} )
                
            ],
            align="center",
        ),
        
                      
        dbc.Row(
            [
                dbc.Col([dcc.Dropdown(id='dd_xcol',
                            options=['Age','Height','Weight'],
                            value = 'Age',
                            placeholder='Select a demographic')],width={"size": 5, "offset": 5}
                         )],
                align='center'
        ),
        
        html.Hr(),
        
        dbc.Row(
            [
                
                dbc.Col(dcc.Graph(id = 'line'),width={"size": 9,"offset":3} )
                
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
        Input('year_slider', 'value'),
        Input('dd_sport', 'value'))

    
def update_barchart(country,medal_type,year,sport):
   
    df_filtered = df_filtering(data,country,medal_type,year,sport)
    df_grouped = df_filtered[['team','medal','sex','event','sport']].groupby(['team','medal','sex','sport']).count().reset_index().rename(columns={'event':'Count',
                                                                                                                                     'team':'Country',
                                                                                                                                     'medal':'Medal',
                                                                                                                                     'sex':'Sex',
                                                                                                                                     'sport':'Sport'})
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
                       hover_data=['Country','Sport'],
                       labels={'Count':'No. of medals'},
                       category_orders={"Medal": ["Gold", "Silver", "Bronze"]},
                       barmode='group',
                       title='Medal Count by Sex',
                       facet_col=  "Country",
                       text = 'Sport'
                       )

    bar_chart.update_layout(showlegend=True,title_x = 0.5,title_font_size=25,title_font_family="Arial Black")

    return bar_chart


@app.callback(
        Output('hist', 'figure'),
        Input('dd_countries', 'value'),
        Input('medals_checkbox', 'value'),
        Input('year_slider', 'value'),
        Input('dd_sport', 'value'),
        Input('dd_xcol', 'value'))
    
def update_hist(country,medal_type,year,sport,xcol):
    df_filtered = df_filtering(data,country,medal_type,year,sport)
    
    df_grouped = df_filtered[[xcol,'medal','event','sex','team','sport']].dropna().groupby([xcol,'medal','sex','team','sport']).count().reset_index().rename(columns={'event':'Count',
                                                                                                                                     'medal':'Medal',
                                                                                                                                     'sex':'Sex',
                                                                                                                                     'team':'Country',
                                                                                                                                     'sport':'Sport'})
    
    
    
    hist = px.histogram(data_frame = df_grouped,
                       x=xcol,
                       y='Count',
                       color= 'Sex',
                       opacity=0.6,
                       color_discrete_sequence=['green','red'], 
                        labels={'Height':'Height (cm)','Weight':'Weight (kgs)','Age':'Age (yrs)'},
                       title=f'{xcol.capitalize()} vs Count of Medals',
                       facet_col ='Country'
                       )
    # bar_chart.layout.update(showlegend=True,
    #                         title={'font': {'size': 20},'textAlign':'center'}) 
    hist.update_layout(showlegend=True,title_x = 0.5,title_font_size=25,title_font_family="Arial Black",yaxis_title="No. of Medals")
    hist.update_traces(marker_line_width=1,marker_line_color="black")
    # hist.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of", "")))


    return hist


@app.callback(
        Output('line', 'figure'),
        Input('dd_countries', 'value'),
        Input('medals_checkbox', 'value'),
        Input('year_slider', 'value'),
        Input('dd_sport', 'value'))
    
def update_line(country,medal_type,year,sport):
    df_filtered = df_filtering(data,country,medal_type,year,sport)
    
    df_grouped = df_filtered[['event','sex','year','team','sport']].dropna().groupby(['year','sex','team','sport']).count().reset_index().rename(columns={'event':'Count',
                                                                                                                            'sex':'Sex',
                                                                                                                            'year':'Year',
                                                                                                                            'team':'Country',
                                                                                                                            'sport':'Sport'})
    
    
    
    line = px.line(data_frame = df_grouped,
                       x='Year',
                       y='Count',
                       color= 'Sex',
                       labels={'Height':'Height (cm)','Weight':'Weight (kgs)','Age':'Age (yrs)'},
                       title=f'Trend in Count of Medals by Sex',
                       facet_col ='Country'
                       )
    
    line.update_layout(showlegend=True,title_x = 0.5,title_font_size=25,title_font_family="Arial Black",yaxis_title="No. of Medals")
    line.update_traces(marker_line_width=1,marker_line_color="black")
    #line.update_layout(xaxis=dict(tickmode='array', tickvals=df_grouped['Year'][::4]))
    # hist.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("sum of", "")))


    return line
if __name__ == '__main__':
    app.run_server(debug=True)