import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import plotly.express.colors as colors
from PIL import Image

st.set_page_config(page_title="관악구 심야 버스 이용자 수 EDA", page_icon="📊")
st.title("관악구 :blue[심야 버스 이용자 수] EDA")
st.sidebar.markdown("###### 본 프로젝트를 통해 정류장과 노선을 기준으로 심야부터 새벽까지의 시간대별 버스 이용자 수를 파악하고자 하였습니다")
st.caption(
    """이 페이지는 네이버에 '관악구를 지나는 버스' 를 검색한 결과 크롤링한 데이터를 바탕으로 제작되었습니다"""
)



tab1, tab2, tab3, tab4, tab5  = st.tabs(["데이터 전처리", "정거장별 이용자수", "버스 노선별 이용자수", "시간대별 이용자수", "그래프 시각화"])




with tab1:
    st.write("- 데이터 : 버스노선별, 정류장별, 시간대별, 승하차 인원 정보")
    df = pd.read_csv('2023년_버스노선별_정류장별_시간대별_승하차_인원_정보(02월).csv', encoding='cp949', low_memory=False)
    df.drop(columns=['사용년월','노선명','표준버스정류장ID','버스정류장ARS번호','교통수단타입코드','등록일자'], axis=1, inplace=True)
    gwanak_bus_list = ['1', '1-1', '5', '9', '9-3', '11-2', '11-5', '20', '51', '103', '150', '152', '461', '500', '501', '502', '504', '505', '506', '507', '540', '641', '643', '650', '651', '750B', '750A', '777', '900', '1002', '1008', '3301', '3500', '4212', '4319', '4318', '5515', '5513', '5511', '5413', '5516', '5517', '5519', '5525', '5523', '5522B호암', '5522A난곡', '5524', '5528', '5536', '5531', '5530', '5535', '5617', '5615', '5609', '5621', '5602', '5616', '5620', '5625', '5623', '5634', '5627', '5633', '5713', '6003', '6017', '6511', '6512', '6514', '6515', '6516', '6635', '7000', '7001', '7007-1', '7770', '7780', '7790', '7800', '8155', '8156', '8507', '8552', '8561', '8541', '8842', 'M5556', 'M5532', 'N15', 'N51', 'N61', 'N75']
    night_time_column = ['23시승차총승객수', '23시하차총승객수','00시승차총승객수', '00시하차총승객수', '1시승차총승객수', '1시하차총승객수', '2시승차총승객수', '2시하차총승객수', '3시승차총승객수','3시하차총승객수','4시승차총승객수','4시하차총승객수','5시승차총승객수','5시하차총승객수','6시승차총승객수','6시하차총승객수']
    st.write("- 관악구를 지나는 버스만을 필터링하여 파악")
    df_gwanak = df[df['노선번호'].isin(gwanak_bus_list)]
    df_gwanak
    st.write("- 23시~6시 사이의 데이터로 필터링")

    #심야 승차 정보
    on_bus = df_gwanak.loc[:,df_gwanak.columns.str.contains('승차')]
    on_bus
    hour = {}
    for col in on_bus.columns:
        hour[col]=col.split('승차총승객수')[0]
    on_bus = on_bus.rename(columns=hour)
    on_bus = on_bus[['23시', '00시','1시','2시','3시','4시','5시','6시']]
    on_bus['심야승차'] = on_bus.sum(axis=1)
    on_bus[['노선번호','정류장', '종류']] = df[['노선번호','역명','교통수단타입명']]
    on_bus['정류장'] = on_bus['정류장'].apply(lambda x: str(x).split('(')[0])
    on_bus = on_bus.sort_values(by='심야승차', ascending=False)
    
    #심야 하차 정보
    off_bus = df_gwanak.loc[:,df_gwanak.columns.str.contains('하차')]
    hour = {}
    for col in off_bus.columns:
        hour[col]=col.split('하차총승객수')[0]
    
    off_bus = off_bus.rename(columns=hour)
    off_bus = off_bus[['00시','1시','2시','3시','4시','5시','6시','23시']]
    off_bus['심야하차'] = off_bus.sum(axis=1)
    off_bus[['노선번호','정류장','종류']] = df[['노선번호','역명','교통수단타입명']]
    off_bus['정류장'] = off_bus['정류장'].apply(lambda x: str(x).split('(')[0])
    off_bus = off_bus.sort_values(by=['정류장', '심야하차'], ascending=False)
    
    st.write("- 심야 승차 정보와 하차 정보를 합해서 심야 승하차 정보로 추출 : 시간 당 승하차 정보를 열로 추출")
    total = pd.merge(on_bus, off_bus, how='outer').groupby('정류장').sum().sort_values(by='심야승차', ascending=False)
    total['심야승하차'] = total['심야승차'] + total['심야하차']
    total.drop(columns=['심야승차','심야하차'], inplace=True)
    total.sort_values(by='심야승하차', ascending=False).head(20)
    total

with tab2:
    #정류장 기준
    st.write("- 정류장 기준 시간별 버스 이용자 수")
    total
    st.write("- 심야 승하차 버스 정류장 상위 20개 - 신림, 구로디지털단지역이 가장 많았다.")
    total_bus_top20_stop = total.groupby('정류장').sum().sort_values(by='심야승하차',ascending=False).head(20)
    total_bus_top20_stop
    

with tab3:
    #노선 기준
    st.write("- 노선 기준 시간별 버스 이용자 수")
    total2 = pd.merge(on_bus, off_bus, how='outer').groupby(['노선번호','종류']).sum().sort_values(by='심야승차', ascending=False)
    #total2 = pd.merge(on_bus, off_bus, how='outer').groupby('노선번호').sum().sort_values(by='심야승차', ascending=False)
    total2['심야승하차'] = total2['심야승차'] + total2['심야하차']
    total2.drop(columns=['심야승차','심야하차'], inplace=True)
    top20_bus = total2.sort_values(by='심야승하차', ascending=False).head(20)
    top20_bus
    st.write("- 노선번호를 중심으로 그룹화함 : 어느 버스 노선이 가장 심야 이용객 수가 많은지 파악")
    

    

with tab4:

    st.write("- 심야 시간대의 승차 인원수 정보")
    on_bus = df_gwanak.loc[:,df_gwanak.columns.str.contains('승차')]

    hour = {}
    for col in on_bus.columns:
        hour[col]=col.split('승차총승객수')[0]

    on_bus = on_bus.rename(columns=hour)
    on_bus = on_bus[['00시','1시','2시','3시','4시','5시','6시','23시']]
    on_bus['심야승차'] = on_bus.sum(axis=1)
    on_bus[['노선번호','정류장', '종류']] = df[['노선번호','역명','교통수단타입명']]
    on_bus['정류장'] = on_bus['정류장'].apply(lambda x: str(x).split('(')[0])
    on_bus = on_bus.sort_values(by='심야승차', ascending=False)
    on_bus

    st.write("- 심야 시간대의 하차 인원수 정보")
    off_bus = df_gwanak.loc[:,df_gwanak.columns.str.contains('하차')]
    hour = {}
    for col in off_bus.columns:
        hour[col]=col.split('하차총승객수')[0]
    off_bus = off_bus.rename(columns=hour)
    off_bus = off_bus[['00시','1시','2시','3시','4시','5시','6시','23시']]
    off_bus['심야하차'] = off_bus.sum(axis=1)
    off_bus[['노선번호','정류장','종류']] = df[['노선번호','역명','교통수단타입명']]
    off_bus['정류장'] = off_bus['정류장'].apply(lambda x: str(x).split('(')[0])
    off_bus = off_bus.sort_values(by=['정류장', '심야하차'], ascending=False)

    off_bus


with tab5:
    st.write("- 카테고리별 정류장 Top20")
    st.write(" ")
    palette = colors.qualitative.Dark24
    on_bus.sort_values(by=['정류장', '심야승차'], ascending=False, inplace=True)
    on_bus_top20_stop = on_bus.groupby('정류장').sum().sort_values(by='심야승차',ascending=False).head(20)
    x = on_bus_top20_stop.index
    y = on_bus_top20_stop['심야승차']
    fig = go.Figure(go.Bar(x=y, y=x, orientation='h', marker_color=palette))
    fig.update_layout(
        title='서울시 심야승차 버스정류장 Top20',
        xaxis_title='심야승차',
        yaxis_title='정류장명',
        yaxis=dict(autorange="reversed"))
    fig.update_traces(text=y, textposition='outside')
    # 그래프 출력
    st.plotly_chart(fig)



    off_bus.sort_values(by=['정류장', '심야하차'], ascending=False)
    off_bus_top20_stop = off_bus.groupby('정류장').sum().sort_values(by='심야하차',ascending=False).head(20)
    x = off_bus_top20_stop.index
    y = off_bus_top20_stop['심야하차']
    fig = go.Figure(go.Bar(x=y, y=x, orientation='h', marker_color = palette))
    fig.update_layout(
        title='서울시 심야하차 버스정류장 Top20',
        xaxis_title='심야하차',
        yaxis_title='정류장명',
        yaxis=dict(autorange="reversed"))
    fig.update_traces(text=y, textposition='outside')
    # 그래프 출력
    st.plotly_chart(fig)




  
    palette = colors.qualitative.Dark24
    x = total_bus_top20_stop.index
    y = total_bus_top20_stop['심야승하차']
    fig = go.Figure(go.Bar(x=y, y=x, orientation='h', marker_color=palette))
    fig.update_layout(
        title='서울시 심야승하차 버스정류장 Top20',
        xaxis_title='심야승하차',
        yaxis_title='정류장명',
        yaxis=dict(autorange="reversed"))
    fig.update_traces(text=y, textposition='outside')
    # 그래프 출력
    st.plotly_chart(fig)


    st.write("- 워드 클라우드로도 시각화 - 구로디지털단지, 신림사거리, 신림역이 크다. ")

    image13 = Image.open('image13.png')
    image133 = st.image(image13, use_column_width=True)
    st.header(" ")

    st.write("- 버스 노선 기준 버스 이용자수 파악" )
    #최다 승하차 노선
    
    total_bus_top20_bus = total2.groupby('노선번호').sum().sort_values(by='심야승하차', ascending=False).head(20)
    total_bus_top20_bus.index = total_bus_top20_bus.index.map(str) # 인덱스를 문자열로 변환\
    total_bus_top20_bus
    st.write(total_bus_top20_bus.index)
    st.write(total_bus_top20_bus['심야승하차'])
    x = total_bus_top20_bus.index
    y = total_bus_top20_bus['심야승하차']

    fig = go.Figure(go.Bar(x=x, y=y, orientation='h'))

    fig.update_layout(
        title='서울시 심야승하차 버스노선 Top20',
        height=600,
        width=800,
        margin=dict(l=100, r=50, t=50, b=50),
        xaxis_title='심야승하차',
        yaxis_title='노선번호',
        yaxis=dict(autorange="reversed"),
    )

    fig.update_yaxes(
        tickfont=dict(size=10)
    )

    st.plotly_chart(fig)


    total_bus_top20_bus = total2.groupby('노선번호').sum().sort_values(by='심야승하차', ascending=False).head(20)

    y = total_bus_top20_bus.index.astype(str)  # 노선번호를 문자열로 변환
    x = total_bus_top20_bus['심야승하차']

    fig = go.Figure(go.Bar(
        x=x,
        y=y,
        orientation='h',
        text=y,  # y축 레이블을 y로 지정
        textposition='auto',  # 자동으로 위치 조정
    ))

    fig.update_layout(
        title='서울시 심야승하차 버스노선 Top20',
        height=600,
        width=800,
        margin=dict(l=100, r=50, t=50, b=50),
        xaxis_title='심야승하차',
        yaxis_title='노선번호',
        yaxis=dict(autorange="reversed"),
    )

    fig.update_yaxes(
        tickfont=dict(size=10)
    )

    st.plotly_chart(fig)




    fig = go.Figure()
    for i, group in enumerate(total2.index.levels[1]):
        mask = total2.index.get_level_values(1) == group
        fig.add_trace(go.Bar(
            x=total2['심야승하차'][mask],
            y=total2.index.get_level_values(0)[mask],
            name=group,
            orientation='h',
            marker=dict(color=['blue', 'red', 'green'][i%3])  # 종류별로 색깔 다르게 지정
        ))
    fig.update_layout(
        title='서울시 심야승하차 버스노선 Top20_노선 종류별',
        xaxis_title='심야승하차',
        yaxis_title='노선번호',
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig)











    st.write("- 정거장 심야 승하차 정보를 바탕으로 시간대별 버스 이용자수 파악")

    # # 각 열의 합계 계산하여 마지막 행으로 추가
    total.loc['시간대별통행량',:] = total.sum(axis=0)
    tot_tail = total.tail(1)
    on_bus.loc['시간대별통행량',:] = on_bus.sum(axis=0)
    on_bus_tail = on_bus.tail(1)
    off_bus.loc['시간대별통행량',:] = off_bus.sum(axis=0)
    off_bus_tail = off_bus.tail(1)

    on_bus_tail = on_bus_tail.drop(['심야승차','노선번호','정류장'], axis=1)
    off_bus_tail = off_bus_tail.drop(['심야하차','노선번호','정류장'], axis=1)

    import plotly.graph_objs as go

    # plotly line graph 생성
    fig = go.Figure()
    x = ['23시~00시', '00시~1시', '1시~2시', '2시~3시', '3시~4시', '4시~5시', '5시~6시', '6시~7시']
    fig.add_trace(go.Scatter(x=x, y = tot_tail.loc['시간대별통행량'], mode='lines+markers', name='관악구의 시간대별 총 통행량'))
    fig.update_layout(title='관악구 심야시간대별 통행량 추이', xaxis_title='시간대', yaxis_title='통행량(승하차 인원)')
    st.plotly_chart(fig)


    import plotly.express.colors as colors
    palette = colors.qualitative.Plotly
    fig = go.Figure()
    x = ['23시~00시', '00시~1시', '1시~2시', '2시~3시', '3시~4시', '4시~5시', '5시~6시', '6시~7시']
    y = tot_tail.loc['시간대별통행량']
    fig.add_trace(go.Bar(x=x, y=y, name='관악구의 시간대별 총 통행량', marker_color=palette))
    fig.update_layout(title='관악구 심야시간대별 통행량 추이', xaxis_title='시간대', yaxis_title='총 통행량')
    fig.update_traces(text=y, textposition='outside')
    st.plotly_chart(fig)

    # Bar 클래스 생성, name 인자로 범례 생성
    x = ['23시~00시', '00시~1시', '1시~2시', '2시~3시', '3시~4시', '4시~5시', '5시~6시', '6시~7시']
    data1 = go.Bar(x=x, y=on_bus_tail.loc['시간대별통행량'], name='승차')
    data2 = go.Bar(x=x, y=off_bus_tail.loc['시간대별통행량'], name='하차')
    layout = go.Layout(title='관악구의 심야시간대별 승하차 인구') # Title 설정
    
    # 생성된 Bar 클래스를 리스트로 만들어 data 인자로 설정
    fig = go.Figure(data=[data1, data2], layout=layout)
    fig.update_traces(text=y, textposition='outside')
    st.plotly_chart(fig)
