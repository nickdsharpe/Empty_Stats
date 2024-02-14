import pandas as pd
import plotly.express as px

teams = ['Hawks', 'Celtics', 'Nets', 'Hornets', 'Bulls', 'Cavaliers', 'Mavericks', 'Nuggets', 'Pistons', 'Warriors', 'Rockets', 'Pacers', 'Clippers', 'Lakers', 'Grizzlies', 'Bucks', 'Heat', 'Timberwolves', 'Pelcans', 'Knicks', 'Thunder', 'Magic', '76ers', 'Suns', 'Kings', 'Spurs', 'Raptors', 'Jazz', 'Wizards', 'Trail Blazers']

def get_creation_data(name, data):
    
    # Grab full team data if necessary, otherwise grab all selected player data
    if name in teams:
        total_data = data[data['team_name'] == name]
        data = data[data['team_name'] == name]
        data = data.dropna(subset=['creator_name'])
    
    else:
        total_data = data[(data['creator_name'] == name) | (data['player_name'] == name)]
        data = data[data['creator_name'] == name]
    
    creation_percentage = round(((len(data) / len(total_data)) * 100),1)
    
    data_hash_map = {}
    ppp_dict = {}
    play_type_hash = {}
    total_ppp = get_ppp(data)
    
    summary = f'Creation %:  {creation_percentage}<br>Total PPP:  {total_ppp}'
    
    for play_type in data['play_type_id']:
        
        if play_type in play_type_hash.keys():
            play_type_hash[play_type] += 1

        else:
            play_type_hash[play_type] = 1
    
    for shooter in data['player_name']:
        shooter = str(shooter)

        if shooter in data_hash_map.keys():
            data_hash_map[shooter] += 1
        else:
            data_hash_map[shooter] = 1
            
    rows_list = []
    
    for play_type in play_type_hash.keys():
        play_type_data = data[data['play_type_id'] == play_type]
        for shooter in play_type_data['player_name']:
            
            player_data = play_type_data[play_type_data['player_name'] == shooter]
            ppp = round((get_ppp(player_data)),2)
            
            new_row = {'play_type_id': play_type, 'shooter': shooter, 'value': 1, 'PPP': ppp}
            
            rows_list.append(new_row)
            
    df = pd.DataFrame(rows_list)
    
    custom_colors = ["#e8554a", "#e8554a", "#e8554a", "#e8554a", "#e8554a", "#e8554a", "#e8554a",'#f0f054', "#52e352", "#52e352", "#52e352", "#52e352", "#52e352", "#52e352", "#52e352"]
    
    fig = px.sunburst(df, path=['play_type_id', 'shooter'], values='value', color='PPP', hover_data=['PPP'],
                      color_continuous_scale=custom_colors,
                      color_continuous_midpoint=0.93)
    fig.update_traces(textinfo='label+percent parent',
                      marker=dict(line=dict(color='white', width=3)))

    fig.update_layout(width=900, height=700, title=dict(text=f"{name} Created Shots", x=0.48, y=0.97), font=dict(size=15, color='black'))
    
    fig.add_annotation(xref='paper', yref='paper', x=0.04, y=1.01, text=summary, showarrow=False, font=dict(color='black', size=15), align='center', bordercolor="black", borderwidth=2, borderpad=7,)
    
    return fig


def get_ppp(data):
    
    points = data['points'].sum()
    fga = data[data['result_id'].isin([1,2,4])]
    fta = data['fta'].sum()
    to = len(data[data['result_id'].isin([5,6])])
    ppp = round((points / ((len(fga)) + (0.44 * fta) + to)),2)

    return ppp
