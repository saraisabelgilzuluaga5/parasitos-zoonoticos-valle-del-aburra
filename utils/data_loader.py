import pandas as pd
import streamlit as st
from pathlib import Path

NEGATIVE_LABEL = "No se observan estructuras parasitarias"

# Standardize municipality names
MUNICIPIO_MAP = {
    "Medelín": "Medellín",
    "Itagui": "Itagüí",
    "La estrella": "La Estrella",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    csv_path = Path(__file__).parent.parent / "coprologicos.csv"
    df = pd.read_csv(csv_path, encoding="utf-8")

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Drop completely empty rows
    df = df.dropna(subset=["Código de la muestra"]).reset_index(drop=True)
    # Drop rows where Código is just punctuation/empty
    df = df[df["Código de la muestra"].str.strip().str.len() > 1].reset_index(drop=True)

    # Strip whitespace from string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Standardize municipality names
    df["Municipio"] = df["Municipio"].replace(MUNICIPIO_MAP)

    # Standardize park names
    df["Parque Público"] = df["Parque Público"].str.strip()

    # Determine if sample is positive
    df["es_positiva"] = df["Parásito zoonótico observado"] != NEGATIVE_LABEL

    # Parse parasites list (handle coinfections separated by comma inside quotes)
    df["parasitos_lista"] = df["Parásito zoonótico observado"].apply(_parse_parasites)

    # Standardize parasite names for consistency
    df["parasitos_lista"] = df["parasitos_lista"].apply(
        lambda lst: [_standardize_parasite(p) for p in lst]
    )

    # Standardize diagnostic columns
    for col in ["Hallazgos Examen Directo (Solución Salina)", "Hallazgos Examen Directo (Lugol)", "Halazgos Flotación de Sheather"]:
        if col in df.columns:
            df[col] = df[col].str.strip()

    return df


def _parse_parasites(value: str) -> list[str]:
    if pd.isna(value) or value == NEGATIVE_LABEL:
        return []
    return [p.strip() for p in value.split(",") if p.strip() and p.strip() != NEGATIVE_LABEL]


def _standardize_parasite(name: str) -> str:
    mapping = {
        "Toxocara Canis": "Toxocara canis",
        "Toxocara canis": "Toxocara canis",
        "Ancylostoma caninum": "Ancylostoma caninum",
        "Giardia intestinalis": "Giardia intestinalis",
        "Trichuris vulpis": "Trichuris vulpis",
    }
    return mapping.get(name, name)


def get_exploded_parasites(df: pd.DataFrame) -> pd.DataFrame:
    """Explode parasitos_lista so each detection is a separate row."""
    positives = df[df["es_positiva"]].copy()
    return positives.explode("parasitos_lista").rename(columns={"parasitos_lista": "parasito"})
