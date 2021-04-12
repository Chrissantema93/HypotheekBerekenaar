import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data = pd.read_csv(r'hypotheek.csv', sep=';')
df = px.data.gapminder()
all_continents = df.continent.unique()
verstrekker = data['Verstrekker'].unique()
rentevaste = data['Rentevaste periode'].unique()
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Checklist(
        id="checklist",
        options=[{"label": x, "value": x} 
                 for x in verstrekker],
        value=verstrekker,
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Checklist(
        id="checklist2",
        options=[{"label": x, "value": x} 
                 for x in rentevaste],
        value=rentevaste,
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="line-chart"),
])

@app.callback(
    Output("line-chart", "figure"), 
    [Input("checklist", "value"),
    Input("checklist2", "value")])
def update_line_chart(verstrekkers, periodes):
    mask = data['Verstrekker'].isin(verstrekkers)
    mask2 = data['Rentevaste periode'].isin(periodes)
    data2 = data[mask & mask2]
    jaren = data2["Jaar"]
    restschuld_10 = data2[data2["Rentevaste periode"] == 10]["Restschuld"]
    restschuld_20 = data2[data2["Rentevaste periode"] == 20]["Restschuld"]
    netto_10 = data2[data2["Rentevaste periode"] == 10]["Netto salaris na hypotheeklasten"]
    netto_20 = data2[data2["Rentevaste periode"] == 20]["Netto salaris na hypotheeklasten"]
    fig = px.bar(data[mask & mask2], 
        x='Jaar', y="Netto salaris na hypotheeklasten", color='Label', barmode="group", text='Netto salaris na hypotheeklasten')
    # fig.add_bar(x=jaren, y=restschuld_10, name="Restschuld 20 jaar vast")
    # fig.add_bar(x=jaren, y=restschuld_20, name="Restschuld 10 jaar vast")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

