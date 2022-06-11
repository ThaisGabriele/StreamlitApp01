import streamlit as st
import pandas as pd

# interactive plots
#import plotly.express as px
#import plotly.graph_objs as go

#from st_aggrid import AgGrid

st.set_page_config(layout="wide")


header = st.container()
team_details = st.container()

#with open('style.css') as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
   
@st.cache
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

    #AgGrid(df)
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
    #AgGrid(players)
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

def page_config():
    st.set_page_config(layout="wide")
        
#### Starts here!

with header:
    st.title("Welcome to my VNL 2022 app!")
    st.text("Another way to check the numbers from the competition - team by team")
    st.markdown("""
    *All data collected from the [official website of the competition](https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-scorers/)* 
    """)

    
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
              
    
    
