import streamlit as st
import pandas as pd

# interactive plots
import plotly.express as px
import plotly.graph_objs as go

#from st_aggrid import AgGrid
st.set_page_config(layout="centered")


header = st.container()
team_ranking, team_details = st.tabs(['Teams general', 'Teams Details'])

# CSS for tables

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>   """

center_heading_text = """
    <style>
        .col_heading   {text-align: center !important}
    </style>          """
    
center_row_text = """
    <style>
        td  {text-align: center !important}
    </style>      """

# Inject CSS with Markdown

st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.markdown(center_heading_text, unsafe_allow_html=True) 
st.markdown(center_row_text, unsafe_allow_html=True) 

heading_properties = [('font-size', '16px'),('text-align', 'center'),
                      ('color', '#353b3c'),  ('font-weight', 'bold'),
                      ('background', '#a4bfeb'),('border', '0.8px solid')]

cell_properties = [('font-size', '16px'),('text-align', 'center')]

dfstyle = [{"selector": "th", "props": heading_properties},
               {"selector": "td", "props": cell_properties}]

# Expander Styling

st.markdown(
    """
<style>
.streamlit-expanderHeader {
 #   font-weight: bold;
    background: gray;
    font-size: 18px;
}
</style>
""",
    unsafe_allow_html=True,
)
    
def color_metrics_perc(val):
    if val >= 40.0:
        color = '#95ecb0'
    elif val < 40.0 and val > 35.0:
        color = '#ffef9f'
    else:
        color = '#ffe5ec'
    
    return 'background-color: %s' % color

def color_metrics_ef(val):
    if val >= 30.0:
        color = '#174d2e'
    else:
        color = '#6b1c1c'
    
    return 'background-color: %s' % color


#with open('style.css') as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
def get_df_sets(df_scorers):
    
    standings = pd.read_html("https://en.volleyballworld.com/volleyball/competitions/vnl-2022/standings/women/#advanced")
    
    df1 = standings[0]['Unnamed: 1_level_0']
    
    df1.rename(columns= {'Unnamed: 1_level_1':'Team'}, inplace=True)
    
    df2 = standings[0]['Sets']
    
    del df2['Set Ratio']
    
    res = pd.concat([df1, df2], axis=1)
    
    res['Team'] = res['Team'].apply(lambda row : row[0:-3])
    
    res = res.assign(Sets = lambda n : n['Won'] + n['Lost'])
    
    #st.dataframe(res)
    
    res = res.filter(['Team','Sets'])
    
    df = pd.merge(df_scorers, res, on="Team")
      
    return df

def get_skills_per_sets(teams):
    
    attack_per_set = lambda x : round((teams['Attack Points'] / teams['Sets']),1)
    block_per_set = lambda x : round((teams['Block Points'] / teams['Sets']),1)
    serve_per_set = lambda x : round((teams['Serve Points'] / teams['Sets']),1)
    
    teams['AttackPerSet'] = attack_per_set('AttackPerSet')
    teams['BlockPerSet'] = block_per_set('BlockPerSet')
    teams['ServePerSet'] = serve_per_set('ServePerSet')
    
    return teams

           
def interactive_plot_attack(teams):
    
    teams = teams.sort_values("AttackPerSet", ascending=False).head(10)
    
    st.markdown(""" **General Stats** """)
    st.dataframe(teams)

    trace1 = go.Bar(
                y = teams.AttackPerSet,
                x = teams.Team,
                name = "Attack",
                marker = dict(color = 'rgba(255, 174, 255, 0.5)',
                             line=dict(color='rgb(0,0,0)',width=1.9)),
                text = teams.AttackPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Attacks/Set')
    
    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
    


def interactive_plot_block(teams):
    
    
    #plot = px.bar(teams.sort_values("BlockPerSet"), x='BlockPerSet', y = 'Team')
    teams = teams.sort_values("BlockPerSet", ascending=False).head(10)
    
    
    # create trace2 
    trace1 = go.Bar(
                    y = teams.BlockPerSet,
                    x = teams.Team,
                    name = "Block",
                    marker = dict(color = 'rgba(255, 255, 128, 0.5)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.BlockPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Blocks/Set')
    
    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
    
def interactive_plot_serve(teams):
    
    teams = teams.sort_values("ServePerSet", ascending=False).head(10)
    # create trace2 
    trace1 = go.Bar(
                    y = teams.ServePerSet,
                    x = teams.Team,
                    name = "Serve",
                    marker = dict(color = 'rgba(170, 255, 128, 0.5)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.ServePerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Serves/Set')
    
    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)


# -------------


def load_scorers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-scorers/"
    
    best_scorers = pd.read_html(url)
    
    best_scorers = best_scorers[0]
    
    best_scorers = best_scorers.rename(columns={
                'Shirt NumberShirt': 'ShirtNumber',
                'Player NamePlayer':'Player', 
                'TeamTeam':'Team',
                'Attack PointsA Pts':'Attack Points', 
                'Block PointsB Pts':'Block Points', 
                'Serve PointsS Pts':'Serve Points',
                'PointsPts':'Total Points'
    })
    
    return best_scorers

def get_attackers(sigla):
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-attackers/"
    
    best_attackers = pd.read_html(url)[0]
    
    best_attackers = best_attackers.rename(columns={
        'Shirt NumberShirt': 'ShirtNumber',
        'Player NamePlayer':'PlayerName', 
        'TeamTeam':'Team',
        'Pointsattacks':'AttackPoints',
        'ErrorsSE':'Errors', 
        'Attemptsshots':'AttemptsShots',
        'Average per matchaverage-per-match':'AveragePerMatch', 
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    
    df = best_attackers.loc[(best_attackers['Team']==sigla)& (best_attackers['TotalAttempts'] > 0)]

    df = df.drop(columns=['ShirtNumber','Team'])


    df = (df.style.set_properties(**{'background': 'white', 'border': '0.5px solid'})
                  .set_table_styles(dfstyle)
                  .applymap(color_metrics_perc, subset=pd.IndexSlice[:, ['Success%']])
    )
    #AgGrid(df, width=890)
    st.dataframe(df)

def get_receivers(sigla):
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-receivers/"
    
    best_receivers = pd.read_html(url)[0]
    
    best_receivers = best_receivers.rename(columns={
        'Shirt NumberShirt': 'ShirtNumber',
        'Player NamePlayer':'PlayerName', 
        'TeamTeam':'Team',
         'SuccesfulSuccesful':'Sucessful',
        'ErrorsSE':'Errors', 
        'AttempsAtt':'Attempts',
        'Average per matchaverage-per-match':'AveragePerMatch',
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    
    })
    
    df = best_receivers.loc[(best_receivers['Team'] == sigla) & (best_receivers['TotalAttempts'] > 0)]
    
    df = df.drop(columns=['ShirtNumber','Team'])
    #AgGrid(df)
    st.dataframe(df)
    
def get_diggers(sigla):
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-diggers/"
    
    best_diggers = pd.read_html(url)[0]
    
    best_diggers = best_diggers.rename(columns={
        'Shirt NumberShirt': 'ShirtNumber',
        'Player NamePlayer':'PlayerName', 
        'TeamTeam':'Team',
        'SuccessfulSuccessful':'Sucessful',
        'Digsgreat-save':'Digs',
        'ErrorsSE':'Errors', 
        'ReceptionsRec':'Receptions',
        'Average per matchaverage-per-match':'AveragePerMatch',
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    
    df = best_diggers.loc[(best_diggers['Team'] == sigla) & (best_diggers['TotalAttempts'] > 0)]
    
    df = df.drop(columns=['ShirtNumber','Team'])
    #AgGrid(df)
    st.dataframe(df)

    
def get_blockers(sigla):
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-blockers/"
    
    best_blockers = pd.read_html(url)[0]
    
    best_blockers = best_blockers.rename(columns={
         'Shirt NumberShirt':'ShirtNumber', 
         'Player NamePlayer':'PlayerName', 
         'TeamTeam':'Team',
         'Blocksstuff-blocks':'Blocks', 
         'ErrorsSE': 'Errors', 
         'ReboundsREB':'Rebounds',
         'Average per matchaverage-per-match': 'AveragePerMatch', 
         'Efficiency %Eff':'Efficiency%', 
         'TotalTA':'TotalAttempts'
    })
    df = best_blockers.loc[(best_blockers['Team']==sigla) & (best_blockers['TotalAttempts'] > 0)]
    
    df = df.drop(columns=['ShirtNumber','Team'])
    #AgGrid(df)
    st.dataframe(df)

def get_servers(sigla):
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-servers/"
    
    best_servers = pd.read_html(url)[0]
    
    best_servers = best_servers.rename(columns={
        'Shirt NumberShirt': 'ShirtNumber',
        'Player NamePlayer':'PlayerName', 
        'TeamTeam':'Team',
        'Pointsserve-points': 'ServePoints',
        'ErrorsSE':'Errors', 
        'AttempsAtt':'Attempts',
        'Average per matchaverage-per-match':'AveragePerMatch', 
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    df = best_servers.loc[(best_servers['Team']==sigla) & (best_servers['TotalAttempts'] > 0)]
    
    df = df.drop(columns=['ShirtNumber','Team'])        
    #AgGrid(df)
    st.dataframe(df)

def players_by_team(df_scorers, sigla):  
    
    players = df_scorers.loc[df_scorers['Team']==sigla]
    
    
    del players['ShirtNumber']
        
    st.markdown(""" **Team Stats** """)
    team_totals = players.groupby("Team").sum()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Points", team_totals['Total Points'])
    col2.metric("Attack Points", team_totals['Attack Points'])
    col3.metric("Block Points", team_totals['Block Points'])
    col4.metric("Serve Points", team_totals['Serve Points'])

    st.markdown(""" **Players Stats** """)
    del players['Team']
    #AgGrid(players,width=780)
    st.dataframe(players)

def show_skill_tables(code):
    
    st.markdown(""" **Attacking** """)
    get_attackers(code)
    
    st.markdown(""" **Reception** """)
    get_receivers(code)
    
    st.markdown(""" **Diggers** """)
    get_diggers(code)
        
    st.markdown(""" **Blocking** """)
    get_blockers(code)
    
    st.markdown(""" **Serving** """)
    get_servers(code)

    

#def page_config():
 #   st.set_page_config(layout="centered")
        
#### Starts here!

with header:
    st.title("Welcome to my VNL 2022 app!")
    st.text("Another way to check the numbers from the competition - team by team")
    st.markdown("""
    *All data collected from the [official website of the competition](https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-scorers/)* 
    """)

    
with team_ranking:
   # st.markdown(""" **Team Details** """)

    
    df_scorers = load_scorers()
    
    df_scorers = df_scorers.filter(items=['Team', 'Attack Points','Block Points', 'Serve Points']).groupby("Team").sum()

    df_scorers = df_scorers.reset_index()
    
    df_scorers['Team'] = df_scorers['Team'].replace({
                                            'THA':'Thailand',
                                            'BUL':'Bulgaria',
                                            'TUR':'Türkiye',
                                            'ITA':'Italy',
                                            'BRA':'Brazil',
                                            'GER':'Germany',
                                            'DOM':'Dominican Republic',
                                            'USA':'United States',
                                            'NED':'Netherlands',
                                            'CHN':'China',
                                            'BEL':'Belgium',
                                            'SRB':'Serbia',
                                            'CAN':'Canada',
                                            'POL':'Poland',
                                            'JPN':'Japan',
                                            'KOR':'Korea'
    })
    
    
    df_scorers = get_df_sets(df_scorers)

    new_df = get_skills_per_sets(df_scorers)

    #st.header("Attacks/sets")

    interactive_plot_attack(new_df)

    #st.header("Blocks/sets")

    interactive_plot_block(new_df)

    #st.header("Serves/sets")

    interactive_plot_serve(new_df)   
    
with team_details:
    
    st.title("Choose a team: ")
    
    team = st.selectbox(
     '',
         ('Belgium', 'Brazil', 'Bulgaria', 'Canada', 'China', 'Dominican Republic',
          'Germany', 'Italy', 'Japan','Korea', 'Netherlands','Poland', 'Serbia','Thailand', 'Türkiye','United States',
         ))

    st.write('You selected:', team)
    df_scorers = load_scorers()
    
    if team == 'Brazil':
        code = 'BRA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Belgium':
        code = 'BEL' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Bulgaria':
        code = 'BUL' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    
    elif team == 'Canada':
        code = 'CAN' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)    

    elif team == 'China':
        code = 'CHN' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    
    elif team == 'Dominican Republic':
        code = 'DOM' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)

    elif team == 'Germany':
        code = 'GER' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    
    elif team == 'Italy':
        code = 'ITA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
   
    elif team == 'Japan':
        code = 'JPN' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Korea':
        code = 'KOR' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)    

        
    elif team == 'Netherlands':
        code = 'NED' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Poland':
        code = 'POL' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
                         
    
    elif team == 'Serbia':
        code = 'SRB' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Thailand':
        code = 'THA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
                         

    elif team == 'Türkiye':
        code = 'TUR' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
              
    elif team == 'United States':
        code = 'USA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
              
    
    
