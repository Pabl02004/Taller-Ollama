import os
import streamlit as st

st.set_page_config(page_title="Taller Ollama", page_icon="🤖")
st.title("Taller Ollama Agent")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu consulta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Aquí conectamos con la lógica del agente
        response = f"Procesando respuesta para: {prompt}"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})