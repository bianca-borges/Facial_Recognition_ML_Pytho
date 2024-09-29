import streamlit as st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time


st.subheader('Sistema de Presença')

with st.spinner('Recuperando dados do banco ...'):
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)

st.success("Dados recuperados com sucesso!")

waitTime = 30
setTime = time.time()
realtimepred = face_rec.RealTimePred()

def video_frame_callback(frame):
    global setTime

    img = frame.to_ndarray(format="bgr24")
    pred_img = realtimepred.face_prediction(img,redis_face_db,
                                        'facial_features',['Name','Role'],thresh=0.5)

    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time()
        print('Salvando no banco')


    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback,
rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)