import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go

st.title("""VNL 2022 - General Statistics""")

st.markdown("""
* An app with the main goal is to better visualize VNL data from players and teams collected in the official [website of the competition](https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-scorers/) 

*Created by Thais G.*
""")

options = st.sidebar.selectbox(
    "What would you like to verify about VNL 2022?",
    ("General statistics", "Players performance","Perfomance by team", "Brazil performance")
)    
  

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

#st.dataframe(df_scorers)
def players_by_team(df_scorers, sigla):  
    
    players = df_scorers.loc[df_scorers['Team']==sigla]
    
    del players['ShirtNumber']
        
    del players['Team']
    
    st.dataframe(players)

def viz_scorers(df_scorers):
# create trace1 
    trace1 = go.Bar(
                y = df_scorers.Team,
                 x = df_scorers['Attack Points'],
                 name = "Pontos de ataque",
                 orientation='h',
                 marker = dict(color = 'rgba(255, 174, 255, 0.5)',
                              line=dict(color='rgb(0,0,0)',width=2.0)),
                 text = df_scorers['Attack Points'])
# # create trace2 
    trace2 = go.Bar(
                 y = df_scorers.Team,
                 x = df_scorers['Block Points'],
                 name = "Pontos de bloqueio",
                 orientation='h',
                 marker = dict(color = 'rgba(255, 255, 128, 0.5)',
                               line=dict(color='rgb(0,0,0)',width=2.0)),
                text = df_scorers['Block Points'])

# # create trace2 
    trace3 = go.Bar(
                 y = df_scorers.Team,
                 x = df_scorers['Serve Points'],
                 name = "Pontos de saque",
                 orientation='h',
                 marker = dict(color = 'rgba(170, 255, 128, 0.5)',
                               line=dict(color='rgb(0,0,0)',width=2.0)),
                 text = df_scorers['Serve Points'])

    data = [trace1, trace2, trace3]

    layout = go.Layout(barmode="group")

    fig = go.Figure(data = data, layout = layout)

    st.plotly_chart(fig)


def get_df_sets(df_scorers):
    
    df = pd.read_csv("match_results.csv")
    
    df = (df.groupby(['TeamA'])
            .sum()
            .filter(items=['Sets'])
            .append(df.groupby(['TeamB'])
            .sum().filter(items=['Sets'])))
    
    df = (df.reset_index()
            .rename(columns={'index':'Team'}))
    
    df = df.groupby('Team').sum().reset_index()
    
    df = pd.merge(df_scorers, df, on="Team")
    

    
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
        title='[Week 1] - Attacks/Set')
    
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
        title='[Week 1] - Blocks/Set')
    
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
        title='[Week 1] - Serves/Set')
    
    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
   
    
#########
def box_chart_attack(best_attackers):
    
    x_data = ['GER', 'CAN', 'BRA', 
          'JPN', 'POL', 'DOM', 
          'KOR', 'NED', 'BEL',
          'SRB', 'THA', 'USA', 
          'ITA', 'CHN', 'TUR', 
          'BUL']

    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)',
              'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)',
             'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)',
             'rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)',
             'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']

    fig = go.Figure()

    for xd,cls in zip(x_data, colors):
            fig.add_trace(go.Box(
                y=best_attackers[best_attackers.Team == xd]['Success%'],
                name=xd,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=cls,
                marker_size=2,
                line_width=1)
            )

    fig.update_layout(
        font=dict(family='Courier New, monospace', size=12, color='#111111'),
        title='[VNL 2022 - Week 1] - Attack - Success%',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )

    st.plotly_chart(fig)
    
def box_chart_rec(best_receivers):
    x_data = ['GER', 'CAN', 'BRA', 
          'JPN', 'POL', 'DOM', 
          'KOR', 'NED', 'BEL',
          'SRB', 'THA', 'USA', 
          'ITA', 'CHN', 'TUR', 
          'BUL']


#y_data = [y0, y1, y2, y3, y4, y5]
    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)',
              'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)',
             'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)',
             'rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)',
             'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']

    #colors = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

    fig = go.Figure()

    for xd,cls in zip(x_data, colors):
            fig.add_trace(go.Box(
                y=best_receivers[best_receivers.Team == xd]['Success%'],
                name=xd,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.2,
                fillcolor=cls,
                marker_size=2,
                line_width=1)
            )

    fig.update_layout(
        font=dict(family='Courier New, monospace', size=12, color='#111111'),
        title='[VNL 2022 - Week 1] - Reception - Success%',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),

        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )

    st.plotly_chart(fig)


if options == "General statistics":
    
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

    
    new_df = get_df_sets(df_scorers)
    
    st.dataframe(new_df)
    
    #viz_scorers(new_df)

    new_df = get_skills_per_sets(new_df)
    
    st.header("Attacks/sets")
    """
    Each skill (attack, block, serve) by set per team!
    """

    interactive_plot_attack(new_df)

    st.header("Blocks/sets")

    interactive_plot_block(new_df)


    st.header("Serves/sets")

    interactive_plot_serve(new_df)
    
elif options == "Players performance":
    
    st.header("Players performance")
    
    team = st.selectbox(
     'Choose a team to analyse!',
         ('Brazil', 'Türkiye', 'Netherlands','United States','Serbia','Italy','China'))

    st.write('You selected:', team)
    df_scorers = load_scorers()
    
    if team == 'Brazil':
        players_by_team(df_scorers,'BRA')
              
    elif team == 'Türkiye':
        players_by_team(df_scorers,'TUR')
        
    elif team == 'Netherlands':
        players_by_team(df_scorers,'NED')
    
    elif team == 'Serbia':
        players_by_team(df_scorers,'SRB')
          
    elif team == 'Italy':
        players_by_team(df_scorers,'ITA')

    elif team == 'China':
        players_by_team(df_scorers,'CHN')
     
    elif team == 'United States':
        players_by_team(df_scorers,'USA')
        
    
    
elif options == "Perfomance by team":
    
    st.header("Team performance")
    
    best_attackers = pd.read_html("https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-attackers/")[0]
    
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

    
    box_chart_attack(best_attackers)
        
    best_receivers = pd.read_html("https://en.volleyballworld.com/volleyball/competitions/vnl-2022/statistics/women/best-receivers/")[0]
    
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
    
    box_chart_rec(best_receivers)


elif options == "Brazil performance":
    
    st.header("Brazil players")
    
    df_scorers = load_scorers()
    
    players = df_scorers.loc[df_scorers['Team']=='BRA']
    
    del players['ShirtNumber']
        
    del players['Team']
    
    players['Player'] = players['Player'].replace({
        'Duarte Alecrim Diana':'Diana Duarte',
        'Da Silva Ana Carolina': 'Ana Carolina Da Silva',
        'Zalewski Daroit Moreira Priscila' : 'Priscila Daroit',
        'Alexandre Costa Nunes Nyeme Victoria': 'Nyeme Nunes',
        'Silva Carneiro Macris Fernanda':  'Macris Carneiro',
        'Ratzke Roberta Silva':'Roberta Ratzke',
        'Barbosa De Souza Karina':'Karina Barbosa',
        'Menezes Oliveira de Souza Ana Cristina':'Ana Cristina Menezes',
        'Araujo Natália':'Natália Araujo',
        'Viezel Lorena Giovana' : 'Lorena Viezel',
        'Nascimento Kisy' : 'Kisy Nascimento',
        'Bergmann Julia Isabelle':'Julia Bergmann',
        'Araujo De Souza Mayany Cristina':'Mayany Cristina',
        'Geraldo Teixeira Lorenne':'Lorenne Teixeira'
    })
      
    st.dataframe(players)
    

with scoring_table:
    
    # General scoring table - by TEAM
    df_scorers = load_scorers()
    df_scorers = get_df_sets(df_scorers)
    
    st.title("A closer look to the teams scoring by skill")
    
    fig = go.Figure(
        data = go.Table(header = dict(values=df_scorers.columns.tolist(), fill_color='#F24C4C', align='center'), 
                        cells = dict(values=[df_scorers.Team, df_scorers['Attack Points'],
                                            df_scorers['Block Points'], df_scorers['Serve Points'], df_scorers['Sets']],
                                    fill_color='#F9F9F9', align='left'))
    )
    
    fig.update_layout(margin=dict(l=5, r=5, b= 10, t=10), paper_bgcolor=background_color)
    
    st.write(fig)
    