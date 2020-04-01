import dash_table
import pandas as pd

url = "/var/www/coronaApp/liveapp/assets/india-helpline.csv"
df_helpline = pd.read_csv(url, encoding="latin1")


layout = dash_table.DataTable(
    id="helpline_table",
    columns=[{"name": i, "id": i} for i in df_helpline.columns],
    data=df_helpline.to_dict("records"),
    page_action="native",
    page_current=0,
    page_size=15,
    sort_action="native",
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold",
        "color": "#243447",
    },
)
