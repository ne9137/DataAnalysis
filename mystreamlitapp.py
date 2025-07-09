#C:\Users\User\2025_DA_kne\day6\0703_web.py
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
plt.rcParams.update( {'font.family' : 'malgun Gothic'})  # 한글 폰트



# graph 관련 warning 이 나오지 않게 세팅하기
import warnings
warnings.filterwarnings(action='ignore')
#warning이 원래 기본 세팅으로 변경하기 (기본세팅 = warning 표시)
#warnings.filterwarnings(action='default') 

#2. 한글 폰트 설정
# 시각화 모듈 임포트
import matplotlib.pyplot as plt

# unicode minus를 사용하지 않기 위한 설정 (minus 깨짐현상 방지)
plt.rcParams['axes.unicode_minus'] = False
# font를 나눔고딕으로 세팅 'NanumGothic'  - windows
plt.rcParams['font.family'] = 'NanumGothic'

import json
import folium
from streamlit_folium import st_folium

import re
import konlpy
from wordcloud import WordCloud
import PIL




st.sidebar.image('rabbit_icon.png')
theme = st.sidebar.selectbox("분석주제",
                             ['Home','영화데이터분석','자동차분석',
                              '학생시험분석','경제데이터분석','기온데이터분석',
                              '국내인구데이터분석',"워드클라우드"])

def readcsv(a):
    st.title(theme)
    b = pd.read_csv(a)
    st.dataframe(b)
    return b

def plot(n,d,a,b,h=None):
    f = plt.figure()

    if n == "box":
        sns.boxplot(data = d, x = a, y = b, hue = h)
    elif n == "line":
        sns.lineplot(data = d, x = a, y = b, hue = h)
    elif n == "bar":
        sns.barplot(data = d, x = a, y = b, hue = h)
    elif n == "scatter":
        sns.scatterplot(data = d, x = a, y = b, hue = h)
    
    st.pyplot(f)


def page_home():
    st.title("ʜɪ⚞₍⑅ᐢ.ˬ.ᐢ₎♡")
    st.image("rabbits.webp")

def page_car():
    mpg = readcsv('mpg.csv')
    f1 = plt.figure()
    sns.scatterplot(data=mpg, x='displ', y = 'hwy', hue = 'drv')
    st.pyplot(f1)

    ff1 = px.scatter(data_frame = mpg, x='displ', y = 'hwy', color = 'drv')
    st.plotly_chart(ff1)


    st.header("drv에따른 cty 평균을 막대그래프로 비교하기")
    mpg_data = mpg.groupby('drv',as_index=False).agg(drv_cty_mean = ('cty','mean'))
    plot("bar", mpg_data, 'drv', 'drv_cty_mean')
    st.dataframe(mpg_data)
    ff2 = px.bar(data_frame = mpg_data, x = 'drv', y = 'drv_cty_mean')
    st.plotly_chart(ff2)
    st.dataframe(mpg_data.info())
    

    st.header("manufacturer에 다른 cty 평균 연비 구하기")
    mpg_data = mpg.groupby('manufacturer',as_index=False).agg(m_cty_mean = ('cty','mean'))
    plot("bar", mpg_data,'m_cty_mean','manufacturer')  
    ff3 = px.bar(data_frame=mpg_data,x='m_cty_mean',y='manufacturer')
    # index를 인식x, column만 인식한다.
    # ,as_index=False를 사용해서 index는 남겨두게 해주면됨.
    st.plotly_chart(ff3)

    selected = st.selectbox('select manufacturer - by .unique()', mpg['manufacturer'].unique())
    st.dataframe(mpg.query('manufacturer == @selected'))

    type_selected = st.selectbox("분류를 선택", ['manufacturer','displ','drv','fl'])
    driveway_selected = st.selectbox("도로종류", ['cty','hwy'])
    func_selected = st.selectbox("계산", ['max','min','mean'])

    mpg_dataselected = mpg.groupby(type_selected)\
                          .agg(sorted_data = (driveway_selected,func_selected))
    st.dataframe(mpg_dataselected)
    st.text(type_selected + " 에 따른 분류의 " + driveway_selected + " 의 " + func_selected + " 입니다.")
    plot("bar", mpg_dataselected, type_selected, 'sorted_data')
    st.header("구동방식(drv)별 고속도로 연비(hwy)")
    plot("box",mpg,'drv','hwy')

    st.header("자동차 category 중 'compact', 'subcompact', 'suv'에 대한 도시 연비(cty) 비교")
    mpg_data2 = mpg.query('category in ["compact", "subcompact", "suv"]')

    #sns.boxplot(data = mpg_data, x = 'category', y = 'cty')
    plot("box", mpg_data2,'category','cty')

    st.header("category 'compact', 'subcompact', 'suv'에 대한 도시 연비(cty)의 평균 비교")
    mpg_ctg = mpg.groupby('category').agg(cty_mean = ('cty','mean'))
    mpg_ctg_data = mpg_ctg.query('category in ["compact", "subcompact", "suv"]') #in[]방식
    # mpg_ctg_data = mpg.query('category == "compact"|category == "subcompact"|category == "suv"') or방식

    # sns.barplot(data = mpg_ctg_data, x = 'category', y = 'cty_mean')
    plot("bar", mpg_ctg_data, 'category','cty_mean')

    # 산점도 그리기
    st.header("plotly chart - x='displ', y='cty' 산점도 입니다.")
    mpg_scatter = px.scatter(data_frame=mpg, x='displ', y='cty', color = 'drv' )
    st.plotly_chart(mpg_scatter)


def page_exam():
    exam = readcsv('exam.csv')
    
def page_economics():
    economics = readcsv('economics.csv')

    st.text("연도별 개인 저축률의 변화 그래프")
    economics['year'] = pd.to_datetime(economics['date']).dt.year
    economics['month'] = pd.to_datetime(economics['date']).dt.month
    economics['day'] = pd.to_datetime(economics['date']).dt.day
    plot("line",economics,'year','psavert')

    st.text("2014년 월별 psavert(개인 저축률)의 변화")
    plot("line",economics.query('year == 2014'),'month','psavert')

def page_midtest():
    movie = pd.read_csv('m10.csv')
    st.title("영화데이터분석")
    st.header("가장 높은 평균평점을 받은 영화 top 10")
    movie_data = movie.groupby('영화제목').agg(평균평점 = ('평점','mean'),평가횟수 = ('영화제목','count'))
    st.dataframe(movie_data.sort_values('평균평점',ascending = False).head(10))

    st.header("가장 많은 사람이 평가한 영화 top 5")
    st.dataframe(movie_data.sort_values('평가횟수',ascending = False).head(5))

    st.header("#600명 이상 평가를 한 영화 중에 평균 평점이 높은 순서") 
    st.dataframe(movie_data.query('평가횟수 >= 600').sort_values('평균평점',ascending = False))

    st.header("영화  Toy Story (1995) 를 평가한 사람들의 연령의 분포")
    toy_story_data = movie.query('영화제목 == "Toy Story (1995)"')\
                      .groupby("연령",as_index=False)\
                      .agg(평가인원 = ('연령','count'))
    st.dataframe(toy_story_data)
    fig1=plt.figure()
    sns.histplot(toy_story_data,x="연령",y="평가인원")
    st.pyplot(fig1)

    st.header("여자들이 제일 높은 평균 평점을 준 영화 top 10")
    movie_data2 = movie.query('성별 == "F"').groupby('영화제목').agg(여성평균평점 = ('평점','mean'))
    st.dataframe(movie_data2.sort_values('여성평균평점',ascending = False).head(10))

    st.header("가장 평점을  많이 준 사람의 사용자아이디 10개")
    st.dataframe(movie.groupby('사용자아이디').agg(평가횟수 = ('사용자아이디','count')).sort_values('평가횟수',ascending=False).head(10))

    st.header("사람들이 좋은 평점을 준 영화 장르\n")
    movie_by_genre = movie.groupby('장르').agg(장르별평균평점 = ('평점','mean'), 평가인원 = ('장르','count'))\
                          .sort_values('장르별평균평점',ascending=False)
    st.dataframe(movie_by_genre)


def page_temp():
    
    temp_raw = pd.read_csv('ta_20240119085216.csv',
    encoding='cp949', # 한글 encoding
    header = 6) #index 0~6은 헤더임, 7부터 읽게함(엑셀에서 8)
    temp = temp_raw.copy()
    st.title("기온데이터분석")
    temp.rename(columns = {'평균기온(℃)' : '평균기온',
                       '최저기온(℃)' : '최저기온',
                       '최고기온(℃)' : '최고기온'},
            inplace = True)
    temp['날짜'] = temp['날짜'].str.replace('\t','')
    temp['월'] = pd.to_datetime(temp['날짜']).dt.month
    temp['일'] = pd.to_datetime(temp['날짜']).dt.day
    temp['일교차'] = temp['최고기온'] - temp['최저기온']
    st.dataframe(temp)
    temp_monthly_mean = temp.groupby('월').agg(월별일교차 = ('일교차','mean'))
    t_fig = plt.figure()
    sns.barplot(data = temp_monthly_mean, x = '월', y = '월별일교차')
    st.pyplot(t_fig)
            

def page_test():
    st.title("test")

def page_pop2():
    df = pd.read_excel('seoul_univ.xlsx',index_col=0)
    seoul_map3 = folium.Map(location = [37.55, 126.98],
                        zoom_start = 12,
                        tiles = 'cartodbpositron')
    for name,lat,lng in zip(df.index,df.위도,df.경도):
        folium.Marker([lat,lng], popup=name).add_to(seoul_map3)

    st_data = st_folium(seoul_map3, width=725)

    # folium,CircleMarker([lat,lng],radius=10,color='brown',fill = True, fill_color = 'coral',
    #                     fill_opacity=0.7,popup=name).add_to(seoul_map3)
    # seoul_map3.save('seoul_univ.html')
    # seoul_map3.show_in_browser()

def page_pop():
    df_pop = pd.read_csv('Population_SIG.csv')
    geo = json.load(open('SIG.geojson',encoding = 'UTF-8'))

    bins = list(df_pop['pop'].quantile([0,0.2,0.4,0.6,0.8,1]))
    map_sig1 = folium.Map(location = [37.567018, 126.978253],
                     zoom_start = 10,
                     tiles = 'cartodbpositron')# cartodbpositron, openstreetmap등 지도스타일
    # folium.Choropleth( 
    #     geo_data = geo,
    #     data =df_pop,
    #     columns = ('code','pop'),
    #     key_on = 'feature.properties.SIG_CD',
    #     fill_color = 'YlGnBu',
    #     fill_opacity = 1,
    #     line_opacity = 0.5,
    #     bins = bins).add_to(map_sig)
    


    folium.Marker(location = [37.459202, 127.153747],
                  popup="성남폴리텍", tooltip="성남폴리텍").add_to(map_sig1)
    
    folium.CircleMarker(location = [37.337910, 127.119279],
                  popup="집", tooltip="집").add_to(map_sig1)

    st_data = st_folium(map_sig1, width=725)

    #folium.streamlit.app 에서 자세하게 찾아볼 수 있음

def page_folium():
    folium_select = st.selectbox("Select :", ["Population","University"])
    if folium_select == "Population":
        page_pop()
    elif folium_select == "University":
        page_pop2()

def page_wordcloud():
    st.title("WordCloud")
    kbo_allstar_game = open('kbo_allstar_game.txt',encoding = 'UTF-8').read()
    kbo_allstar_game = re.sub('[^가-힣]',' ',kbo_allstar_game)
    hannanum = konlpy.tag.Hannanum()
    nouns = hannanum.nouns(kbo_allstar_game)
    df_word = pd.DataFrame({'word' : nouns})
    df_word['word_n'] = df_word['word'].str.len()
    df_word = df_word.query('word_n >= 2')
    df_word.sort_values('word')
    df_word = df_word.groupby('word', as_index=False) \
                .agg(n = ('word', 'count')) \
                .sort_values('n', ascending=False)
    nouns2 = hannanum.nouns(kbo_allstar_game)
    df = pd.DataFrame({'word': nouns2})
    df1=df.assign(word_count = df['word'].str.len())\
        .query("word_count >=2")\
            .groupby('word', as_index=False )\
                .agg(횟수 = ('word', 'count'))\
                    .sort_values('횟수', ascending=False)\
                        .head(20)
    
    font = 'DoHyeon-Regular.ttf'
    dic_word = df_word.set_index('word').to_dict()['n']
    wc = WordCloud(random_state = 100,
                # colormap = 'hot',
                font_path = font,
                width = 1000,height = 1000,
                background_color = 'ivory')
    img_wordcloud = wc.generate_from_frequencies(dic_word)

    # word_fig = plt.figure(figsize = (5,5))
    # plt.axis('off')
    # plt.imshow(img_wordcloud)
    # st.pyplot(word_fig)
    icon = PIL.Image.open('star.jpg')
    img = np.array(icon)
    wc = WordCloud(random_state = 200,
               font_path = font,
               width = 1000,
               height = 1000,
               colormap = 'YlOrBr',
               # contour_width = 1,
               # contour_color = 'brown',
               background_color = 'white',
               mask = img)
    img_wordcloud = wc.generate_from_frequencies(dic_word)

    fig = plt.figure(figsize = (10,10))
    plt.axis('off')
    plt.imshow(img_wordcloud)    
    st.pyplot(fig)

    st.dataframe(df1)






if theme == "test":
    page_test()
    
elif theme == "Home":
    page_home()
    
elif theme == "자동차분석":
    page_car()  

elif theme == "학생시험분석":
    page_exam()

elif theme == "경제데이터분석":
    page_economics()

elif theme == "영화데이터분석":
    page_midtest()

elif theme == "기온데이터분석":
    page_temp()

elif theme == "국내인구데이터분석":
    page_folium()

elif theme == "워드클라우드":
    page_wordcloud()




