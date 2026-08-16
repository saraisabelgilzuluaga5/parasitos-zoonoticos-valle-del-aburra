import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, get_exploded_parasites
from utils.theme import PARASITE_COLORS, PARASITE_COLORS_ITALIC, POSITIVE_COLOR, NEGATIVE_COLOR, italicize

df = load_data()
exploded = get_exploded_parasites(df)

with st.sidebar:
    parasitos_sel = st.multiselect("Parásito(s)", sorted(exploded["parasito"].unique()), default=sorted(exploded["parasito"].unique()))
    municipios_sel = st.multiselect("Municipio(s)", sorted(df["Municipio"].unique()), default=sorted(df["Municipio"].unique()))

exploded_f = exploded[exploded["parasito"].isin(parasitos_sel) & exploded["Municipio"].isin(municipios_sel)]
df_f = df[df["Municipio"].isin(municipios_sel)]

# 1. Donut: proportional distribution of detections
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de detecciones por especie")
    det_counts = exploded_f["parasito"].value_counts().reset_index()
    det_counts.columns = ["Parásito", "Detecciones"]
    total_det = det_counts["Detecciones"].sum()
    det_counts["Porcentaje"] = (det_counts["Detecciones"] / total_det * 100).round(1)
    det_counts["Parásito_display"] = det_counts["Parásito"].apply(italicize)

    fig1 = px.pie(
        det_counts, values="Detecciones", names="Parásito_display",
        color="Parásito_display", color_discrete_map=PARASITE_COLORS_ITALIC,
        hole=0.5,
    )
    fig1.update_traces(textinfo="label+percent+value")
    fig1.update_layout(margin=dict(t=20, b=20))
    st.plotly_chart(fig1, width="stretch")
    st.caption(f"Total de detecciones: {total_det}")

# 2. Type of parasitism
with col2:
    st.subheader("Tipo de parasitismo")
    positivas_f = df_f[df_f["es_positiva"]]
    n_positivas = len(positivas_f)
    n_poli = (positivas_f["parasitos_lista"].apply(len) > 1).sum()
    n_unico = n_positivas - n_poli

    parasitism_df = pd.DataFrame({
        "Tipo": ["Parasitismo único", "Poliparasitismo (≥2)"],
        "n": [n_unico, n_poli],
    })
    parasitism_df["Porcentaje"] = (parasitism_df["n"] / n_positivas * 100).round(1) if n_positivas > 0 else 0

    fig2 = px.pie(
        parasitism_df, values="n", names="Tipo",
        color="Tipo", color_discrete_map={"Parasitismo único": "#457B9D", "Poliparasitismo (≥2)": "#E63946"},
        hole=0.5,
    )
    fig2.update_traces(textinfo="label+percent+value")
    fig2.update_layout(margin=dict(t=20, b=20))
    st.plotly_chart(fig2, width="stretch")
    st.caption(f"Muestras positivas: {n_positivas}")

# 3. Grouped bar: frequency per parasite per municipality
st.subheader("Frecuencia de cada parásito por municipio")
freq_mun = exploded_f.groupby(["Municipio", "parasito"]).size().reset_index(name="Detecciones")
freq_mun["Parásito"] = freq_mun["parasito"].apply(italicize)
fig3 = px.bar(
    freq_mun, x="Municipio", y="Detecciones", color="Parásito",
    color_discrete_map=PARASITE_COLORS_ITALIC,
    barmode="group", text="Detecciones",
)
fig3.update_layout(xaxis_tickangle=-45, margin=dict(b=80))
st.plotly_chart(fig3, width="stretch")

# 4. Coinfection table
st.subheader("Muestras con poliparasitismo (coinfecciones)")
coinfections = positivas_f[positivas_f["parasitos_lista"].apply(len) > 1][
    ["Código de la muestra", "Municipio", "Parque Público", "Parásito zoonótico observado"]
].reset_index(drop=True)
if len(coinfections) > 0:
    st.dataframe(coinfections, width="stretch", hide_index=True)
else:
    st.info("No se encontraron coinfecciones en la selección actual.")

# 5. Structure type
st.subheader("Tipo de estructura parasitaria encontrada")
positivas_all = df_f[df_f["es_positiva"]]
struct_counts = positivas_all["Estructuras Parasitarias"].value_counts().reset_index()
struct_counts.columns = ["Estructura", "n"]
# Filter out the "no structures" label
struct_counts = struct_counts[~struct_counts["Estructura"].str.contains("No se observan", na=False)]
fig5 = px.bar(
    struct_counts, x="Estructura", y="n", text="n",
    color_discrete_sequence=["#2A9D8F"],
    labels={"n": "Muestras", "Estructura": "Tipo de estructura"},
)
fig5.update_layout(showlegend=False)
st.plotly_chart(fig5, width="stretch")

# Health context
with st.expander("ℹ️ Relevancia para la salud pública"):
    st.markdown("""
    - ***Ancylostoma caninum***: Causa larva migrans cutánea. Riesgo al caminar descalzo en parques contaminados. ~740 millones de infecciones humanas anuales a nivel mundial.
    - ***Toxocara canis***: Causa larva migrans visceral y ocular, especialmente en niños. Los huevos permanecen viables en el suelo durante años.
    - ***Giardia intestinalis***: Causa giardiasis (diarrea, malabsorción). Transmisión fecal-oral directa, relevante en niños que juegan en parques.
    - ***Trichuris vulpis***: Causa tricuriasis. Huevos altamente resistentes en el ambiente (30-60 días para volverse infectantes).
    """)
