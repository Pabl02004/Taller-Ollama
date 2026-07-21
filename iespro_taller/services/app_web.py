import streamlit as st

st.set_page_config(page_title="Taller Ollama", page_icon="🔑")

# Inicializar estado de autenticación
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- PANTALLA DE INICIO DE SESIÓN ---
def show_login():
    st.title("Iniciar Sesión")
    
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Ingresar")
        
        if submit:
            # Aquí puedes conectar tu función de validación de base de datos MySQL o usuarios
            if username and password:  # Reemplazar con lógica real de validación
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Por favor ingresa usuario y contraseña válidos.")

# --- PANTALLA PRINCIPAL (CHAT IA) ---
def show_chat():
    st.sidebar.title(f"Bienvenido, {st.session_state.get('username', 'Usuario')}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()

    st.title("Taller Ollama Agent 🤖")

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
            response = f"Procesando respuesta para: {prompt}"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Flujo de la aplicación
if not st.session_state.authenticated:
    show_login()
else:
    show_chat()