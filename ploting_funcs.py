import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime

SHOW_DATES = [
    # [NAME, [START, END]]
    ['האח הגדול VIP עונה 4',
     [datetime.datetime(year=2021, month=7, day=10), datetime.datetime(year=2021, month=8, day=31)]],
    ['האח הגדול עונה 12',
     [datetime.datetime(year=2022, month=6, day=7), datetime.datetime(year=2022, month=8, day=31)]],
    ['חתונמי עונה 4',
     [datetime.datetime(year=2021, month=7, day=13), datetime.datetime(year=2021, month=11, day=27)]],
    ['חתונמי עונה 5',
     [datetime.datetime(year=2022, month=5, day=9), datetime.datetime(year=2022, month=8, day=31)]],
    ['הישרדות VIP עונה 5',
     [datetime.datetime(year=2022, month=4, day=3), datetime.datetime(year=2021, month=10, day=16)]],
    ['רוקדים עם כוכבים ',
     [datetime.datetime(year=2022, month=2, day=13), datetime.datetime(year=2022, month=4, day=11)]]
]


def plot_avgs(df, show_metadata=False, shows=SHOW_DATES):
    tdf = df.groupby(by=df.base_month).agg({'word_count': 'sum', 'post_id': 'count'}).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=tdf.base_month, y=tdf.word_count / tdf.post_id, mode='lines+markers',
                   name='מספר מילים ממוצע לפוסט')
    )

    fig.update_layout(
        legend=dict(
            title_font_family="Times New Roman",
            font=dict(
                family="Arial",
                size=15,
                color="black"
            ),
            bordercolor="Black",
            borderwidth=2,
        ),
        font=dict(
            family="Arial",
            size=24,
        ),
        width=900,
        height=500,
        showlegend=False
    )
    fig.update_xaxes(minor=dict(showgrid=True), showticklabels=False)

    if show_metadata:
        for i, show in enumerate(shows):
            name, dates = show
            fig.add_trace(go.Scatter(x=dates, y=[i * 2 + 1] * 2,
                                     mode='lines', name=name,
                                     line=dict(width=4),
                                     legendgroup=name),
                          secondary_y=True)

        fig.update_layout(showlegend=True)
        fig.update_xaxes(minor=dict(showgrid=True), showticklabels=True)

    return fig


def show_heatmap(df):
    df['dummy'] = 1
    fig = px.density_heatmap(df, x="hour", y='dummy', marginal_x="histogram", text_auto=True, nbinsx=24)
    fig.update_layout(height=300, xaxis=dict(ticks='', showgrid=False, zeroline=False, nticks=48))
    fig.show()
