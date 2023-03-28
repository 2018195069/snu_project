import folium
import streamlit as st
import joblib
import pandas as pd
from folium.plugins import Fullscreen, minimap, Search, MarkerCluster, AntPath

from streamlit_folium import st_folium, folium_static


@st.cache_data
def load_data():
    buses = joblib.load("./src/Gwanak_bus")
    bike = pd.read_csv("./src/공공자전거 대여소 정보(22.12월 기준).csv")
    kw_bike = bike.loc[bike['자치구'] == '관악구']
    gwanak_boundary = joblib.load("gwanak_boundary")
    stop_cnt = pd.read_csv("./src/bus_stop_cnt.csv")
    return buses, kw_bike, gwanak_boundary, stop_cnt

bus_type = ['간선','지선', '심야', '마을', '일반', '광역', '공항', '직행좌석']
bus_group = {x:folium.FeatureGroup(name=x) for x in bus_type}
search_name = st.text_input("Enter name of bus route to search:")

def create_map(buses, bikes, bus_type, boundary, stop_cnt):
    # folium map객체 생성
    m = folium.Map(location=[37.478428, 126.931862])

    # 관악구 경계 생성 후 이를 위한 feature group 생성
    b_points = [(i[1], i[0]) for i in boundary]
    boundary_group = folium.FeatureGroup(name='관악구 경계')
    boundary_group.add_to(m)
    folium.PolyLine(b_points, weight=2, opacity=1, color='purple', name='관악구 경계선').add_to(boundary_group)
    
    # 버스 종류별 (지선, 간선 등) feature group 생성
    for group in bus_group.values():
        group.add_to(m)
        
    # 선택한 버스 타입에 해당하는 버스 노선 생성
    for _, bus in buses.iterrows():
        bus_fg = bus_group[bus['typeName']]
        bus_color = bus['color']
        routes = bus['points']
        points = [(i['y'], i['x']) for i in routes]
        tooltip = folium.map.Tooltip(
            f"<b>[{bus['typeName']}][ {bus['name']} ]</b><br>{bus['startPoint']} - {bus['endPoint']}"
            )
        if search_name and search_name == bus['name']:
            route = AntPath(locations=points,name=bus['name'] ,weight=5,tooltip=tooltip, opacity=1,color=bus_color, delay=1600)
        else:
            route = folium.PolyLine(points,name=bus['name'] ,weight=5,tooltip=tooltip, opacity=0.25,color=bus_color)
        route.add_to(bus_fg)
        #route.add_to(bus_routes)
    
    # 모든 정류소 마커 생성
    # bus_stop_fg = folium.FeatureGroup(name="버스 정류장", show=False)
    # bus_stop_fg.add_to(m)
    # for _, stop in stop_cnt.iterrows():
    #     folium.Marker(location = [stop['y'], stop['x']],
    #         tooltip=stop['name'],
    #         name=stop['name'],
    #         icon=folium.Icon(color='orange',prefix='fa',icon='bus')
    #         ).add_to(bus_stop_fg)

    # 따릉이 대여소 마커 생성
    bike_fg = MarkerCluster(name="따릉이 대여소", show=False) 
    bike_fg.add_to(m)
    for _, bike in bikes.iterrows():
        folium.Marker(location = [bike['위도'], bike['경도']],
            tooltip=bike['보관소(대여소)명'],
            name=bike['보관소(대여소)명'],
            icon=folium.Icon(color='green',prefix='fa',icon='bicycle')
            ).add_to(bike_fg)

    Search(layer=bike_fg,search_zoom=20 ,search_label='name', placeholder="따릉이 위치 검색").add_to(m)
    #Search(layer=bus_stop_fg,search_zoom=20 ,search_label='name', placeholder="정류소 위치 검색").add_to(m)

    m.fit_bounds([[37.4421012, 126.831755], [37.5467284, 127.0857543]])
    return m

# 데이터 로드 및 캐싱
buses, gwanak_bike, gwanak_boundary, stop_cnt = load_data()

# 시간대 슬라이더 생성
time_range = st.sidebar.slider("시간대를 선택하세요", 0, 24, (9,10), step=1)
buses_selected = buses[(buses['s_firstTime'] <= time_range[0]) & (buses['s_lastTime'] >= time_range[1])]

m=create_map(buses_selected, gwanak_bike, bus_type, gwanak_boundary, stop_cnt)

Fullscreen().add_to(m)
minimap.MiniMap(zoom_level_offset=-5,toggle_display=True).add_to(m)
folium.TileLayer("Stamen Watercolor").add_to(m)
folium.TileLayer("CartoDB dark_matter").add_to(m)
# call to render Folium map in Streamlit
folium.LayerControl().add_to(m)
st_folium(m,height=700,width=700,returned_objects=[])


