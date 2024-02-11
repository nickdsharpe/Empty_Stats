import plotly.express as px
import pandas as pd

def get_creation_recipients(player, data):
    
    data = data[data['creator_name'] == player]
    data_hash_map = {}
    ppp_dict = {}
    total_ppp = get_ppp(data)
    
    summary = f'Total PPP:<br>{total_ppp}'

    for shooter in data['player_name']:
        shooter = str(shooter)

        if shooter == 'nan':
            shooter = 'Unassisted'

        if shooter in data_hash_map.keys():
            data_hash_map[shooter] += 1

        else:
            data_hash_map[shooter] = 1

    for shooter in data_hash_map.keys():

        player_data = data[data['player_name'] == shooter]
        player_data = player_data[player_data['creator_name'] == player]

        ppp = get_ppp(player_data)
        ppp_dict[shooter] = ppp

    ppp_df = pd.DataFrame.from_dict(ppp_dict, orient='index')
    data_hash_map_df = pd.DataFrame.from_dict(data_hash_map, orient='index')
    data_hash_map_df = data_hash_map_df.rename(columns={0: 'assists'})
    full_df = pd.concat([data_hash_map_df, ppp_df], axis=1)
    full_df = full_df.rename(columns={0: "PPP"})

    fig = px.pie(full_df, values='assists', names=full_df.index, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(text=full_df['PPP'])
    fig.update_traces(textposition='inside',  textinfo='percent+label+text', textfont_size=18,
                      marker=dict(line=dict(color='#000000', width=3)))

    fig.update_layout(width=1000, height=800, title=dict(text=f"{player} Created Shots", x=0.37, y=0.95), font=dict(size=20, color='black'))
    
    fig.add_annotation(xref='paper', yref='paper', x=-0.08, y=0.95, text=summary, showarrow=False, font=dict(color='black', size=18), align='center', bordercolor="#c7c7c7", borderwidth=2, borderpad=7,)

    return fig

def get_ppp(data):
    
    points = data['points'].sum()
    fga = data[data['result_id'].isin([1,2,4])]
    fta = data['fta'].sum()
    to = len(data[data['result_id'].isin([5,6])])
    ppp = round((points / ((len(fga)) + (0.44 * fta) + to)),2)

    return ppp