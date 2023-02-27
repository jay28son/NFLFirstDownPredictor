import streamlit as st
import pandas as pd
import dill as pickle

st.title('NFL Play Predictor')
with st.sidebar:
    posteam = st.selectbox(
        'Possession Team',
        ('SF', 'ARI', 'CHI', 'DET', 'CLE', 'BAL', 'LA', 'DAL', 'GB', 'MIN',
       'HOU', 'KC', 'IND', 'JAX', 'CIN', 'LAC', 'LV', 'CAR', 'MIA', 'NE',
       'NYJ', 'BUF', 'WAS', 'PHI', 'NYG', 'PIT', 'ATL', 'SEA', 'NO', 'TB',
       'TEN', 'DEN')
    )
    posteam_type = st.selectbox(
        'Home or Away',
        ('home','away')
    )
    defteam = st.selectbox(
        'Defending Team',
        ('SF', 'ARI', 'CHI', 'DET', 'CLE', 'BAL', 'LA', 'DAL', 'GB', 'MIN',
       'HOU', 'KC', 'IND', 'JAX', 'CIN', 'LAC', 'LV', 'CAR', 'MIA', 'NE',
       'NYJ', 'BUF', 'WAS', 'PHI', 'NYG', 'PIT', 'ATL', 'SEA', 'NO', 'TB',
       'TEN', 'DEN')
    )
    yards_till = st.number_input(
        'Yards Till End Zone', min_value = 0, max_value = 100
    )
    qtr = st.number_input(
        'Quarter', min_value = 1, max_value = 5
    )
    qtr_seconds = st.number_input(
        'Seconds Remaining In Quarter',min_value = 0, max_value = 900
    )
    down = st.number_input(
        'Down', min_value = 1, max_value = 4
    )
    ydstogo = st.number_input(
        'Yards Till First Down', min_value = 0,max_value = 100
    )
    posteam_score = st.number_input(
        'Possession Teams Score',min_value = 0
    )
    defteam_score = st.number_input(
        'Defending Teams Score',min_value = 0
    )

col1, col2,col3 = st.columns(3)
with col1:
    st.markdown(f"<h1 style='text-align: center; color: white;'>{posteam}.</h1>", unsafe_allow_html=True)

    st.image(f'./images/nflteams/{posteam}.png')
with col2:
    st.markdown("<h1 style='text-align: center; color: grey;'>VS.</h1>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<h1 style='text-align: center; color: white;'>{defteam}.</h1>", unsafe_allow_html=True)
    st.image(f'./images/nflteams/{defteam}.png')
bootton = st.button('Calculate')
def calculating(posteam,posteam_type,defteam,yardline_100,qtr,quarter_seconds_remaining,down,ydstogo,posteam_score,defteam_score):
    df = pd.read_pickle('./models/df.pkl')
    with open('./models/gs_xgb.pkl','rb') as f:
        model = pickle.load(f)
    classes = ['field goal', 'pass', 'punt', 'qb_kneel', 'qb spike', 'run']
    new_row = {'posteam':posteam,'posteam_type':posteam_type,'defteam':defteam,'yardline_100':yardline_100,'qtr':qtr ,'quarter_seconds_remaining':quarter_seconds_remaining,'down':down,'ydstogo':ydstogo,'posteam_score':posteam_score,'defteam_score':defteam_score}
    tests = pd.DataFrame(new_row,index = df.index)
    tests = tests.head(1)
    preds = model.predict(tests)
    preds_proba = model.predict_proba(tests)
    predicted_class_proba = round(preds_proba[0][preds[0]] * 100,2)
    return(f'Theres a {predicted_class_proba}% chance that this play will be a {classes[preds[0]]}')
def imaging(posteam,posteam_type,defteam,yardline_100,qtr,quarter_seconds_remaining,down,ydstogo,posteam_score,defteam_score):
    df = pd.read_pickle('./models/df.pkl')
    with open('./models/gs_xgb.pkl','rb') as f:
        model = pickle.load(f)
    classes = ['field goal', 'pass', 'punt', 'qb kneel', 'qb spike', 'run']
    new_row = {'posteam':posteam,'posteam_type':posteam_type,'defteam':defteam,'yardline_100':yardline_100,'qtr':qtr ,'quarter_seconds_remaining':quarter_seconds_remaining,'down':down,'ydstogo':ydstogo,'posteam_score':posteam_score,'defteam_score':defteam_score}
    tests = pd.DataFrame(new_row,index = df.index)
    tests = tests.head(1)
    preds = model.predict(tests)
    return(f'./images/plays/{classes[preds[0]]}.png')

col4,col5,col6 = st.columns(3)
if bootton:
    with col4:
        st.write(calculating(posteam,posteam_type,defteam,yards_till,qtr,qtr_seconds,down,ydstogo,posteam_score,defteam_score))
    with col5:
        st.image(imaging(posteam,posteam_type,defteam,yards_till,qtr,qtr_seconds,down,ydstogo,posteam_score,defteam_score))
