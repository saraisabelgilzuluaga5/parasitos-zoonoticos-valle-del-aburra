import streamlit as st
import plotly.express as px
from utils.data_loader import load_data, get_exploded_parasites
from utils.theme import POSITIVE_COLOR, NEGATIVE_COLOR, italicize

df = load_data()
exploded = get_exploded_parasites(df)

st.markdown(
    """
    **Área Metropolitana del Valle del Aburrá (2025-2026)**

    Dashboard interactivo del trabajo de grado de **Sara Isabel Gil Zuluaga**
    para optar al título de Microbiólogo y Bioanalista.
    Universidad de Antioquia. Tutora: Sara Yepes (MSc en Salud Pública).
    """
)

# KPIs
total = len(df)
positivas = int(df["es_positiva"].sum())
prevalencia = (positivas / total) * 100
parasito_freq = exploded["parasito"].value_counts()
parasito_mas_frecuente = parasito_freq.index[0] if len(parasito_freq) > 0 else "N/A"
prev_municipio = df.groupby("Municipio")["es_positiva"].mean() * 100
municipio_max = prev_municipio.idxmax()
municipio_max_val = prev_municipio.max()

with st.container(horizontal=True):
    st.metric("Total muestras", f"{total}", border=True)
    st.metric("Prevalencia general", f"{prevalencia:.1f}%", border=True)
    st.metric("Parásito más frecuente", italicize(parasito_mas_frecuente, "md"), border=True)
    st.metric("Mayor prevalencia", f"{municipio_max} ({municipio_max_val:.1f}%)", border=True)

# Main content
col_left, col_right = st.columns([1, 2])

with col_left:
    with st.container(border=True):
        st.subheader("Resultado general")
        result_df = df["es_positiva"].value_counts().reset_index()
        result_df.columns = ["Resultado", "n"]
        result_df["Resultado"] = result_df["Resultado"].map({True: "Positiva", False: "Negativa"})
        fig = px.pie(
            result_df, values="n", names="Resultado",
            color="Resultado",
            color_discrete_map={"Positiva": POSITIVE_COLOR, "Negativa": NEGATIVE_COLOR},
            hole=0.5,
        )
        fig.update_traces(textinfo="label+percent+value")
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig)

with col_right:
    with st.container(border=True):
        st.subheader("Distribución de muestras por municipio y parque")
        table_df = (
            df.groupby(["Municipio", "Parque Público"])
            .agg(Muestras=("es_positiva", "count"), Positivas=("es_positiva", "sum"))
            .reset_index()
        )
        table_df["Positivas"] = table_df["Positivas"].astype(int)
        st.dataframe(table_df, hide_index=True)

st.download_button(
    "Descargar dataset",
    icon=":material/download:",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="coprologicos.csv",
    mime="text/csv",
)
