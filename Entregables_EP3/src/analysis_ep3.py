"""
Analysis module for EP3 - Enhanced analysis with visualization improvements.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


def resolve_data_dir() -> Path:
    """Busca carpeta de datos priorizando Entregables_EP2/outputs."""
    file_path = Path(__file__).resolve()
    for parent in file_path.parents:
        candidate_ep2 = parent / "outputs"
        if candidate_ep2.exists() and candidate_ep2.is_dir():
            return candidate_ep2

        candidate = parent / "Dataset_Utilizado"
        if candidate.exists() and candidate.is_dir():
            return candidate
            
        candidate_ep2_parent = parent / "Entregables_EP2" / "outputs"
        if candidate_ep2_parent.exists() and candidate_ep2_parent.is_dir():
            return candidate_ep2_parent
    
    raise FileNotFoundError(
        "No se encontró ni 'outputs' de Entregables_EP2 ni 'Dataset_Utilizado'. "
        "Verifica la estructura del repositorio."
    )


def _to_numeric_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_catalog() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carga películas y series en una tabla consolidada de catálogo."""
    data_dir = resolve_data_dir()

    peliculas = pd.read_csv(data_dir / "peliculas_clean.csv")
    series = pd.read_csv(data_dir / "series_clean.csv")

    peliculas = _to_numeric_columns(
        peliculas,
        ["anio_estreno", "popularidad", "votos", "promedio_votos", "presupuesto", "ingresos", "roi"],
    )
    series = _to_numeric_columns(
        series,
        ["anio_estreno", "popularidad", "votos", "promedio_votos"],
    )

    peliculas["tipo"] = "Película"
    series["tipo"] = "Serie"

    if "presupuesto" not in series.columns:
        series["presupuesto"] = np.nan
    if "ingresos" not in series.columns:
        series["ingresos"] = np.nan
    if "roi" not in series.columns:
        series["roi"] = np.nan

    common = [
        "id_muestra",
        "tipo",
        "titulo",
        "anio_estreno",
        "pais_principal",
        "genero_principal",
        "idioma",
        "popularidad",
        "votos",
        "promedio_votos",
        "presupuesto",
        "ingresos",
        "roi",
    ]

    peliculas = peliculas.copy()
    series = series.copy()

    for df in (peliculas, series):
        for col in common:
            if col not in df.columns:
                df[col] = np.nan

        df["pais_principal"] = df["pais_principal"].fillna("Sin información")
        df["genero_principal"] = df["genero_principal"].fillna("Sin información")
        df["idioma"] = df["idioma"].fillna("Sin información")

    catalogo = pd.concat([peliculas[common], series[common]], ignore_index=True)
    catalogo = catalogo.drop_duplicates(subset=["id_muestra"]).copy()

    return catalogo, peliculas, series


def apply_filters(
    df: pd.DataFrame,
    tipo: list[str],
    anio_min: int,
    anio_max: int,
    paises: list[str],
    generos: list[str],
    idiomas: list[str],
) -> pd.DataFrame:
    """Aplica filtros globales al dataframe."""
    result = df[df["tipo"].isin(tipo)].copy()
    result = result[(result["anio_estreno"] >= anio_min) & (result["anio_estreno"] <= anio_max)]

    if paises:
        result = result[result["pais_principal"].isin(paises)]
    if generos:
        result = result[result["genero_principal"].isin(generos)]
    if idiomas:
        result = result[result["idioma"].isin(idiomas)]

    return result


def compute_kpis(catalogo: pd.DataFrame, peliculas: pd.DataFrame) -> Dict[str, float]:
    """Calcula KPIs clave para dashboard ejecutivo."""
    titulos = catalogo["id_muestra"].nunique()
    peliculas_count = (catalogo["tipo"] == "Película").sum()
    series_count = (catalogo["tipo"] == "Serie").sum()
    
    popularidad_media = catalogo["popularidad"].mean()
    rating_medio = catalogo["promedio_votos"].mean()
    votos_totales = catalogo["votos"].sum()

    peliculas_fin = peliculas[(peliculas["presupuesto"] > 0) & (peliculas["ingresos"] > 0)]
    roi_promedio = peliculas_fin["roi"].mean() if not peliculas_fin.empty else np.nan

    return {
        "titulos": titulos,
        "peliculas": peliculas_count,
        "series": series_count,
        "popularidad_media": popularidad_media,
        "rating_medio": rating_medio,
        "votos_totales": votos_totales,
        "roi_promedio": roi_promedio,
    }


def compute_market_insights(catalogo: pd.DataFrame) -> Dict[str, any]:
    """Calcula insights de mercado adicionales para EP3."""
    total_titles = catalogo["id_muestra"].nunique()
    unique_countries = catalogo["pais_principal"].nunique()
    unique_genres = catalogo["genero_principal"].nunique()
    unique_languages = catalogo["idioma"].nunique()
    
    # Concentración de géneros
    top_5_genres = catalogo.groupby("genero_principal")["id_muestra"].nunique().nlargest(5).sum()
    genre_concentration = (top_5_genres / total_titles) * 100 if total_titles > 0 else 0
    
    # Concentración de países
    top_5_countries = catalogo.groupby("pais_principal")["id_muestra"].nunique().nlargest(5).sum()
    country_concentration = (top_5_countries / total_titles) * 100 if total_titles > 0 else 0
    
    # Contenido reciente vs antiguo
    recent_titles = (catalogo["anio_estreno"] >= catalogo["anio_estreno"].quantile(0.75)).sum()
    old_titles = (catalogo["anio_estreno"] <= catalogo["anio_estreno"].quantile(0.25)).sum()
    
    return {
        "total_titles": total_titles,
        "unique_countries": unique_countries,
        "unique_genres": unique_genres,
        "unique_languages": unique_languages,
        "genre_concentration": genre_concentration,
        "country_concentration": country_concentration,
        "recent_titles_ratio": (recent_titles / total_titles * 100) if total_titles > 0 else 0,
        "old_titles_ratio": (old_titles / total_titles * 100) if total_titles > 0 else 0,
    }


def compute_quality_metrics(catalogo: pd.DataFrame) -> Dict[str, float]:
    """Calcula métricas de calidad del contenido."""
    high_quality = (catalogo["promedio_votos"] >= 7.0).sum()
    medium_quality = ((catalogo["promedio_votos"] >= 5.0) & (catalogo["promedio_votos"] < 7.0)).sum()
    low_quality = (catalogo["promedio_votos"] < 5.0).sum()
    
    total = catalogo["id_muestra"].nunique()
    
    return {
        "high_quality_count": high_quality,
        "medium_quality_count": medium_quality,
        "low_quality_count": low_quality,
        "high_quality_pct": (high_quality / total * 100) if total > 0 else 0,
        "medium_quality_pct": (medium_quality / total * 100) if total > 0 else 0,
        "low_quality_pct": (low_quality / total * 100) if total > 0 else 0,
    }
