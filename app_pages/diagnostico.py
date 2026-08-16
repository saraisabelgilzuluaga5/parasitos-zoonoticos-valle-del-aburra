import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, get_exploded_parasites
from utils.theme import PARASITE_COLORS, PARASITE_COLORS_ITALIC, POSITIVE_COLOR, NEGATIVE_COLOR, italicize

df = load_data()
exploded = get_exploded_parasites(df)

TECNICAS = {
    "Examen Directo (Sol. Salina)": "Hallazgos Examen Directo (Solución Salina)",
    "Examen Directo (Lugol)": "Hallazgos Examen Directo (Lugol)",
    "Flotación de Sheather": "Halazgos Flotación de Sheather",
}

with st.sidebar:
    municipios_sel = st.multiselect("Municipio(s)", sorted(df["Municipio"].unique()), default=sorted(df["Municipio"].unique()))
df_f = df[df["Municipio"].isin(municipios_sel)]
total = len(df_f)

# 1. Positivity by technique
st.subheader("Positividad por técnica coproparasitológica")

tech_data = []
for label, col in TECNICAS.items():
    n_pos = (df_f[col] == "Positivo").sum()
    pct = (n_pos / total) * 100 if total > 0 else 0
    tech_data.append({"Técnica": label, "Positivas": n_pos, "Positividad (%)": round(pct, 1)})

tech_df = pd.DataFrame(tech_data).sort_values("Positividad (%)", ascending=True)

fig1 = px.bar(
    tech_df, x="Positividad (%)", y="Técnica", orientation="h",
    text=tech_df.apply(lambda r: f"{r['Positividad (%)']:.1f}% (n={r['Positivas']})", axis=1),
    color_discrete_sequence=[POSITIVE_COLOR],
)
fig1.update_layout(showlegend=False, height=300, margin=dict(l=0))
fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, width="stretch")

st.caption(f"Porcentajes calculados sobre {total} muestras analizadas. Cada muestra fue procesada con las tres técnicas.")

# 2. Concordance heatmap
st.subheader("Concordancia entre métodos diagnósticos")

positivas_f = df_f[df_f["es_positiva"]].copy()
n_pos = len(positivas_f)

cols_short = list(TECNICAS.keys())
cols_real = list(TECNICAS.values())

# Build boolean columns for positivity per technique
for short, real in zip(cols_short, cols_real):
    positivas_f[short] = positivas_f[real] == "Positivo"

# Concordance matrix
concordance = pd.DataFrame(index=cols_short, columns=cols_short, dtype=int)
for i, t1 in enumerate(cols_short):
    for j, t2 in enumerate(cols_short):
        concordance.loc[t1, t2] = int((positivas_f[t1] & positivas_f[t2]).sum())

fig2 = px.imshow(
    concordance.values.astype(int),
    x=cols_short, y=cols_short,
    text_auto=True, aspect="auto",
    color_continuous_scale="Blues",
    labels=dict(color="Muestras"),
)
fig2.update_layout(height=350, margin=dict(l=0))
st.plotly_chart(fig2, width="stretch")
st.caption("Diagonal: total de positivos por cada técnica. Fuera de diagonal: muestras detectadas por ambas técnicas simultáneamente.")

# 3. Detection by technique per parasite
st.subheader("Detección por técnica según parásito")

exploded_f = exploded[exploded["Municipio"].isin(municipios_sel)]
detection_data = []

for _, row in exploded_f.iterrows():
    for short, real in TECNICAS.items():
        if row[real] == "Positivo":
            detection_data.append({"Parásito": row["parasito"], "Técnica": short})

if detection_data:
    det_df = pd.DataFrame(detection_data)
    det_df["Parásito"] = det_df["Parásito"].apply(italicize)
    det_counts = det_df.groupby(["Parásito", "Técnica"]).size().reset_index(name="Detecciones")
    fig3 = px.bar(
        det_counts, x="Parásito", y="Detecciones", color="Técnica",
        barmode="group", text="Detecciones",
        color_discrete_sequence=["#457B9D", "#2A9D8F", "#E9C46A"],
    )
    fig3.update_layout(xaxis_tickangle=-45, margin=dict(b=80))
    st.plotly_chart(fig3, width="stretch")
else:
    st.info("No hay datos para la selección actual.")

# 4. Combination table
st.subheader("Combinaciones de métodos en muestras positivas")

positivas_f["Combinación"] = positivas_f.apply(
    lambda r: " + ".join([t for t in cols_short if r[t]]) or "Ninguno positivo", axis=1
)
combo_counts = positivas_f["Combinación"].value_counts().reset_index()
combo_counts.columns = ["Combinación de técnicas", "Muestras"]
st.dataframe(combo_counts, width="stretch", hide_index=True)

# Context
with st.expander("ℹ️ Nota metodológica"):
    st.markdown("""
    **Flotación de Sheather:** Solución de sacarosa (densidad 1.27) con centrifugación a 2500 rpm por 5 minutos.
    Método principal para detección de huevos de helmintos (*A. caninum*, *T. canis*, *T. vulpis*).

    **Examen directo con solución salina:** Facilita la visualización de trofozoitos móviles de *Giardia intestinalis*.

    **Examen directo con Lugol:** Tiñe estructuras internas de quistes, mejorando la identificación morfológica.
    """)
