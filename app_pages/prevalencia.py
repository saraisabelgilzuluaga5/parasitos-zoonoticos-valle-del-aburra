import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_data, get_exploded_parasites
from utils.theme import PARASITE_COLORS, PARASITE_COLORS_ITALIC, POSITIVE_COLOR, NEGATIVE_COLOR, AVERAGE_LINE_COLOR, italicize

df = load_data()
exploded = get_exploded_parasites(df)

with st.sidebar:
    municipios_sel = st.multiselect("Municipio(s)", sorted(df["Municipio"].unique()), default=sorted(df["Municipio"].unique()))
    parasitos_sel = st.multiselect("Parásito(s)", sorted(exploded["parasito"].unique()), default=sorted(exploded["parasito"].unique()))

df_filtered = df[df["Municipio"].isin(municipios_sel)]
exploded_filtered = exploded[exploded["Municipio"].isin(municipios_sel) & exploded["parasito"].isin(parasitos_sel)]

prevalencia_general = (df_filtered["es_positiva"].sum() / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0

# ============================================================
st.header("Sección A: Prevalencia por Municipio")
# ============================================================

# 1. Prevalence bar chart by municipality
prev_mun = df_filtered.groupby("Municipio").agg(
    total=("es_positiva", "count"),
    positivas=("es_positiva", "sum"),
).reset_index()
prev_mun["prevalencia"] = (prev_mun["positivas"] / prev_mun["total"]) * 100
prev_mun = prev_mun.sort_values("prevalencia", ascending=True)
prev_mun["sobre_promedio"] = prev_mun["prevalencia"] >= prevalencia_general

fig1 = px.bar(
    prev_mun, x="prevalencia", y="Municipio", orientation="h",
    color="sobre_promedio",
    color_discrete_map={True: POSITIVE_COLOR, False: NEGATIVE_COLOR},
    text=prev_mun["prevalencia"].apply(lambda x: f"{x:.1f}%"),
    labels={"prevalencia": "Prevalencia (%)", "sobre_promedio": "Sobre promedio"},
)
fig1.add_vline(x=prevalencia_general, line_dash="dash", line_color=AVERAGE_LINE_COLOR,
               annotation_text=f"Promedio: {prevalencia_general:.1f}%")
fig1.update_layout(showlegend=False, height=400, margin=dict(l=0))
fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, width="stretch")

# 2. Stacked bar: positive vs negative by municipality
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Muestras positivas vs negativas")
    stack_mun = df_filtered.groupby(["Municipio", "es_positiva"]).size().reset_index(name="n")
    stack_mun["Resultado"] = stack_mun["es_positiva"].map({True: "Positiva", False: "Negativa"})
    fig2 = px.bar(
        stack_mun, x="Municipio", y="n", color="Resultado",
        color_discrete_map={"Positiva": POSITIVE_COLOR, "Negativa": NEGATIVE_COLOR},
        text="n",
    )
    fig2.update_layout(barmode="stack", xaxis_tickangle=-45, margin=dict(b=80))
    st.plotly_chart(fig2, width="stretch")

# 3. Heatmap: municipality x parasite
with col_b:
    st.subheader("Detecciones por especie y municipio")
    heat_data = exploded_filtered.groupby(["Municipio", "parasito"]).size().reset_index(name="n")
    heat_pivot = heat_data.pivot(index="Municipio", columns="parasito", values="n").fillna(0).astype(int)
    heat_pivot.columns = [italicize(c) for c in heat_pivot.columns]
    fig3 = px.imshow(
        heat_pivot, text_auto=True, aspect="auto",
        color_continuous_scale="YlOrRd",
        labels=dict(x="Parásito", y="Municipio", color="Detecciones"),
    )
    fig3.update_layout(margin=dict(l=0))
    st.plotly_chart(fig3, width="stretch")

# ============================================================
st.header("Sección B: Prevalencia por Parque Público")
# ============================================================

# 4. Prevalence bar chart by park
prev_park = df_filtered.groupby(["Municipio", "Parque Público"]).agg(
    total=("es_positiva", "count"),
    positivas=("es_positiva", "sum"),
).reset_index()
prev_park["prevalencia"] = (prev_park["positivas"] / prev_park["total"]) * 100
prev_park["label"] = prev_park["Parque Público"] + " (" + prev_park["Municipio"] + ")"
prev_park = prev_park.sort_values("prevalencia", ascending=True)
prev_park["sobre_promedio"] = prev_park["prevalencia"] >= prevalencia_general

fig4 = px.bar(
    prev_park, x="prevalencia", y="label", orientation="h",
    color="sobre_promedio",
    color_discrete_map={True: POSITIVE_COLOR, False: NEGATIVE_COLOR},
    text=prev_park.apply(lambda r: f"{r['prevalencia']:.1f}% (n={r['total']})", axis=1),
    labels={"prevalencia": "Prevalencia (%)", "label": "Parque", "sobre_promedio": "Sobre promedio"},
)
fig4.add_vline(x=prevalencia_general, line_dash="dash", line_color=AVERAGE_LINE_COLOR,
               annotation_text=f"Promedio: {prevalencia_general:.1f}%")
fig4.update_layout(showlegend=False, height=600, margin=dict(l=0))
fig4.update_traces(textposition="outside")
st.plotly_chart(fig4, width="stretch")

# 5 & 6 side by side
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Muestras positivas vs negativas por parque")
    stack_park = df_filtered.groupby(["Parque Público", "es_positiva"]).size().reset_index(name="n")
    stack_park["Resultado"] = stack_park["es_positiva"].map({True: "Positiva", False: "Negativa"})
    fig5 = px.bar(
        stack_park, x="Parque Público", y="n", color="Resultado",
        color_discrete_map={"Positiva": POSITIVE_COLOR, "Negativa": NEGATIVE_COLOR},
        text="n",
    )
    fig5.update_layout(barmode="stack", xaxis_tickangle=-45, margin=dict(b=120), height=500)
    st.plotly_chart(fig5, width="stretch")

with col_d:
    st.subheader("Detecciones por especie y parque")
    heat_park = exploded_filtered.groupby(["Parque Público", "parasito"]).size().reset_index(name="n")
    heat_park_pivot = heat_park.pivot(index="Parque Público", columns="parasito", values="n").fillna(0).astype(int)
    heat_park_pivot.columns = [italicize(c) for c in heat_park_pivot.columns]
    fig6 = px.imshow(
        heat_park_pivot, text_auto=True, aspect="auto",
        color_continuous_scale="YlOrRd",
        labels=dict(x="Parásito", y="Parque", color="Detecciones"),
    )
    fig6.update_layout(margin=dict(l=0), height=500)
    st.plotly_chart(fig6, width="stretch")
