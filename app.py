import csv
import datetime

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

INPUT_FILE = 'formatted_sales.csv'
REGIONS = ['all', 'north', 'east', 'south', 'west']


def load_sales_data(file_path):
    all_rows = []

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_rows.append(
                {
                    'Date': datetime.date.fromisoformat(row['Date']),
                    'Sales': float(row['Sales']),
                    'Region': row['Region'].strip().lower(),
                }
            )

    return all_rows


def aggregate_daily_sales(rows):
    daily_sales = {}

    for row in rows:
        date = row['Date']
        daily_sales[date] = daily_sales.get(date, 0.0) + row['Sales']

    sorted_sales = sorted(daily_sales.items())
    return [{'Date': date, 'Sales': sales} for date, sales in sorted_sales]


all_data = load_sales_data(INPUT_FILE)
initial_data = aggregate_daily_sales(all_data)

fig = px.line(
    initial_data,
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
    font_family='Inter, sans-serif',
)
fig.update_xaxes(showgrid=True, gridcolor='#ebedf0')
fig.update_yaxes(showgrid=True, gridcolor='#ebedf0')

app = Dash(
    __name__,
    external_stylesheets=[
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap',
    ],
)
app.title = 'Pink Morsel Sales Visualiser'
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1('Pink Morsel Sales Visualiser'),
                html.P(
                    'Explore how Pink Morsel sales changed before and after the January 15, 2021 price increase. Use the region selector to compare performance across the north, east, south, and west regions.',
                ),
            ],
            className='header',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label('Region filter', className='label'),
                        dcc.RadioItems(
                            id='region-selector',
                            options=[{'label': region.title(), 'value': region} for region in REGIONS],
                            value='all',
                            inline=True,
                            inputStyle={'margin-right': '8px', 'margin-left': '16px'},
                            className='radio-items',
                        ),
                    ],
                    className='control-panel',
                ),
                dcc.Graph(id='sales-chart', figure=fig, className='chart-card'),
            ],
            className='content',
        ),
    ],
    className='page',
)


@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-selector', 'value'),
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered = all_data
    else:
        filtered = [row for row in all_data if row['Region'] == selected_region]

    daily_data = aggregate_daily_sales(filtered)
    figure = px.line(
        daily_data,
        x='Date',
        y='Sales',
        markers=True,
        title=f'Pink Morsel Daily Sales — {selected_region.title() if selected_region != "all" else "All Regions"}',
    )
    figure.update_layout(
        xaxis_title='Date',
        yaxis_title='Sales',
        title_x=0.5,
        plot_bgcolor='white',
        font_family='Inter, sans-serif',
    )
    figure.update_xaxes(showgrid=True, gridcolor='#ebedf0')
    figure.update_yaxes(showgrid=True, gridcolor='#ebedf0')
    return figure


if __name__ == '__main__':
    app.run(debug=True)
