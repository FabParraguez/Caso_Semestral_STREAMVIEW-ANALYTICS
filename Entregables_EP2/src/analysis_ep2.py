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

    peliculas["tipo"] = "Pelicula"
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

        df["pais_principal"] = df["pais_principal"].fillna("Sin informacion")
        df["genero_principal"] = df["genero_principal"].fillna("Sin informacion")
        df["idioma"] = df["idioma"].fillna("Sin informacion")

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
    out = df.copy()
    out = out[out["tipo"].isin(tipo)]
    out = out[(out["anio_estreno"] >= anio_min) & (out["anio_estreno"] <= anio_max)]
    if paises:
        out = out[out["pais_principal"].isin(paises)]
    if generos:
        out = out[out["genero_principal"].isin(generos)]
    if idiomas:
        out = out[out["idioma"].isin(idiomas)]
    return out


def compute_kpis(catalogo_filtrado: pd.DataFrame, peliculas_filtradas: pd.DataFrame) -> Dict[str, float]:
    titulos = int(catalogo_filtrado["id_muestra"].nunique())
    peliculas = int(catalogo_filtrado[catalogo_filtrado["tipo"] == "Pelicula"]["id_muestra"].nunique())
    series = int(catalogo_filtrado[catalogo_filtrado["tipo"] == "Serie"]["id_muestra"].nunique())

    popularidad_media = float(catalogo_filtrado["popularidad"].mean()) if not catalogo_filtrado.empty else 0.0
    rating_medio = float(catalogo_filtrado["promedio_votos"].mean()) if not catalogo_filtrado.empty else 0.0
    votos_totales = int(catalogo_filtrado["votos"].sum()) if not catalogo_filtrado.empty else 0

    peliculas_fin = peliculas_filtradas[(peliculas_filtradas["presupuesto"] > 0) & (peliculas_filtradas["ingresos"] > 0)].copy()
    roi_promedio = float(peliculas_fin["roi"].mean()) if not peliculas_fin.empty else np.nan

    return {
        "titulos": titulos,
        "peliculas": peliculas,
        "series": series,
        "popularidad_media": popularidad_media,
        "rating_medio": rating_medio,
        "votos_totales": votos_totales,
        "roi_promedio": roi_promedio,
    }
