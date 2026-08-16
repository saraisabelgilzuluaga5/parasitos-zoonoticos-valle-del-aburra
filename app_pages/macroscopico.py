import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from utils.theme import POSITIVE_COLOR, NEGATIVE_COLOR

df = load_data()

with st.sidebar:
    municipios_sel = st.multiselect("Municipio(s)", sorted(df["Municipio"].unique()), default=sorted(df["Municipio"].unique()))
    parasitos_all = sorted(set(p for lst in df["parasitos_lista"] for p in lst))
    parasitos_sel = st.multiselect("Parásito(s)", parasitos_all, default=parasitos_all)

df_f = df[df["Municipio"].isin(municipios_sel)]
total = len(df_f)

# 1. Consistency distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("Consistencia de las heces")
    consist = df_f["Consistencia"].value_counts().reset_index()
    consist.columns = ["Consistencia", "n"]
    consist["Porcentaje"] = (consist["n"] / total * 100).round(1)
    fig1 = px.bar(
        consist, x="Consistencia", y="n",
        text=consist.apply(lambda r: f"{r['n']} ({r['Porcentaje']}%)", axis=1),
        color_discrete_sequence=["#457B9D"],
    )
    fig1.update_layout(showlegend=False, yaxis_title="Muestras")
    fig1.update_traces(textposition="outside")
    st.plotly_chart(fig1, width="stretch")

# 2. Color distribution
with col2:
    st.subheader("Color de las heces")
    color = df_f["Color"].value_counts().reset_index()
    color.columns = ["Color", "n"]
    color["Porcentaje"] = (color["n"] / total * 100).round(1)
    fig2 = px.bar(
        color, x="Color", y="n",
        text=color.apply(lambda r: f"{r['n']} ({r['Porcentaje']}%)", axis=1),
        color_discrete_sequence=["#2A9D8F"],
    )
    fig2.update_layout(showlegend=False, yaxis_title="Muestras")
    fig2.update_traces(textposition="outside")
    st.plotly_chart(fig2, width="stretch")

# 3. Macroscopic findings
st.subheader("Presencia de hallazgos macroscópicos")
hallazgos = {
    "Sangre": "Examen Macroscopico  -  Presencia de sangre",
    "Moco": "Examen Macroscopico  - Presencia de moco",
    "Alimentos sin digerir": "Examen Macroscopico -  Presencia de alimentos sin digerir",
}

hallazgo_data = []
for label, col in hallazgos.items():
    if col in df_f.columns:
        n_present = (df_f[col] == "Presente").sum()
        pct = (n_present / total * 100) if total > 0 else 0
        hallazgo_data.append({"Hallazgo": label, "Presente": n_present, "Porcentaje": round(pct, 1)})

hallazgo_df = pd.DataFrame(hallazgo_data).sort_values("Porcentaje", ascending=True)
fig3 = px.bar(
    hallazgo_df, x="Porcentaje", y="Hallazgo", orientation="h",
    text=hallazgo_df.apply(lambda r: f"{r['Porcentaje']}% (n={r['Presente']})", axis=1),
    color_discrete_sequence=[POSITIVE_COLOR],
)
fig3.update_layout(showlegend=False, height=250, xaxis_title="Presencia (%)", margin=dict(l=0))
fig3.update_traces(textposition="outside")
st.plotly_chart(fig3, width="stretch")

# 4. Consistency vs positivity
st.subheader("Relación entre características macroscópicas y positividad parasitaria")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Consistencia vs Positividad**")
    consist_pos = df_f.groupby("Consistencia").agg(
        total=("es_positiva", "count"),
        positivas=("es_positiva", "sum"),
    ).reset_index()
    consist_pos["Positividad (%)"] = (consist_pos["positivas"] / consist_pos["total"] * 100).round(1)
    fig4 = px.bar(
        consist_pos, x="Consistencia", y="Positividad (%)",
        text=consist_pos.apply(lambda r: f"{r['Positividad (%)']:.1f}% ({int(r['positivas'])}/{int(r['total'])})", axis=1),
        color_discrete_sequence=[POSITIVE_COLOR],
    )
    fig4.update_layout(showlegend=False)
    fig4.update_traces(textposition="outside")
    st.plotly_chart(fig4, width="stretch")

# 5. Moco/alimentos vs positivity
with col4:
    st.markdown("**Presencia de moco/alimentos vs Positividad**")
    relation_data = []
    for label, col in {"Moco": hallazgos["Moco"], "Alimentos sin digerir": hallazgos["Alimentos sin digerir"]}.items():
        if col in df_f.columns:
            for val in ["Presente", "Ausente"]:
                subset = df_f[df_f[col] == val]
                n = len(subset)
                pos = subset["es_positiva"].sum()
                pct = (pos / n * 100) if n > 0 else 0
                relation_data.append({"Hallazgo": label, "Estado": val, "Positividad (%)": round(pct, 1), "n": n})

    rel_df = pd.DataFrame(relation_data)
    fig5 = px.bar(
        rel_df, x="Hallazgo", y="Positividad (%)", color="Estado",
        barmode="group",
        text=rel_df["Positividad (%)"].apply(lambda x: f"{x:.1f}%"),
        color_discrete_map={"Presente": POSITIVE_COLOR, "Ausente": NEGATIVE_COLOR},
    )
    fig5.update_traces(textposition="outside")
    st.plotly_chart(fig5, width="stretch")

# 6. Table of positive samples characteristics
st.subheader("Características macroscópicas de muestras positivas")
if parasitos_sel:
    pos_filter = df_f[df_f["parasitos_lista"].apply(lambda lst: any(p in parasitos_sel for p in lst))]
else:
    pos_filter = df_f[df_f["es_positiva"]]

display_cols = ["Código de la muestra", "Municipio", "Parque Público", "Color", "Consistencia",
                "Examen Macroscopico  - Presencia de moco", "Examen Macroscopico -  Presencia de alimentos sin digerir",
                "Parásito zoonótico observado"]
available_cols = [c for c in display_cols if c in pos_filter.columns]
st.dataframe(pos_filter[available_cols].reset_index(drop=True), width="stretch", hide_index=True)
