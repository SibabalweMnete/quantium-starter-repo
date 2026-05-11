import csv
import datetime

from dash import Dash, dcc, html
import plotly.express as px

INPUT_FILE = 'formatted_sales.csv'


def load_daily_sales(file_path):
    daily_sales = {}

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = datetime.date.fromisoformat(row['Date'])
            sales = float(row['Sales'])
            daily_sales[date] = daily_sales.get(date, 0.0) + sales

    sorted_sales = sorted(daily_sales.items())
    return [
        {'Date': date, 'Sales': sales}
        for date, sales in sorted_sales
    ]


data = load_daily_sales(INPUT_FILE)
fig = px.line(
    data,
    x='Date',
    y='Sales',
    markers=True,
    title='Pink Morsel Total Daily Sales',
)
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Sales',
    title_x=0.5,
    plot_bgcolor='white',
)
fig.update_xaxes(showgrid=True, gridcolor='#e5e5e5')
fig.update_yaxes(showgrid=True, gridcolor='#e5e5e5')

app = Dash(__name__)
app.title = 'Pink Morsel Sales Visualiser'
app.layout = html.Div(
    [
        html.H1('Pink Morsel Sales Visualiser', style={'textAlign': 'center'}),
        html.P(
            'Total daily sales of Pink Morsels over time. The chart is sorted by date so price increase impacts are easy to compare.',
            style={'textAlign': 'center', 'maxWidth': '720px', 'margin': '0 auto 24px'},
        ),
        dcc.Graph(figure=fig),
    ],
    style={'fontFamily': 'Arial, sans-serif', 'margin': '24px'},
)


if __name__ == '__main__':
    app.run(debug=True)
