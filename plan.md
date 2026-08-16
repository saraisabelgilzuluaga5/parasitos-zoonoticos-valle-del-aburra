# Plan del Dashboard Interactivo

## Prevalencia de Parásitos Zoonóticos en Heces de Perros en Parques Públicos del Área Metropolitana del Valle del Aburrá (2025-2026)

---

## Contexto

Este dashboard interactivo complementa el trabajo de grado de **Sara Isabel Gil Zuluaga** para optar al título de Microbiólogo y Bioanalista en la Universidad de Antioquia, bajo la tutoría de Sara Yepes (MSc en Salud Pública).

Las visualizaciones se generaron desde cero a partir de los datos más recientes registrados en el archivo `coprologicos.csv`, aplicando el estado del arte en ciencia de datos y visualización con el apoyo de inteligencia artificial.

**Estudio:** Descriptivo transversal. Muestras fecales caninas recolectadas en parques públicos urbanos de los 10 municipios del Área Metropolitana del Valle del Aburrá entre diciembre del 2025 y mayo del 2026.

---

## Objetivos del Estudio (guían la estructura del dashboard)

1. Describir las características macroscópicas de las heces de perros recolectadas.
2. Identificar el género de los parásitos zoonóticos mediante técnicas coproparasitológicas.
3. Establecer la prevalencia de parásitos zoonóticos según parque y municipio de muestreo.
4. Analizar los hallazgos parasitológicos con el riesgo potencial para la salud pública.

---

## Principio de Cálculo Dinámico

Todas las métricas del dashboard se calculan en tiempo real a partir de `coprologicos.csv`. Si el CSV se actualiza con nuevas muestras, el dashboard recalcula automáticamente todos los valores. **Nunca se hardcodean números.**

### Definiciones de cálculo:

| Métrica | Fórmula |
|---------|--------|
| Total muestras | Número de filas válidas en el CSV (excluyendo filas vacías) |
| Muestra positiva | Fila donde "Parásito zoonótico observado" ≠ "No se observan estructuras parasitarias" |
| Prevalencia general | (muestras positivas / total muestras) × 100 |
| Prevalencia por municipio | (positivas del municipio / total del municipio) × 100 |
| Prevalencia por parque | (positivas del parque / total del parque) × 100 |
| Detecciones por especie | Contar cada parásito individualmente (coinfecciones se "explotan" en filas separadas) |
| Poliparasitismo | Muestras cuyo campo "Parásito zoonótico observado" contiene más de un parásito (separados por coma) |
| Positividad por técnica | (muestras con "Positivo" en la columna de la técnica / total muestras) × 100 |

---

## Arquitectura del Proyecto

```
tesis_isa_sarita/
├── app.py                      # Página principal: resumen y KPIs
├── pages/
│   ├── 1_📊_Prevalencia.py     # Obj. 3: Prevalencia por municipio y parque
│   ├── 2_🦠_Parasitos.py      # Obj. 2: Identificación y distribución de especies
│   ├── 3_🔬_Diagnostico.py    # Obj. 2: Rendimiento de técnicas coproparasitológicas
│   └── 4_🧪_Macroscopico.py   # Obj. 1: Características macroscópicas
├── utils/
│   ├── data_loader.py          # Carga, limpieza y transformación del CSV
│   └── theme.py                # Paleta de colores y configuración visual
├── coprologicos.csv            # Dataset completo del estudio
├── requirements.txt            # Dependencias Python
├── .streamlit/
│   └── config.toml             # Tema visual de Streamlit
├── .gitignore
├── README.md
└── plan.md                     # Este archivo
```

---

## Diseño del Dashboard por Página

### Página Principal (`app.py`) - Resumen del Estudio

**Propósito:** Presentar el contexto del estudio y los resultados globales de un vistazo.

**Contenido:**
- Encabezado con título del estudio, autora y universidad.
- Breve descripción de la metodología (estudio descriptivo transversal, muestreo no probabilístico por conveniencia).
- **4 métricas KPI** en fila (calculadas dinámicamente del CSV):
  - Total muestras analizadas
  - Prevalencia general (%)
  - Parásito más frecuente (el de mayor conteo de detecciones)
  - Municipio con mayor prevalencia (el de mayor % calculado)
- **Gráfico de dona:** Proporción general de muestras positivas vs negativas.
- **Tabla resumen:** Distribución de muestras por municipio y parque (reproduciendo Tabla 1 de la tesis).
- Opción de descarga del dataset en CSV.

---

### Página 1: Prevalencia (`1_📊_Prevalencia.py`) - Objetivo Específico 3

**Propósito:** Establecer la prevalencia de parásitos zoonóticos según el parque y municipio de muestreo.

#### Sección A: Prevalencia por Municipio

1. **Gráfico de barras horizontal ordenado:** Prevalencia general (%) por municipio, con línea de referencia del promedio general calculado. Ordenado de mayor a menor. Coloreado según si supera o no el promedio.

2. **Gráfico de barras apiladas:** Muestras positivas vs negativas por municipio (números absolutos), para dar contexto del tamaño muestral.

3. **Heatmap (mapa de calor):** Filas = municipios, columnas = parásitos. Valores = número de detecciones. Permite ver qué parásitos predominan en qué municipios.

#### Sección B: Prevalencia por Parque Público

4. **Gráfico de barras horizontal ordenado:** Prevalencia (%) en cada parque, ordenado de mayor a menor. Con línea de referencia del promedio general calculado. Anotado con n de muestras analizadas por parque.

5. **Gráfico de barras apiladas:** Muestras positivas vs negativas por parque (números absolutos).

6. **Heatmap (mapa de calor):** Filas = parques, columnas = parásitos. Valores = número de detecciones por parque. Permite ver qué parásitos predominan en qué parques.

**Filtros:** Selector de municipio(s), selector de parásito(s).

---

### Página 2: Parásitos Identificados (`2_🦠_Parasitos.py`) - Objetivo Específico 2

**Propósito:** Identificar las especies parasitarias y analizar su distribución.

**Visualizaciones:**

1. **Gráfico de dona:** Distribución proporcional de todas las detecciones por especie (porcentajes calculados del total de detecciones, incluyendo coinfecciones como detecciones individuales).

2. **Gráfico de barras agrupadas:** Frecuencia absoluta de cada parásito por municipio. Cada municipio tiene 4 barras (una por especie).

3. **Tipo de parasitismo:** Gráfico simple mostrando la proporción calculada de parasitismo único vs poliparasitismo (muestras con ≥2 parásitos).

4. **Tabla de coinfecciones:** Detalle de todas las muestras con poliparasitismo (código, municipio, parque, parásitos encontrados). Se filtra dinámicamente.

5. **Tipo de estructura parasitaria:** Gráfico de barras mostrando Huevos vs Quistes como forma diagnóstica encontrada.

**Filtros:** Selector de especie parasitaria, selector de municipio.

---

### Página 3: Técnicas Diagnósticas (`3_🔬_Diagnostico.py`) - Objetivo Específico 2

**Propósito:** Comparar el rendimiento de las tres técnicas coproparasitológicas utilizadas.

**Visualizaciones:**

1. **Gráfico de barras:** Positividad (%) de cada técnica, calculada como (muestras "Positivo" / total muestras) × 100. Con número absoluto de muestras positivas anotado.

2. **Heatmap de concordancia:** Matriz mostrando cuántas muestras fueron positivas en combinaciones de métodos (solo Sheather, solo Salina, Sheather+Salina, los tres, etc.).

3. **Gráfico de barras agrupadas:** Para cada parásito, qué técnica lo detectó con mayor frecuencia. Esto demuestra que Sheather es superior para huevos de helmintos y el examen directo para quistes de protozoos (*Giardia*).

4. **Diagrama UpSet o tabla cruzada:** Visualización clara de la superposición entre métodos diagnósticos para todas las muestras positivas.

**Nota contextual:** La técnica de flotación de Sheather (solución de sacarosa con centrifugación a 2500 rpm por 5 minutos) fue el método principal de diagnóstico. Los exámenes directos con solución salina y lugol complementaron la detección, especialmente para formas móviles (trofozoitos de *Giardia*).

---

### Página 4: Examen Macroscópico (`4_🧪_Macroscopico.py`) - Objetivo Específico 1

**Propósito:** Describir las características macroscópicas y explorar su relación con la positividad parasitaria.

**Visualizaciones:**

1. **Gráfico de barras:** Distribución de consistencia (conteo y % calculados de los valores únicos en la columna Consistencia).

2. **Gráfico de barras:** Distribución de color (conteo y % calculados de los valores únicos en la columna Color).

3. **Presencia de hallazgos macroscópicos:** Gráfico de barras horizontal con el % de "Presente" calculado para cada variable (sangre, moco, alimentos sin digerir).

4. **Relación consistencia vs positividad:** Gráfico de barras agrupadas mostrando el % de positividad parasitaria por tipo de consistencia. (Hipótesis: muestras pastosas y diarreicas tienen mayor positividad que las duras).

5. **Relación moco/alimentos vs positividad:** Gráfico de barras agrupadas comparando la tasa de positividad en muestras con presencia vs ausencia de moco y alimentos sin digerir.

6. **Tabla cruzada:** Características macroscópicas de todas las muestras positivas (filtrado dinámico, para ver si hay patrones).

**Filtros:** Selector de municipio, selector de parásito.

---

## Relevancia para la Salud Pública (Contexto del Dashboard)

Cada página incluirá una sección de contexto breve (expandible con `st.expander`) que conecte los hallazgos con su relevancia en salud pública:

- *A. caninum*: Causa larva migrans cutánea. Riesgo por caminar descalzo en parques contaminados.
- *T. canis*: Causa larva migrans visceral y ocular, especialmente en niños. Huevos viables en suelo por años.
- *G. intestinalis*: Causa giardiasis. Transmisión fecal-oral directa, especialmente relevante en niños que juegan en parques.
- *T. vulpis*: Causa tricuriasis. Huevos altamente resistentes en el ambiente (30-60 días para ser infectantes).

---

## Stack Tecnológico

| Componente | Tecnología | Justificación |
|-----------|-----------|---------------|
| Framework web | Streamlit | Rápido para dashboards de datos, deployment gratuito |
| Visualización | Plotly Express | Gráficas interactivas, hover con detalle, exportables |
| Datos | Pandas | Estándar para análisis de datos tabulares |
| Lenguaje | Python | Última versión instalada |
| Deployment | Streamlit Community Cloud | Gratuito, conecta directo con GitHub |

---

## Dependencias (`requirements.txt`)

```
streamlit>=1.35.0
pandas>=2.0.0
plotly>=5.18.0
```

---

## Configuración del Entorno Local

```bash
# Crear ambiente virtual
python -m venv .venv

# Activar ambiente virtual (macOS/Linux)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dashboard localmente
streamlit run app.py
```

---

## Consideraciones de Implementación

1. **Limpieza de datos (`data_loader.py`):**
   - Normalizar nombres de columnas (eliminar espacios extra, tildes inconsistentes).
   - Manejar valores entre comillas para coinfecciones (e.g., `"Ancylostoma caninum, Toxocara Canis"`).
   - Estandarizar texto: "Medelín" → "Medellín", "Itagui" → "Itagüí".
   - Eliminar fila vacía al final del CSV.
   - Crear columna booleana `es_positiva` para facilitar cálculos de prevalencia.
   - Crear columna `parasitos_lista` (lista de parásitos por muestra para manejar coinfecciones).

2. **Cálculo de prevalencia:**
   - Prevalencia = (muestras positivas / total muestras) × 100.
   - Una muestra es positiva si el campo "Parásito zoonótico observado" contiene un nombre de parásito (no "No se observan estructuras parasitarias").
   - Para frecuencia por especie: contar cada parásito individualmente (las 4 coinfecciones cuentan doble).

3. **Paleta de colores (`theme.py`):**
   - Paleta consistente para los 4 parásitos a lo largo de todas las páginas.
   - Colores accesibles (color-blind friendly).
   - Colores semánticos: verde/rojo para positivo/negativo.

4. **Idioma:** Todo en español (labels, títulos, tooltips, legendas).

5. **Performance:** El dataset es pequeño, no se requieren optimizaciones. Se usará `@st.cache_data` para evitar recargar el CSV en cada interacción.

6. **Reproducibilidad:** Todos los valores se computan dinámicamente del CSV. Si el CSV se actualiza, el dashboard recalcula todo. No se hardcodean números en el código.

---

## Deployment en Streamlit Community Cloud

1. Crear repositorio en GitHub (manual, cuenta personal de Sara).
2. Subir código, CSV y archivos de configuración.
3. Conectar el repositorio desde [share.streamlit.io](https://share.streamlit.io).
4. Configurar `app.py` como archivo principal.
5. La app quedará disponible con URL pública para incluir en el documento de grado.

---

## Orden de Implementación

| Paso | Archivo | Descripción |
|------|---------|-------------|
| 1 | `utils/data_loader.py` | Carga y limpieza del CSV |
| 2 | `utils/theme.py` | Paleta de colores y constantes visuales |
| 3 | `app.py` | Página principal con KPIs y resumen |
| 4 | `pages/1_📊_Prevalencia.py` | Prevalencia por municipio y parque |
| 5 | `pages/2_🦠_Parasitos.py` | Distribución de especies parasitarias |
| 6 | `pages/3_🔬_Diagnostico.py` | Comparación de técnicas diagnósticas |
| 7 | `pages/4_🧪_Macroscopico.py` | Examen macroscópico y correlaciones |
| 8 | `.streamlit/config.toml` | Tema visual |
| 9 | `requirements.txt`, `.gitignore`, `README.md` | Configuración del proyecto |
| 10 | Verificación | Validar que los números coincidan con la tesis |
