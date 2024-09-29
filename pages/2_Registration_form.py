import streamlit as st
from Home import face_rec
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av


st.subheader('Formulario')

registration_form = face_rec.RegistrationForm()

def video_callback_func(frame):
    img = frame.to_ndarray(format='bgr24')
    reg_img, embedding = registration_form.get_embedding(img)

    if embedding is not None:
        with open('face_embedding.txt',mode='ab') as f:
            np.savetxt(f,embedding)

    return av.VideoFrame.from_ndarray(reg_img,format='bgr24')


with st.container(border=True):
    name = st.text_input(label='Name',placeholder='Nome completo')
    role = st.selectbox(label='Role', placeholder='Selecione papel', options=('--selecione--',
                                                                          'Estudante', 'Professor'))
    course = st.selectbox(label='Selecione curso', placeholder='Selecione curso',
                          options=('--selecione--','Ciencias da Computação',
                                   'Elétrica','Eletronica'))
    year_level = st.selectbox(label='Periodo', placeholder='Periodo',
                              options=('--selecione--', 'I - Primeiro',
                                       'II - Segundo',
                                       'III - Terceiro','IV - Quarto'))
    address = st.text_area(label='Address', placeholder='Endereço')
    contact = st.text_input(label='Contact Number', placeholder='Numero')
    email = st.text_input(label='Email', placeholder='E-mail')

    st.write('Click no botão Start para coletar sua imagem')
    with st.expander('Instruções'):
        st.caption('1. Faça expressões diferentes para capturar os detalhes do seu rosto.')
        st.caption('2. Click em stop após 200 amostras coletadas.')

    webrtc_streamer(key='registration', video_frame_callback=video_callback_func,
                    rtc_configuration={
                        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                    }
                    )



if st.button('Submit'):
    return_val = registration_form.save_data_in_redis_db(name,role)
    if return_val == True:
        st.success(f"{name} registrado com suecesso!")
    elif return_val == 'name_false':
        st.error('O campo Name não pode estar vazio.')

    elif return_val == 'file_false':
        st.error('face_embedding.txt não encontrada.')

# else:
#     authenticator.login('Login', 'main')
        
