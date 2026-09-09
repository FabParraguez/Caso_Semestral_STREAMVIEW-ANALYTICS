from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Gerencia de Contenidos - StreamView Analytics",
    page_icon="🎬",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --sv-ink: #e8eef2;
        --sv-muted: #9eabb4;
        --sv-panel: #151c22;
        --sv-panel-soft: #1b252d;
        --sv-line: rgba(160, 181, 194, 0.18);
        --sv-accent: #55c2b4;
        --sv-accent-soft: rgba(85, 194, 180, 0.12);
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #0c1115;
        color: var(--sv-ink);
    }

    .main .block-container {
        max-width: 1480px;
        padding: 2.2rem 3.2rem 3rem;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0;
    }

    h1 {
        font-size: 2.15rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.15rem !important;
    }

    h2 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
    }

    h3 {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    .stApp > header {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #11181e;
        border-right: 1px solid var(--sv-line);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        color: var(--sv-ink);
    }

    [data-testid="stSidebar"] .stButton > button {
        background: var(--sv-accent-soft);
        border: 1px solid rgba(85, 194, 180, 0.45);
        color: #baf1e9;
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(85, 194, 180, 0.2);
        border-color: var(--sv-accent);
        color: #e8fffa;
    }

    [data-testid="stMetric"] {
        background: var(--sv-panel);
        border: 1px solid var(--sv-line);
        border-top: 3px solid var(--sv-accent);
        border-radius: 8px;
        padding: 0.85rem 1rem 0.8rem;
        min-height: 110px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--sv-muted);
        font-size: 0.78rem;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: var(--sv-ink);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.65rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--sv-line);
    }

    .stCaption {
        color: var(--sv-muted);
        font-size: 0.95rem;
    }

    hr {
        border-color: var(--sv-line);
        margin: 1.7rem 0;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--sv-line);
        border-radius: 8px;
        overflow: hidden;
    }

    .recommendation-card {
        background: var(--sv-panel);
        border: 1px solid var(--sv-line);
        border-left: 3px solid var(--sv-accent);
        border-radius: 8px;
        min-height: 145px;
        padding: 1rem 1.1rem;
        color: var(--sv-ink);
        line-height: 1.5;
    }

    .recommendation-card b {
        color: #baf1e9;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.98rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "Dataset_Utilizado"


@st.cache_data
def load_data():
    peliculas = pd.read_csv(DATA_DIR / "peliculas_clean.csv")
    series = pd.read_csv(DATA_DIR / "series_clean.csv")

    peliculas = peliculas.copy()
    series = series.copy()

    for df in [peliculas, series]:
        if "anio_estreno" in df.columns:
            df["anio_estreno"] = pd.to_numeric(df["anio_estreno"], errors="coerce")
        if "tipo" not in df.columns:
            df["tipo"] = "Pelicula" if "presupuesto" in df.columns else "Serie"

    peliculas["tipo"] = "Pelicula"
    series["tipo"] = "Serie"

    if "roi" not in peliculas.columns:
        presupuesto = pd.to_numeric(peliculas["presupuesto"], errors="coerce")
        ingresos = pd.to_numeric(peliculas["ingresos"], errors="coerce")
        peliculas["roi"] = pd.NA
        valido_para_roi = (presupuesto > 0) & (ingresos > 0)
        peliculas.loc[valido_para_roi, "roi"] = (
            ingresos[valido_para_roi] - presupuesto[valido_para_roi]
        ) / presupuesto[valido_para_roi]

    series["roi"] = pd.NA
    series["presupuesto"] = pd.NA
    series["ingresos"] = pd.NA

    common_cols = [
        "id_muestra",
        "tipo",
        "titulo",
        "anio_estreno",
        "pais_principal",
        "genero_principal",
        "idioma",
        "duracion",
        "popularidad",
        "votos",
        "promedio_votos",
        "roi",
        "presupuesto",
        "ingresos",
    ]

    catalogo = pd.concat(
        [peliculas[common_cols], series[common_cols]],
        ignore_index=True,
    )

    return catalogo, peliculas, series


catalogo, peliculas, series = load_data()


catalogo = catalogo.dropna(subset=["id_muestra"]).copy()
catalogo["pais_principal"] = catalogo["pais_principal"].fillna("Sin informacion")
catalogo["genero_principal"] = catalogo["genero_principal"].fillna("Sin informacion")
catalogo["idioma"] = catalogo["idioma"].fillna("Sin informacion")

LANGUAGE_LABELS = {
    "af": "Afrikáans",
    "am": "Amhárico",
    "as": "Asamés",
    "az": "Azerí",
    "bg": "Búlgaro",
    "bs": "Bosnio",
    "cn": "Chino (código de fuente)",
    "cy": "Galés",
    "da": "Danés",
    "dz": "Dzongkha",
    "et": "Estonio",
    "eu": "Euskera",
    "ga": "Irlandés",
    "gl": "Gallego",
    "ht": "Criollo haitiano",
    "hy": "Armenio",
    "is": "Islandés",
    "ka": "Georgiano",
    "kk": "Kazajo",
    "kl": "Groenlandés",
    "km": "Jemer",
    "kn": "Canarés",
    "ku": "Kurdo",
    "ky": "Kirguís",
    "la": "Latín",
    "lb": "Luxemburgués",
    "lt": "Lituano",
    "lv": "Letón",
    "mi": "Maorí",
    "mk": "Macedonio",
    "mn": "Mongol",
    "ms": "Malayo",
    "mt": "Maltés",
    "nb": "Noruego bokmål",
    "ne": "Nepalí",
    "or": "Odia",
    "pa": "Panyabí",
    "ps": "Pastún",
    "si": "Cingalés",
    "sk": "Eslovaco",
    "tl": "Tagalo",
    "ur": "Urdu",
    "vi": "Vietnamita",
    "xx": "Idioma no identificado",
    "yo": "Yoruba",
    "za": "Zulú",
    "zu": "Zulú",
}

LANGUAGE_CODES = {
    "Ingles": "en",
    "Frances": "fr",
    "Japones": "ja",
    "Coreano": "ko",
    "Espanol": "es",
    "Chino": "zh",
    "Italiano": "it",
    "Hindi": "hi",
    "Aleman": "de",
    "Ruso": "ru",
    "Portugues": "pt",
    "Danes": "da",
    "Polaco": "pl",
    "Turco": "tr",
    "Holandes": "nl",
    "Indonesio": "id",
    "Noruego": "no",
    "Sueco": "sv",
    "Tamil": "ta",
    "Tailandes": "th",
    "Telugu": "te",
    "Finlandes": "fi",
    "Malayalam": "ml",
    "Arabigo": "ar",
    "Persa": "fa",
    "Hungaro": "hu",
    "Hebreo": "he",
    "Checo": "cs",
    "Catalan": "ca",
    "Ucraniano": "uk",
    "Bangla": "bn",
    "Serbio": "sr",
    "Rumano": "ro",
    "Griego": "el",
    "Croata": "hr",
    "Marathi": "mr",
    "Esloveno": "sl",
}


def language_label(value):
    value = str(value)
    if value in LANGUAGE_LABELS:
        return f"{value} - {LANGUAGE_LABELS[value]}"
    if value in LANGUAGE_CODES:
        return f"{LANGUAGE_CODES[value]} - {value}"
    return f"-- - {value}"


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if tipo_sel:
        out = out[out["tipo"].isin(tipo_sel)]
    out = out[(out["anio_estreno"] >= anio_sel[0]) & (out["anio_estreno"] <= anio_sel[1])]
    if pais_sel:
        out = out[out["pais_principal"].isin(pais_sel)]
    if genero_sel:
        out = out[out["genero_principal"].isin(genero_sel)]
    if idioma_sel:
        out = out[out["idioma"].isin(idioma_sel)]
    return out


st.title("Gerencia de Contenidos")
st.caption("StreamView Analytics  /  Panel de decisión para adquisición, producción y promoción")

st.sidebar.header("Filtros de contenido")

tipos_disponibles = sorted(catalogo["tipo"].dropna().unique().tolist())
min_year = int(catalogo["anio_estreno"].min())
max_year = int(catalogo["anio_estreno"].max())
paises = sorted(catalogo["pais_principal"].dropna().astype(str).unique().tolist())
generos = sorted(catalogo["genero_principal"].dropna().astype(str).unique().tolist())
idiomas = sorted(catalogo["idioma"].dropna().astype(str).unique().tolist())

st.session_state.setdefault("tipo_filter", tipos_disponibles)
st.session_state.setdefault("anio_filter", (min_year, max_year))
st.session_state.setdefault("pais_filter", [])
st.session_state.setdefault("genero_filter", [])
st.session_state.setdefault("idioma_filter", [])

if st.sidebar.button("Restablecer filtros", use_container_width=True):
    st.session_state["tipo_filter"] = tipos_disponibles
    st.session_state["anio_filter"] = (min_year, max_year)
    st.session_state["pais_filter"] = []
    st.session_state["genero_filter"] = []
    st.session_state["idioma_filter"] = []
    st.rerun()

tipo_sel = st.sidebar.multiselect(
    "Tipo", options=tipos_disponibles, key="tipo_filter"
)
anio_sel = st.sidebar.slider(
    "Año de estreno",
    min_value=min_year,
    max_value=max_year,
    key="anio_filter",
)
pais_sel = st.sidebar.multiselect("País principal", options=paises, key="pais_filter")
genero_sel = st.sidebar.multiselect("Género principal", options=generos, key="genero_filter")
idioma_sel = st.sidebar.multiselect(
    "Idioma",
    options=idiomas,
    format_func=language_label,
    key="idioma_filter",
)

catalogo_f = apply_filters(catalogo)

if catalogo_f.empty:
    st.warning("No hay datos para la combinación actual de filtros. Ajusta los criterios.")
    st.stop()

catalogo_unique = catalogo_f.drop_duplicates(subset=["tipo", "id_muestra"]).copy()

genero_ejecutivo = (
    catalogo_unique.groupby("genero_principal", as_index=False)
    .agg(
        popularidad_promedio=("popularidad", "mean"),
        titulos=("id_muestra", "nunique"),
    )
)
genero_ejecutivo_elegible = genero_ejecutivo[
    genero_ejecutivo["titulos"] >= min(20, len(catalogo_unique))
]
if genero_ejecutivo_elegible.empty:
    genero_ejecutivo_elegible = genero_ejecutivo
genero_destacado = genero_ejecutivo_elegible.sort_values(
    ["popularidad_promedio", "titulos"], ascending=False
).iloc[0]

roi_mediano_ejecutivo = pd.to_numeric(
    catalogo_unique.loc[catalogo_unique["tipo"] == "Pelicula", "roi"],
    errors="coerce",
).median()

st.subheader("Resumen ejecutivo")
ejecutivo1, ejecutivo2, ejecutivo3 = st.columns(3)
ejecutivo1.metric("Catálogo analizado", f"{catalogo_unique['id_muestra'].nunique():,} títulos")
ejecutivo2.metric(
    "Género con mayor popularidad promedio",
    str(genero_destacado["genero_principal"]),
    f"Popularidad {genero_destacado['popularidad_promedio']:.2f}",
)
ejecutivo3.metric(
    "ROI mediano de películas",
    f"{roi_mediano_ejecutivo:.2%}" if pd.notna(roi_mediano_ejecutivo) else "N/D",
    "Series: sin datos financieros",
)
st.caption(
    "Lectura rápida para adquisición y promoción. Las señales respetan los filtros seleccionados."
)

st.subheader("KPI principal")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total títulos", f"{catalogo_unique['id_muestra'].nunique():,}")
col2.metric("Películas", f"{catalogo_unique[catalogo_unique['tipo']=='Pelicula']['id_muestra'].nunique():,}")
col3.metric("Series", f"{catalogo_unique[catalogo_unique['tipo']=='Serie']['id_muestra'].nunique():,}")
col4.metric("Popularidad promedio", f"{catalogo_unique['popularidad'].mean():.2f}")
col5.metric("Rating promedio", f"{catalogo_unique['promedio_votos'].mean():.2f}")
col6.metric("Votos totales", f"{int(catalogo_unique['votos'].sum()):,}")

st.markdown("---")

financieros = catalogo_unique[catalogo_unique["tipo"] == "Pelicula"].copy()
financieros["presupuesto"] = pd.to_numeric(financieros["presupuesto"], errors="coerce")
financieros["ingresos"] = pd.to_numeric(financieros["ingresos"], errors="coerce")
financieros_validos = financieros[
    (financieros["presupuesto"] > 0) & (financieros["ingresos"] > 0)
]
presupuesto_total = financieros_validos["presupuesto"].sum()
ingresos_total = financieros_validos["ingresos"].sum()
roi_global = (
    (ingresos_total - presupuesto_total) / presupuesto_total
    if presupuesto_total > 0
    else None
)

st.subheader("KPI financieros")
fin_col1, fin_col2, fin_col3, fin_col4 = st.columns(4)
fin_col1.metric("Presupuesto total", f"{presupuesto_total:,.0f}")
fin_col2.metric("Ingresos totales", f"{ingresos_total:,.0f}")
fin_col3.metric(
    "ROI global ponderado",
    f"{roi_global:.2%}" if roi_global is not None else "N/D",
)
fin_col4.metric("Películas con datos válidos", f"{len(financieros_validos):,}")
st.caption(
    "Calculado únicamente con películas que tienen presupuesto e ingresos mayores que cero; "
    "las series no contienen variables financieras."
)
with st.expander("Ver películas incluidas en los KPI financieros"):
    detalle_financiero = financieros_validos[
        ["titulo", "anio_estreno", "presupuesto", "ingresos", "roi"]
    ].copy()
    detalle_financiero = detalle_financiero.rename(
        columns={
            "titulo": "Película",
            "anio_estreno": "Año",
            "presupuesto": "Presupuesto",
            "ingresos": "Ingresos",
            "roi": "ROI",
        }
    ).sort_values("Película")
    detalle_financiero["ROI"] = detalle_financiero["ROI"].map(
        lambda value: f"{value:.2%}"
    )
    st.dataframe(detalle_financiero, hide_index=True, use_container_width=True, height=360)

colA, colB = st.columns(2)

with colA:
    trend = (
        catalogo_unique.groupby(["anio_estreno", "tipo"], as_index=False)["id_muestra"]
        .nunique()
        .rename(columns={"id_muestra": "titulos"})
        .sort_values("anio_estreno")
    )
    fig_trend = px.line(
        trend,
        x="anio_estreno",
        y="titulos",
        color="tipo",
        markers=True,
        text="titulos",
        title="Evolución del catálogo por año de estreno",
    )
    fig_trend.update_traces(texttemplate="%{text:,.0f}", textposition="top center")
    fig_trend.update_layout(xaxis_title="Año", yaxis_title="Cantidad de títulos", hovermode="x unified")
    st.plotly_chart(fig_trend, config={"displayModeBar": False}, use_container_width=True)

with colB:
    top_genres = (
        catalogo_unique.drop_duplicates(subset=["tipo", "id_muestra", "genero_principal"])
        .groupby("genero_principal", as_index=False)
        .size()
        .rename(columns={"size": "titulos", "genero_principal": "genero"})
        .sort_values("titulos", ascending=False)
        .head(10)
    )
    fig_genres = px.bar(
        top_genres.sort_values("titulos", ascending=True),
        x="titulos",
        y="genero",
        orientation="h",
        title="Top géneros por volumen de contenido",
        color="titulos",
        color_continuous_scale="Blues",
        text="titulos",
    )
    fig_genres.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    st.plotly_chart(fig_genres, config={"displayModeBar": False}, use_container_width=True)

colC, colD = st.columns(2)

with colC:
    top_countries = (
        catalogo_unique.groupby("pais_principal", as_index=False)
        .agg(
            popularidad_promedio=("popularidad", "mean"),
            rating_promedio=("promedio_votos", "mean"),
            titulos=("id_muestra", "nunique"),
        )
        .query("titulos >= 20")
        .sort_values("popularidad_promedio", ascending=False)
        .head(10)
    )
    fig_countries = px.bar(
        top_countries.sort_values("popularidad_promedio", ascending=True),
        x="popularidad_promedio",
        y="pais_principal",
        orientation="h",
        title="Popularidad promedio por país productor",
        color="popularidad_promedio",
        color_continuous_scale="Teal",
        hover_data=["rating_promedio", "titulos"],
        text="popularidad_promedio",
    )
    fig_countries.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_countries.update_layout(
        xaxis_title="Popularidad promedio",
        yaxis_title="País productor",
        coloraxis_colorbar_title="Popularidad",
    )
    st.plotly_chart(fig_countries, config={"displayModeBar": False}, use_container_width=True)

with colD:
    impacto_genero = (
        catalogo_unique.groupby("genero_principal", as_index=False)
        .agg(
            popularidad_promedio=("popularidad", "mean"),
            rating_promedio=("promedio_votos", "mean"),
            titulos=("id_muestra", "nunique"),
        )
        .sort_values("popularidad_promedio", ascending=False)
        .head(10)
    )

    fig_impacto_genero = px.bar(
        impacto_genero.sort_values("popularidad_promedio", ascending=True),
        x="popularidad_promedio",
        y="genero_principal",
        orientation="h",
        title="Popularidad promedio por género",
        color="popularidad_promedio",
        color_continuous_scale="Blues",
        hover_data=["rating_promedio", "titulos"],
        text="popularidad_promedio",
    )
    fig_impacto_genero.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_impacto_genero.update_layout(
        xaxis_title="Popularidad promedio",
        yaxis_title="Género",
        showlegend=False,
    )
    st.plotly_chart(fig_impacto_genero, config={"displayModeBar": False}, use_container_width=True)

st.subheader("Duración y atractivo de audiencia")
duracion_catalogo = catalogo_unique.copy()
duracion_catalogo["duracion_valor"] = pd.to_numeric(
    duracion_catalogo["duracion"].astype("string").str.extract(r"(\d+(?:[.,]\d+)?)")[0].str.replace(",", "."),
    errors="coerce",
)
duracion_disponible = duracion_catalogo["duracion_valor"].notna()

if duracion_disponible.sum() == 0 or duracion_catalogo.loc[duracion_disponible, "duracion_valor"].nunique() <= 1:
    st.info(
        "El análisis de duración no está disponible con la fuente actual: "
        "películas no tienen valores de duración y las series repiten '1 Temporadas'."
    )
else:
    duracion_catalogo = duracion_catalogo[duracion_disponible].copy()
    duracion_catalogo["rango_duracion"] = pd.cut(
        duracion_catalogo["duracion_valor"],
        bins=[0, 30, 60, 90, 120, float("inf")],
        labels=["Hasta 30", "31-60", "61-90", "91-120", "Más de 120"],
    )
    atractivo_duracion = (
        duracion_catalogo.groupby("rango_duracion", observed=False, as_index=False)
        .agg(
            popularidad_promedio=("popularidad", "mean"),
            rating_promedio=("promedio_votos", "mean"),
            titulos=("id_muestra", "nunique"),
        )
        .dropna(subset=["popularidad_promedio"])
    )
    fig_duracion = px.bar(
        atractivo_duracion,
        x="rango_duracion",
        y="popularidad_promedio",
        title="Popularidad promedio por rango de duración",
        text="popularidad_promedio",
        hover_data=["rating_promedio", "titulos"],
    )
    fig_duracion.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig_duracion, config={"displayModeBar": False}, use_container_width=True)

min_titulos_recomendacion = 20

generos_recomendables = (
    catalogo_unique.groupby("genero_principal", as_index=False)
    .agg(
        popularidad_promedio=("popularidad", "mean"),
        rating_promedio=("promedio_votos", "mean"),
        titulos=("id_muestra", "size"),
    )
)
generos_recomendables = generos_recomendables[
    generos_recomendables["titulos"] >= min_titulos_recomendacion
]
if generos_recomendables.empty:
    generos_recomendables = (
        catalogo_unique.groupby("genero_principal", as_index=False)
        .agg(
            popularidad_promedio=("popularidad", "mean"),
            rating_promedio=("promedio_votos", "mean"),
            titulos=("id_muestra", "size"),
        )
    )
genero_recomendado = (
    generos_recomendables
    .sort_values(["popularidad_promedio", "titulos"], ascending=False)
    .iloc[0]
)

paises_recomendables = (
    catalogo_unique.drop_duplicates(subset=["tipo", "id_muestra", "pais_principal"])
    .groupby("pais_principal", as_index=False)
    .agg(
        popularidad_promedio=("popularidad", "mean"),
        titulos=("id_muestra", "size"),
    )
)
paises_recomendables = paises_recomendables[
    paises_recomendables["titulos"] >= min_titulos_recomendacion
]
if paises_recomendables.empty:
    paises_recomendables = (
        catalogo_unique.drop_duplicates(subset=["tipo", "id_muestra", "pais_principal"])
        .groupby("pais_principal", as_index=False)
        .agg(
            popularidad_promedio=("popularidad", "mean"),
            titulos=("id_muestra", "size"),
        )
    )
pais_recomendado = (
    paises_recomendables
    .sort_values(["popularidad_promedio", "titulos"], ascending=False)
    .iloc[0]
)

titulos_recomendados = (
    catalogo_unique.sort_values(["popularidad", "promedio_votos"], ascending=False)
    .head(3)["titulo"]
    .astype(str)
    .tolist()
)
titulos_texto = ", ".join(titulos_recomendados)

st.subheader("Recomendaciones de negocio")
rec1, rec2, rec3 = st.columns(3)

with rec1:
    st.markdown(
        f"""
        <div class='recommendation-card'>
        <b>1. Priorizar adquisiciones</b><br>
        Evaluar nuevas adquisiciones en <b>{genero_recomendado['genero_principal']}</b>, que presenta la mayor popularidad promedio entre los géneros con evidencia suficiente ({genero_recomendado['popularidad_promedio']:.2f}; {int(genero_recomendado['titulos']):,} títulos).
        </div>
        """,
        unsafe_allow_html=True,
    )

with rec2:
    st.markdown(
        f"""
        <div class='recommendation-card'>
        <b>2. Producir con foco</b><br>
        Considerar <b>{pais_recomendado['pais_principal']}</b> como mercado atractivo por popularidad promedio ({pais_recomendado['popularidad_promedio']:.2f}) y evidencia suficiente ({int(pais_recomendado['titulos']):,} títulos); no es una recomendación por volumen.
        </div>
        """,
        unsafe_allow_html=True,
    )

with rec3:
    st.markdown(
        f"""
        <div class='recommendation-card'>
        <b>3. Promocionar con criterio</b><br>
        Priorizar campañas para <b>{titulos_texto}</b>, los títulos con mayor popularidad dentro de la selección actual.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Top títulos por impacto | mayor a menor")
impact_table = catalogo_unique.sort_values(["popularidad", "promedio_votos"], ascending=False).head(12)[
    ["titulo", "tipo", "pais_principal", "genero_principal", "popularidad", "promedio_votos", "votos"]
].reset_index(drop=True)
impact_table.insert(0, "Posición", range(1, len(impact_table) + 1))

st.dataframe(impact_table, width="stretch", hide_index=True)
