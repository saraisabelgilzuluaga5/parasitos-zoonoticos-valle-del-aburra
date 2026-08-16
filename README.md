# Parásitos Zoonóticos en Parques Públicos del Valle del Aburrá

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://parasitos-zoonoticos-valle-del-aburra-s3rin3ls6mfbwgkmrhesxz.streamlit.app/)

Dashboard interactivo que visualiza la prevalencia de parásitos zoonóticos en heces de perros recolectadas en parques públicos urbanos del Área Metropolitana del Valle del Aburrá (diciembre 2025 - mayo 2026).

## Trabajo de Grado

**Autora:** Sara Isabel Gil Zuluaga  
**Título:** Microbiólogo y Bioanalista  
**Universidad:** Universidad de Antioquia  
**Tutora:** Sara Yepes (MSc en Salud Pública)

## Ejecutar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

```
├── app.py                      # Página principal
├── pages/                      # Páginas del dashboard
├── utils/                      # Módulos de datos y tema
├── coprologicos.csv            # Dataset
├── requirements.txt            # Dependencias
└── .streamlit/config.toml      # Tema visual
```

## Datos

El archivo `coprologicos.csv` contiene los resultados de los exámenes coproparasitológicos de 322 muestras fecales caninas recolectadas en 18 parques públicos de 10 municipios.
