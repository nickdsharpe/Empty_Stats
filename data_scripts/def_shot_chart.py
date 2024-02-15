import pandas as pd
import numpy as np
import seaborn as sns
from plotly.subplots import make_subplots
np.seterr(invalid='ignore')
from plotly_court import draw_plotly_court
from mpl_court import create_court
import plotly.figure_factory as ff
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import plotly.graph_objects as go

def get_def_shot_chart(name, data, play_type='TOTAL', save=False):
    
    data = data[data['defender_name'] == name]
    
    shots = [(pair, z) for pair, z in zip(zip(data['event_x'], data['event_y']), data['result_id'])]
    
    # Calculate PPP and SQ
    shooting_ppp = get_ppp(data)
    shooting_fga = data[data['result_id'].isin([1,2,4])]
    shooting_sq = round((data['shot_quality_id'].sum() / len(shooting_fga)),1)

    creation_ppp = get_ppp(data)
    creation_fga = data[data['result_id'].isin([1,2,4])]
    creation_sq = round((data['shot_quality_id'].sum() / len(creation_fga)),1)

    total_points = data['points'].sum()
    total_fga = data[data['result_id'].isin([1,2,4])]
    total_fta = data['fta'].sum()
    total_to = len(data[data['result_id'].isin([5,6])])
    total_ppp = round((total_points / ((len(total_fga)) + (0.44 * total_fta) + total_to)),2)
    total_ts = round(((total_points / (2 * ((len(total_fga) + (0.44 * total_fta) + total_to)))) * 100),1)
    total_sq = round((data['shot_quality_id'].sum() / len(total_fga)),1)
    ftr = round((total_fta / len(total_fga)),2)

    # Calculate True Shooting
    shooting_ts = get_ts(data)
    creation_ts = get_ts(data)

    # Three point percentage and shot quality
    total_three_point_fga = data[data['shot_zone_id'].isin(['3ptZ1', '3ptZ2', '3ptZ3', '3ptZ4', '3ptZ5'])]
    total_three_point_fg_per = round(((len(total_three_point_fga[total_three_point_fga['result_id'] == 1]) / len(total_three_point_fga)) *100),1)
    total_three_point_fg_SQ = round((total_three_point_fga['shot_quality_id'].sum() / len(total_three_point_fga)),1)

    shooting_three_point_fga = data[data['shot_zone_id'].isin(['3ptZ1', '3ptZ2', '3ptZ3', '3ptZ4', '3ptZ5'])]
    shooting_three_point_fg_per = round(((len(shooting_three_point_fga[shooting_three_point_fga['result_id'] == 1]) / len(shooting_three_point_fga)) *100),1)
    shooting_three_point_fg_SQ = round((shooting_three_point_fga['shot_quality_id'].sum() / len(shooting_three_point_fga)),1)

    creation_three_point_fga = data[data['shot_zone_id'].isin(['3ptZ1', '3ptZ2', '3ptZ3', '3ptZ4', '3ptZ5'])]
    creation_three_point_fg_per = round(((len(creation_three_point_fga[creation_three_point_fga['result_id'] == 1]) / len(creation_three_point_fga)) *100),1)
    creation_three_point_fg_SQ = round((creation_three_point_fga['shot_quality_id'].sum() / len(creation_three_point_fga)),1)

    # Turnover Percentage
    to_per = round(((total_to / (len(total_fga) + (0.475 * total_fta) + total_to)) * 100),1)

    # Rim PPP
    rim_data = data[data['shot_zone_id'] == 'Rim']
    rim_points = rim_data['points'].sum()
    rim_fga = rim_data[rim_data['result_id'].isin([1,2,4])]
    rim_fta = rim_data['fta'].sum()
    rim_to = len(rim_data[rim_data['result_id'].isin([5,6])])
    rim_ppp = round((rim_points / (len(rim_fga) + (0.44 * rim_fta) + rim_to)),2)

    # Rim Stats
    rim_ts = get_ts(rim_data)
    rim_sq = round((rim_data['shot_quality_id'].sum() / len(rim_fga)),2)

    # Most frequent play type
    play_types_df = get_freq(data)
    most_freq_df = play_types_df.sort_values('freq', ascending=False)
    most_freq_play_type = most_freq_df['play_type'].iloc[0]
    most_freq_play_type_freq = most_freq_df['freq'].iloc[0]
    most_freq_ppp = most_freq_df['ppp'].iloc[0]

    # 2nd Most frequent play type
    second_most_freq_play_type = most_freq_df['play_type'].iloc[1]
    second_most_freq_play_type_freq = most_freq_df['freq'].iloc[1]
    second_most_freq_ppp = most_freq_df['ppp'].iloc[1]

    # 3rd Most frequent play type
    third_most_freq_play_type = most_freq_df['play_type'].iloc[2]
    third_most_freq_play_type_freq = most_freq_df['freq'].iloc[2]
    third_most_freq_ppp = most_freq_df['ppp'].iloc[2]

    # Best Play Type
    best_df = play_types_df.sort_values('ppp', ascending=True)
    best_df = best_df[best_df['freq'] >= 5]
    best_play_type = best_df['play_type'].iloc[0]
    best_play_type_ppp = best_df['ppp'].iloc[0]
    best_play_type_freq = best_df['freq'].iloc[0]

    # 2nd Best Play Type
    second_best_play_type = best_df['play_type'].iloc[1]
    second_best_play_type_ppp = best_df['ppp'].iloc[1]
    second_best_play_type_freq = best_df['freq'].iloc[1]

    # 3rd Best Play Type
    third_best_play_type = best_df['play_type'].iloc[2]
    third_best_play_type_ppp = best_df['ppp'].iloc[2]
    third_best_play_type_freq = best_df['freq'].iloc[2]

    # Worst Play Type
    worst_df = play_types_df.sort_values('ppp', ascending=False)
    worst_df = worst_df[worst_df['freq'] >= 5]
    worst_play_type = worst_df['play_type'].iloc[0]
    worst_play_type_ppp = worst_df['ppp'].iloc[0]
    worst_play_type_freq = worst_df['freq'].iloc[0]

    # 2nd Worst Play Type
    second_worst_play_type = worst_df['play_type'].iloc[1]
    second_worst_play_type_ppp = worst_df['ppp'].iloc[1]
    second_worst_play_type_freq = worst_df['freq'].iloc[1]

    # 3rd Worst Play Type
    third_worst_play_type = worst_df['play_type'].iloc[2]
    third_worst_play_type_ppp = worst_df['ppp'].iloc[2]
    third_worst_play_type_freq = worst_df['freq'].iloc[2]

    #FTR:  {ftr} <br> TO%:  {to_per} <br><br> Rim PPP:  {rim_ppp} <br> Rim TS%:  {rim_ts}% on {rim_sq} SQ

    total_summary = f'''Total PPP:  {total_ppp} <br> TS%: {total_ts}% on {total_sq} SQ <br>3PT%: {total_three_point_fg_per}% on {total_three_point_fg_SQ} SQ<br>FTR: {ftr}<br>TO%: {to_per}'''

    player_summary = f'''Rim PPP:  {rim_ppp}<br>TS%:  {rim_ts}% on {rim_sq} SQ<br>FTR: {ftr}<br>TO%: {to_per}'''

    most_freq_summary = f'Most Frequent:<br>1. {most_freq_play_type} ({most_freq_play_type_freq}%)  {most_freq_ppp} PPP<br>2. {second_most_freq_play_type} ({second_most_freq_play_type_freq}%)  {second_most_freq_ppp} PPP<br>3. {third_most_freq_play_type} ({third_most_freq_play_type_freq}%)  {third_most_freq_ppp} PPP'

    best_summary = f'''Best Plays:<br>1. {best_play_type}  {best_play_type_ppp} PPP ({best_play_type_freq}%)<br>2. {second_best_play_type}  {second_best_play_type_ppp} PPP ({second_best_play_type_freq}%)<br>3. {third_best_play_type}  {third_best_play_type_ppp} PPP ({third_best_play_type_freq}%)'''
        
    worst_summary = f'''Worst Plays:<br>1. {worst_play_type}  {worst_play_type_ppp} PPP ({worst_play_type_freq}%)<br>2. {second_worst_play_type}  {second_worst_play_type_ppp} PPP ({second_worst_play_type_freq}%)<br>3. {third_worst_play_type}  {third_worst_play_type_ppp} PPP ({third_worst_play_type_freq}%)'''
    
    court_fig = go.Figure()
    draw_plotly_court(court_fig, fig_width=600)
    
    court_fig.update_layout(
        font=dict(size=36),
        title=dict(text=f'{name} Defensive Shot Chart', x=0.5, y=0.97),
        title_font=dict(size=36, color='black'),
        margin=dict(t=70, b=10, r=430, l=430, pad=0),
        autosize=False,
        width=1520,
        height=700,
        paper_bgcolor='white',
    )
    
    for shot in shots:

            x = shot[0][0]
            y = shot[0][1]
            res = shot[1]

            if res == 1:
                shape = 'circle'
                color = '#4aff50'
                opacity = 0.7
                size = 14

            if res == 2:
                shape = 'circle'
                color = '#f54767'
                opacity = 0.7
                size = 14

            if res == 3:
                shape = 'triangle-up'
                color = '#40ccff'
                opacity = 0.7
                size = 15

            if res == 4:
                shape = 'triangle-up'
                color = '#40ccff'
                opacity = 0.7
                size = 15

            if res == 5:
                shape = 'diamond'
                color = '#ffed2b'
                opacity = 0.7
                size = 14

            if res == 6:
                shape = 'diamond'
                color = '#ffed2b'
                opacity = 0.7
                size = 14

            court_fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode="markers",
                    marker=dict(
                        opacity=opacity,
                        size=size,
                        color=color,
                        symbol=shape
                    ),
                    hoverinfo='none'
                )
            )
            
    court_fig.add_annotation(xref='paper', yref='paper', x=-0.60, y=0.9, text=total_summary, showarrow=False, font=dict(color='black', size=25), align='center', bordercolor="#c7c7c7", borderwidth=2, borderpad=7,)

    court_fig.add_annotation(xref='paper', yref='paper', x=-0.60, y=0.4, text=player_summary, showarrow=False, font=dict(color='black', size=25), align='center', bordercolor="#c7c7c7", borderwidth=2, borderpad=7,)

    court_fig.add_annotation(xref='paper', yref='paper', x=1.62, y=1, text=most_freq_summary, showarrow=False, font=dict(color='black', size=25), align='center', bordercolor="#c7c7c7", borderwidth=2, borderpad=7)

    court_fig.add_annotation(xref='paper', yref='paper', x=1.62, y=0.7, text=best_summary, showarrow=False, font=dict(color='black', size=25), align='center', bordercolor="#c7c7c7", borderwidth=2, borderpad=7)

    court_fig.add_annotation(xref='paper', yref='paper', x=1.62, y=0.15, text=worst_summary, showarrow=False, font=dict(color='black', size=25), align='center', bordercolor="#c7c7c7", borderwidth=2, borderpad=7)
            
    court_fig.write_image("sample.png")
    
    return court_fig

def get_ppp(data):
    
    points = data['points'].sum()
    fga = data[data['result_id'].isin([1,2,4])]
    fta = data['fta'].sum()
    to = len(data[data['result_id'].isin([5,6])])
    ppp = round((points / ((len(fga)) + (0.44 * fta) + to)),2)

    return ppp

def get_freq(data):
    
    play_types_df = pd.DataFrame(columns=['play_type', 'ppp', 'freq'])
   
    for play_type in data['play_type_id'].value_counts().keys():

        ppp = get_ppp(data[data['play_type_id'] == play_type])
        count = len(data[data['play_type_id'] == play_type])
        freq = round(((count / len(data)) * 100),1)

        new_row_values = [play_type, ppp, freq]

        new_row = pd.DataFrame([new_row_values], columns=['play_type', 'ppp', 'freq'])
        play_types_df = pd.concat([play_types_df, new_row], ignore_index=True)
        
    return play_types_df

def get_ts(data):
    
    points = data['points'].sum()
    fga = data[data['result_id'].isin([1,2,4])]
    fta = data['fta'].sum()
    to = len(data[data['result_id'].isin([5,6])])
    ts = round(((points / (2 * ((len(fga) + (0.44 * fta) + to)))) * 100),1)
    
    return ts