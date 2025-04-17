import dash
from dash import dcc, html
import dash_leaflet as dl
from dash.dependencies import Input, Output
import pandas as pd
import geopandas as gpd
import json

# Загрузка данных
geo_data = gpd.read_file('geoBoundaries-RUS-ADM1.geojson')
df = pd.read_csv('Книга3.csv')
df["Год"] = df["Год"].astype(str)

# Приведение к нижнему регистру для сопоставления
geo_data['shapeName'] = geo_data['shapeName'].str.lower()
df['Регион'] = df['Регион'].str.lower()

# Уникальные значения
years = sorted(df["Год"].unique())
region_options = sorted(df['Регион'].dropna().unique())
region_dropdown_options = [{"label": r.capitalize(), "value": r} for r in region_options]
region_dropdown_options.insert(0, {"label": "Все регионы", "value": "all"})

# Длинные названия показателей (пример)
full_indicator_list = [
    "численность населения в трудоспособном возрасте на 1 января текущего года (человек, на 1 января, всего в трудоспособном возрасте (для мужчин 16-59,для женщин 16-54))",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) всего по всем видам экономической деятельности",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) растениеводство и животноводство, охота и предоставление соответствующих услуг в этих областях",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) лесоводство и лесозаготовки",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) обработка древесины и производство изделий из дерева и пробки, кроме мебели, производство изделий из соломки и материалов для плетения",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) обеспечение электрической энергией, газом и паром; кондиционирование воздуха",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) торговля оптовая, кроме оптовой торговли автотранспортными средствами и мотоциклами",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) торговля розничная, кроме торговли автотранспортными средствами и мотоциклами",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность сухопутного и трубопроводного транспорта",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) складское хозяйство и вспомогательная транспортная деятельность",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность в области здравоохранения",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) добыча металлических руд",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность в области телевизионного и радиовещания",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность по уходу с обеспечением проживания",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) производство пищевых продуктов",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность библиотек, архивов, музеев и прочих объектов культуры",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность в области спорта, отдыха и развлечений",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) прочие",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) работы строительные специализированные",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность в сфере телекоммуникаций",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) рыболовство и рыбоводство",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) строительство зданий",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) торговля оптовая и розничная автотранспортными средствами и мотоциклами и их ремонт",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность воздушного и космического транспорта",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность по обслуживанию зданий и территорий",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) добыча угля",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) деятельность в области архитектуры и инженерно-технического проектирования; технических испытаний, исследований и анализа",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) производство металлургическое",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) добыча прочих полезных ископаемых",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) производство химических веществ и химических продуктов",
    "количество стационарных источников загрязнения атмосферы на конец года, имеющихся у юридических лиц (единица, значение показателя за год) добыча нефти и природного газа"
]

# Инициализация страницы
dash.register_page(__name__)

layout = html.Div([
    html.H2("Карта с данными по годам", style={"textAlign": "center"}),

    html.Div([
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": year, "value": year} for year in years],
            value=years[0],
            clearable=False,
            style={"width": "200px", "marginRight": "20px"}
        ),
        dcc.Dropdown(
            id="region-dropdown",
            options=region_dropdown_options,
            value="all",
            clearable=False,
            style={"width": "250px", "marginRight": "20px"}
        ),
        dcc.Dropdown(
            id="full-indicator-dropdown",
            options=[{"label": ind, "value": ind} for ind in full_indicator_list],
            value=full_indicator_list[0],
            clearable=False,
            style={"width": "800px"}
        )
    ], style={"display": "flex", "justifyContent": "center", "marginBottom": "20px", "flexWrap": "wrap"}),

    dl.Map(
        id="map",
        center=[61, 105],
        zoom=4,
        children=[
            dl.TileLayer(),
            dl.GeoJSON(id="geojson-layer"),
            dl.LayerGroup(id="markers"),
            dl.LayerGroup(id="region-markers")
        ],
        style={"height": "600px", "width": "100%", "marginTop": "20px"}
    )
])

# Обновление GeoJSON
@dash.callback(
    Output("geojson-layer", "data"),
    [Input("year-dropdown", "value"),
     Input("full-indicator-dropdown", "value"),
     Input("region-dropdown", "value")]
)
def update_geojson(selected_year, selected_indicator, selected_region):
    filtered_df = df[df["Год"] == selected_year]

    if selected_region != "all":
        filtered_df = filtered_df[filtered_df["Регион"] == selected_region]
        geo_filtered = geo_data[geo_data["shapeName"] == selected_region]
    else:
        geo_filtered = geo_data

    merged = geo_filtered.merge(filtered_df, left_on="shapeName", right_on="Регион", how="left")
    return json.loads(merged.to_json())

# Маркеры населённых пунктов
@dash.callback(
    Output("markers", "children"),
    [Input("year-dropdown", "value"),
     Input("full-indicator-dropdown", "value"),
     Input("region-dropdown", "value")]
)
def update_markers(selected_year, selected_indicator, selected_region):
    filtered_df = df[df["Год"] == selected_year]
    if selected_region != "all":
        filtered_df = filtered_df[filtered_df["Регион"] == selected_region]

    if selected_indicator not in df.columns:
        return []

    filtered_df = filtered_df.dropna(subset=["широта", "долгота"])

    markers = []
    for _, row in filtered_df.iterrows():
        try:
            lat, lon = float(row["широта"]), float(row["долгота"])
        except ValueError:
            continue

        popup = [
            html.B(row['Регион'].capitalize()),
            html.Br(),
            f"{row.get('Населённый пункт', '')}, {row['Год']}",
            html.Br(),
            f"{selected_indicator}: {row[selected_indicator]}"
        ]

        markers.append(dl.Marker(position=[lat, lon], children=dl.Popup(popup)))

    return markers

# Центры регионов
@dash.callback(
    Output("region-markers", "children"),
    [Input("year-dropdown", "value"),
     Input("full-indicator-dropdown", "value"),
     Input("region-dropdown", "value")]
)
def update_region_markers(selected_year, selected_indicator, selected_region):
    filtered_df = df[df["Год"] == selected_year]
    if selected_region != "all":
        filtered_df = filtered_df[filtered_df["Регион"] == selected_region]
        geo_filtered = geo_data[geo_data["shapeName"] == selected_region]
    else:
        geo_filtered = geo_data

    merged = geo_filtered.merge(filtered_df, left_on="shapeName", right_on="Регион", how="left")

    markers = []
    for _, row in merged.iterrows():
        if row["geometry"] and row["geometry"].is_valid:
            center = row["geometry"].centroid
            lat, lon = center.y, center.x

            region_name = row["shapeName"].capitalize() if isinstance(row["shapeName"], str) else "Неизвестный регион"
            value = row.get(selected_indicator)
            value_display = f"{value}" if pd.notna(value) else "Нет данных"

            popup = dl.Popup([
                html.B(region_name),
                html.Br(),
                f"Год: {selected_year}",
                html.Br(),
                f"{selected_indicator}: {value_display}"
            ])

            markers.append(dl.CircleMarker(
                center=[lat, lon],
                radius=10,
                color="green",
                fill=True,
                fillOpacity=0.6,
                children=popup
            ))

    return markers