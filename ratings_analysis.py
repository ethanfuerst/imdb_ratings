#%%
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px
import plotly.figure_factory as ff

#%%
with open('ratings.csv', 'r', encoding='mac_roman', newline='') as csvfile:
    df = pd.read_csv(csvfile)

df = df[df['Title Type'] == 'movie'].copy()
df['Release Date'] = pd.to_datetime(df['Release Date'])
df['Date Rated'] = pd.to_datetime(df['Date Rated'])
df['Diff in ratings'] = round(df['IMDb Rating'] - df['Your Rating'],1)
df['Link'] = '<a href=”' + df['URL'].astype(str) +'”>'+ df['Title'].astype(str) 


df.drop('Title Type', axis=1, inplace=True)
df.to_csv('ratings_clean.csv', index=False)

# Genres
one_hot = df['Genres'].str.get_dummies(sep=', ')
genres = list(one_hot.sum().sort_values(ascending=False).index)[:8]
one_hot = one_hot[genres].astype(bool).copy()
df = df.join(one_hot)
df = df.drop(['Genres', 'Date Rated'], axis=1)

df['Decade'] = pd.cut(df['Year'], bins=list(range(1979, 2039, 10)), labels=[str(i+1)[2:] + "'s" for i in range(1979, 2029, 10)], include_lowest=True)

color_list = ['#1A4D94', '#007A33', '#CB4F0A', '#5A2D81'] * int(len(df)/3)
full_color_list = ['#1A4D94', '#5C7DAA', '#007A33', '#33955C', '#CB4F0A', '#F58426','#5A2D81', '#DFAEE6'] * int(len(df)/7)

alt_greys = ['#cccccc', '#e4e4e4'] * len(df)

#%%
# Table1
# See if links work when exporting as picture and .html file
my_ratings = pd.DataFrame()
my_ratings['My Rating'] = [i for i in range(10,0,-1)]
my_ratings['Criteria'] = ['Perfect','Great','Really good','Good','Okay','Average','Not good','Really not good','Bad','Is this even a movie?']
my_ratings['Link'] = ['<a href=”https://www.imdb.com/title/tt0468569/”>The Dark Knight</a>',
        '<a href=”https://www.imdb.com/title/tt0361748/”>Inglourious Basterds</a>',
        '<a href=”https://www.imdb.com/title/tt0993846/”>The Wolf of Wall Street</a>',
        '<a href=”https://www.imdb.com/title/tt1677720/”>Ready Player One</a>',
        '<a href=”https://www.imdb.com/title/tt1219289/”>Limitless</a>',
        '<a href=”https://www.imdb.com/title/tt2461150/”>Masterminds</a>',
        '',
        '<a href=”https://www.imdb.com/title/tt0360556/”>Fahrenheit 451</a>',
        '',
        '<a href=”https://www.imdb.com/title/tt0368226/”>The Room</a>'
]
my_ratings['Title'] = ['The Dark Knight',
'Inglourious Basterds',
'The Wolf of Wall Street',
'Ready Player One',
'Limitless',
'Masterminds',
'',
'Fahrenheit 451',
'',
'The Room'
]


fig = go.Figure(data=[go.Table(
    header=dict(values=['My Rating', 'Criteria', 'Example'],
                fill_color='#5C7DAA',
                font_color='white',
                align='left'),
    cells=dict(values=[my_ratings['My Rating'], my_ratings['Criteria'], my_ratings['Title']],
                fill_color=[alt_greys[:len(df)]]*3,
                font_color='black',
                align='left'))])

fig.show()

#%%
# Scatter1
# my rating vs. imdb rating
fig = go.Figure(data=go.Scatter(x=df['IMDb Rating'],
                                y=df['Your Rating'],
                                mode='markers',
                                marker=dict(
                                    size=8,
                                    color=df['Year'],
                                    colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(0,122,51)']],
                                    showscale=True,
                                    colorbar=dict(
                                        title="Year released"
                                    ),
                                    cmin=df['Year'].min(),
                                    cmax=df['Year'].max(),
                                    cmid=df['Year'].mean()
                                ),
                                hovertemplate=df['Title'].astype(str)+' (' +df['Year'].astype(str) + ' film)'+
                                '<br><b>IMDb Rating</b>: %{x}<br>'+
                                '<b>My Rating</b>: %{y}'+'<extra></extra>'
                                ))
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='IMDb Rating vs. My Rating',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='IMDb Rating'
    ),
    yaxis=dict(
        title='My Rating'
    )
)
fig.show()


#%%
# Table2
# Sort on columns?
# Do links work in html file
# Add legend
df_diff = df.sort_values(axis=0,by='Diff in ratings').reset_index(drop=True).copy()

colors = n_colors('rgb(0,122,51)','rgb(207, 198, 0)', int(len(df_diff)/2), colortype='rgb') + n_colors('rgb(207, 198, 0)', 'rgb(0, 145, 222)', int(len(df_diff)/2), colortype='rgb')
fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Title</b>', '<b>IMDb Rating</b>', '<b>My Rating</b>', '<b>Difference in Ratings</b>'],
    align='center',font=dict(color='white', size=12),
    fill_color='#5C7DAA'
  ),
  cells=dict(
    values=[df_diff['Link'], df_diff['IMDb Rating'], df_diff['Your Rating'], round(df_diff['Diff in ratings'],1)],
    align='left', font=dict(color=['black', 'black', 'black', 'white'], size=11),
    fill_color=[alt_greys[:len(df)],alt_greys[:len(df)],alt_greys[:len(df)],colors]
    ))
])
# plotly.offline.plot(fig, filename='table2')

fig.show()

#%%
# Scatter2
# year vs diff in ratings
# Add text labels
# Add color gradient
fig = go.Figure(data=go.Scatter(x=df['Year'],
                    y=df['Diff in ratings'],
                    mode='markers',
                    # marker_color=df['Runtime (mins)'],
                    marker=dict(
                        size=8,
                        color=df['Your Rating'],
                        colorscale=[[0, 'rgb(255,255,255)'], [1, 'rgb(26,77,148)']],
                        showscale=True,
                        colorbar=dict(
                            title="My rating"
                        ),
                        cmin=df['Your Rating'].min(),
                        cmax=df['Your Rating'].max(),
                        cmid=df['Your Rating'].mean()
                    ),
                    hovertemplate=df['Title'].astype(str)+' (' +df['Year'].astype(str) + ' film)'+
                    '<br><b>IMDb Rating</b>: '+df['IMDb Rating'].astype(str)+'<br>'+
                    '<b>My Rating</b>: '+df['Your Rating'].astype(str)+'<br>'+
                    '<b>Difference</b>: %{y}'+'<extra></extra>'
                ))
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='Year vs. Difference in Ratings',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Year'
    ),
    yaxis=dict(
        title='Difference in Ratings'
    )
)
fig.show()

#%%
# bar1
# num movies per year
# Add hovertext
bar = df.groupby('Year').count()['Title'].copy()
fig = go.Figure(data=go.Bar(x=bar.index,
                    y=bar.values,
                    marker_color=full_color_list[0:len(bar)]
                ))
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='Number of movies in my ratings by year released',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Year'
    ),
    yaxis=dict(
        title='Number of movies rated'
    )
)
fig.show()

#%%
# Table3
# top 5 genres by decade


#%%
# plotly box/whisker1
# x is decade y is my rating
# See if I can change colors of decades

df.sort_values('Year', inplace=True)
fig = go.Figure(data=go.Box(x=df['Decade'],
                    y=df['Your Rating'],
                    marker=dict( 
                        color='#000000'
                    ),
                    line=dict(color='#CB4F0A')
                ))
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='My ratings by decade',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Decade'
    ),
    yaxis=dict(
        title='Rating'
    )
)
fig.show()

#%%
# plotly box/whisker2
# x is genre y is my rating

fig = go.Figure()
for i in range(len(genres)):
    fig.add_trace(go.Box(
        y=df[df[genres[i]] == True]['Your Rating'],
        name=genres[i]
    ))
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='My ratings by genre',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Genre'
    ),
    yaxis=dict(
        title='My Rating'
    )
)
fig.show()


#%%
# This is confusing. Brainstorm this
# df[(df['Decade'] == "90's") & (df['Sci-Fi'] == True)]
# df[(df['Decade'] == "90's") & (df['Sci-Fi'] == False)]
df_2 = df.groupby(['Decade','Sci-Fi'], as_index=False).mean()[['Decade','Sci-Fi','IMDb Rating', 'Your Rating']]
df_2['Sci-Fi'] = np.where(df_2['Sci-Fi'], 'Sci-Fi', 'not Sci-Fi')
df_2['combo'] = df_2['Decade'].astype(str) + ' ' + df_2['Sci-Fi'].astype(str)
df_2.sort_values(['Decade','Sci-Fi'], inplace=True)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_2['combo'], 
    y=df_2['IMDb Rating'],
    name='IMDb Rating',
    mode='markers'
))
fig.add_trace(go.Scatter(
    x=df_2['combo'], 
    y=df_2['Your Rating'],
    name='My Rating',
    mode='markers'
))
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='My ratings by decade and genre',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Decade and Genre'
    ),
    yaxis=dict(
        title='Average Rating'
    )
)
fig.show()

#%%
# Change to plt bar
df.groupby('Decade').sum()[['Sci-Fi', 'Crime', 'Comedy', 'Action', 'Thriller']].plot(kind='bar')
# eh idk



# %%
