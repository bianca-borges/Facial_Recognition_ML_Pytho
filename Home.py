import streamlit as st
# from auth import authenticator
st.set_page_config(page_title='Sistema de Presença',layout='wide')



with st.spinner("Iniciando Componentes"):
    import face_rec


st.header('Sistema de Reconhecimento Facial')

st.success('Modelo carregado!')
st.success('Banco de dados carregado!')



