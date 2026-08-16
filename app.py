import streamlit as st

st.set_page_config(
    page_title="Parásitos zoonóticos - Valle del Aburrá",
    page_icon=":material/microbiology:",
    layout="wide",
)


def check_password():
    """Gate the app behind a password stored in st.secrets."""
    if st.session_state.get("authenticated"):
        return True

    st.title("Acceso restringido")
    st.markdown("Este dashboard es parte de un trabajo de grado. Ingrese la contraseña proporcionada en el documento.")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar", icon=":material/login:"):
        if password == st.secrets["password"]:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta.")
    return False


if not check_password():
    st.stop()

page = st.navigation(
    [
        st.Page("app_pages/home.py", title="Resumen", icon=":material/home:"),
        st.Page("app_pages/prevalencia.py", title="Prevalencia", icon=":material/bar_chart:"),
        st.Page("app_pages/parasitos.py", title="Parásitos", icon=":material/bug_report:"),
        st.Page("app_pages/diagnostico.py", title="Diagnóstico", icon=":material/biotech:"),
        st.Page("app_pages/macroscopico.py", title="Macroscópico", icon=":material/science:"),
    ],
    position="top",
)

page.run()
