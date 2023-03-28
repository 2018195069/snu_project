import streamlit as st
from PIL import Image

subheader_choices = ['1. 주제 의식 도출', '2. 시각화 대상 지역 선정 이유', '3. 시각화 대상 시간대 선정 이유', '4. 시각화 대상 주제 선정 이유', '5. 시각화 목표', '6. 참고사례', '7. 개선 가능성']



with st.sidebar.form(key="my_form"):
    selectbox_subheader = st.selectbox("목차", subheader_choices)
    pressed = st.form_submit_button(" ")




st.title("관악구 :blue[버스 노선 정보] 시각화 프로젝트")
st.caption('_5조 김지민, 박철수, 서우림, 윤경주, 이수연, 조은소리_')
st.title(" ")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([" 1 ", "2", "3", "4", "5", "6"])

with tab1:
   
   st.subheader("1. 주제 의식 도출")
   st.write("- 주제의식 : 대중교통 정보를 지도상에서 한눈에 쉽게 파악할 수는 없을끼?")
   st.write("---- 버스 막차 시간대가 노선별로 달라 한 눈에 파악하기가 어렵다")
   st.write("---- 같은 경로를 다니는 서로 다른 노선의 버스를 한 눈에 볼 수는 없을까?")
   st.write("---- 정류장 중심이 아닌 지도 중심으로 경로를 파악할 수는 없을까?")

   st.subheader("- 수요 분석")
   st.write("---- 밤 12시 넘어서까지 팀 프로젝트 및 과제가 있는 대학생")
   st.write("---- 심야까지 이어진 음주 후 귀가하고자 하는 직장인")
   st.write('---- 아이돌 공연 방송을 보기 위해 새벽에 방송국으로 이동하고 싶은 아이돌팬')
   st.write("---- 야근으로 늦게 귀가하는 직장인")
   st.write("---- 관악구 한정 버스 경로 및 자전거 대중교통 정보를 지도 위에서 파악하고 싶은 사람")
   st.write('---- 네이버지도와 카카오맵이 아닌 다른 수단으로 교통정보를 얻고자 하는 사람')
   
   st.write("- 카카오맵, 네이버지도를 쓰면 버스 노선의 정보를 알지만 지도상의 정보를 알기 어렵다")
   image11 = Image.open('bus_sche1.png')
   image111 = st.image(image11, use_column_width=True)
   image12 = Image.open('bus_sche2.png')
   image122 = st.image(image12, use_column_width=True)
   st.write("- 대전광역시 시내버스 노선 안내도 : 구체적으로 정류장 이름을 알지 못하더라도, 위치만 알면 역명 파악 가능")
   image5 = Image.open('bus.png')
   image55 = st.image(image5, use_column_width=True)  





with tab2:
   st.subheader(" ")
   st.subheader("2. 시각화 대상 지역 선정 이유")
   st.write("- 시각화 대상 지역 : 서울특별시 관악구")
   st.write("- 빅데이터 핀테크 교육이 이뤄지는 서울대를 중심으로 선정")
   st.write("- 서울과 경기도의 경계이자 서남권에 위치한 교통의 요지로 유동인구가 많기 때문에 대상 지역으로 선정")
   st.write("- 관악구는 서울시 5대 핵심 권역 중 서남권 권역에 위치")

   image1 = Image.open('seoul1.png')
   image2 = Image.open('seoul2.png')
   image3 = Image.open('seoul3.png')

   image11 = st.image(image1, use_column_width=True)
   st.write("- 사당-신도림에 걸친 서울시 3대 도심 여의도˙영등포와 강남을 잇는 교통의 요지")
   image22 = st.image(image2, use_column_width=True)
   st.write("- 경기 서남부로 연결되는 관문 - 과천, 광명, 시흥, 부천")
   image33 = st.image(image3, use_column_width=True)
   st.caption("(출처 :서울시,  ⎡2040 서울도시기본계획⎦, 2023)")


with tab3:
    st.subheader(" ")
    st.subheader("3. 시각화 대상 시간대 선정 이유")
    st.write("- 시각화 대상 시간대 :  심야 및 새벽 시간대(오후 11시~다음날 오전 6시) → 전체 시간대(24시)")
    st.write("- 선정 이유")
    st.write("---- 원래 취지 : :red[심야 및 새벽 시간대 이용 가능 교통 수단의 한계와 교통 수단별 막차 시간의 상이]함으로 종합적으로 대중교통 정보를 확인하는 데 어려움을 느낌.")
    st.write("---- 바뀐 취지 : :red[심야 및 새벽 시간대 이용 가능 교통 수단의 수가 적어] 보다 많은 정보를 보이고자 전체 시간대로 확대.")

with tab4:
    st.subheader(" ")
    st.subheader("4. 시각화 대상 주제 선정 이유")
    st.write("- 대중교통 선정 이유")
    st.write("---- 최근 택시비 야간 할증 폭등으로 저렴한 대중교통 수요 증가.")
    image4 = Image.open('price.png')
    image44 = st.image(image4, use_column_width=True)
    st.write("---- 교통기본권이자 교통복지로서 교통사각지대 해소라는 공공성 지님.")
    st.write(" ")
    st.write("- 대상 대중교통 : 서울시 관악구를 관통하는 버스 및 공공자전거")
    st.write("---- 버스 : 서울시 시내버스 + 심야버스 + 마을버스 + 경기도 광역버스")
    st.write("---- 공공자전거 : 따릉이")
    st.write("---- 사설 공유 킥보드 및 공유자전거 제외 : 공공성 X  대중성 X 정거장 고정 X → 원천 데이터 수집의 어려움")

with tab5:
    st.subheader(" ")
    st.subheader("5. 시각화 목표")
    st.write("- 가시성 높은 대중교통 정보의 획득")
    st.write("- 승객들의 이용 패턴 파악")
    st.write('- 특정 시간대의 유동인구 파악 → 향후 서울시 안심마을보안관 사업과 연계해 보다  안전한 야간 통행권 확보에')
    st.subheader(" ")





with tab6:  
    st.header("제언")
    st.subheader(" ")
    st.subheader("6. 개선가능성")
    st.write("- 대상 지역의 확장 : 관악구 외 서울 전체로 확장 필요성")
    st.write("- 대상 대중교통의 확장 : 시내버스 및 따릉이 외 지하철 및 택시로 확장 필요성")
    st.write("- 지도 상 초정밀 버스 위치 정보 제공 필요성 : 카카오맵의 부산, 제주, 춘천 등 시내버스 실시간 위치 시각화")
    
    image6 = Image.open('app.png')
    image66 = st.image(image6, use_column_width=True)
    st.write("- 저상버스 위치 정보 제공 필요성 : 교통약자를 위한 저상버스의 실시간 위치 정보 제공의 필요성")
    image7 = Image.open('lfbus.png')
    image77 = st.image(image6, use_column_width=True)
    image8 = Image.open('news.png')
    image88 = st.image(image8, use_column_width=True)
    st.write("- 새로운 유동인구 정보를 반영한 노선 개편의 필요성 : 2013년 유동인구 밀집 지역 조사를 바탕으로 올빼미 버스 노선 설계됨. 젠트리피케이션과 구도심개발 등으로 유동 인구 밀집 지역의 일부 변화 발생. ")
    image9 = Image.open('map.png')
    image99 = st.image(image9, use_column_width=True)
    st.write("- 개별 유저의 GPS 위치 정보 사용 시 정교화 가능성")
    st.write("----  본 프로젝트는 개인정보보호를 위해 개별 유저의 GPS 위치 정보를 사용하지 않음. → 개별 유저의 GPS 위치 정보의 사용이 가능하다면 네이버지도, 카카오맵처럼 정교한 시각화 정보 제공이 가능할 것으로 기대")
    st.write("-  공공자전거 따릉이 정보 확충")
    st.write("----  실제 정거장에 정차된 자전거 개수 표시 : 따릉이 정거장을 표시했으나, 실제 정거장에 자전거가 있는지를 파악하려면 따릉이 어플을 사용해야 함.")
    st.write("----  따릉이 정거장의 고장 및 수리 여부를 지도 표시")
    image10 = Image.open('bikes.png')
    image100 = st.image(image10, use_column_width=True)
    st.write("- 환승 정보 반영할 필요성")
    st.write("---- 개별 교통수단 간의 환승 정보 파악 필요성 (버스, 지하철 등) ")
