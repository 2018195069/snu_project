import folium
import streamlit as st
import joblib
import pandas as pd
from folium.plugins import Fullscreen, minimap

from streamlit_folium import st_folium, folium_static


@st.cache_data
def load_data():
    buses = joblib.load("./bus_data/Gwanak_bus")
    bike = pd.read_csv("./bike_data/공공자전거 대여소 정보(22.12월 기준).csv")
    kw_bike = bike.loc[bike['자치구'] == '관악구']
    gwanak_boundary = joblib.load("gwanak_boundary")
    return buses, kw_bike, gwanak_boundary

bus_type = ['간선','지선', '심야', '마을', '일반', '광역', '공항', '직행좌석']
bus_group = {x:folium.FeatureGroup(name=x) for x in bus_type}
def create_map(buses, bikes, bus_type, boundary):
    m = folium.Map(location=[37.478428, 126.931862])
    boundary_group = folium.FeatureGroup(name='관악구 경계')
    boundary_group.add_to(m)
    b_points = [(i[1], i[0]) for i in boundary]
    folium.PolyLine(b_points, weight=2, opacity=1, color='purple').add_to(boundary_group)
    # 선택한 버스 타입에 해당하는 버스 노선 생성
    
    for _, bus in buses.iterrows():
        fg = bus_group[bus['typeName']]
        bus_color = bus['color']
        routes = bus['points']
        points = [(i['y'], i['x']) for i in routes]
        tooltip = folium.map.Tooltip(
            "<b>[ " + bus['name'] + ' ]</b><br>'+ bus['startPoint'] +" - "+ bus['endPoint']
            )
        folium.PolyLine(points, weight=5,tooltip=tooltip, opacity=0.25,color=bus_color).add_to(fg)
    for group in bus_group.values():
        group.add_to(m)
    # 따릉이 대여소 마커 생성
    fg = folium.FeatureGroup(name="따릉이 대여소", show=False) 
    fg.add_to(m)
    for _, bike in bikes.iterrows():
        folium.Marker(location = [bike['위도'], bike['경도']],
            tooltip=bike['보관소(대여소)명'],
            icon=folium.Icon(color='green',prefix='fa',icon='bicycle')
            ).add_to(fg)

    m.fit_bounds([[37.4421012, 126.831755], [37.5467284, 127.0857543]])
    return m

buses, gwanak_bike, gwanak_boundary = load_data()

# 시간대 슬라이더 생성
time_range = st.sidebar.slider("시간대를 선택하세요", 0, 24, (9,10), step=1)
buses_selected = buses[(buses['s_firstTime'] <= time_range[0]) & (buses['s_lastTime'] >= time_range[1])]

m=create_map(buses_selected, gwanak_bike, bus_type, gwanak_boundary)
bus_group['지선'].control
Fullscreen().add_to(m)
minimap.MiniMap(zoom_level_offset=-5,toggle_display=True).add_to(m)
folium.TileLayer("Stamen Watercolor").add_to(m)
folium.TileLayer("CartoDB dark_matter").add_to(m)
# call to render Folium map in Streamlit
folium.LayerControl().add_to(m)
st_folium(m,height=700,width=700,returned_objects=[])


