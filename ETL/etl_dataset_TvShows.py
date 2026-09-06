"""
ETL - Netflix TV Shows Detailed up to 2025 (ES)
StreamView Analytics - Proyecto Visual Analytics
------------------------------------------------
Aplica limpieza y transformaciones documentadas para dejar el dataset
de SERIES listo para análisis y visualización.

Salidas:
 1. series_clean.csv        -> UNA FILA POR PAIS (dataset limpio ya explotado por 'pais').
                                Si una serie tiene 3 paises, aparece 3 veces (una por pais),
                                conservando TODAS las columnas limpias generadas.
                                Incluye 'cantidad_paises' para saber cuando NO duplicar conteos.
 2. series_por_genero.csv   -> explode de genero (para rankings/gráficos por género)
 3. log_calidad_series.txt  -> resumen de decisiones tomadas (trazabilidad)
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_CANDIDATES = [
    BASE_DIR / "StreamViewAnalytics" / "DataSet_Espanol" / "netflix_tv_shows_detailed_up_to_2025_es.csv",
    BASE_DIR / "StreamViewAnalytics" / "DataSet_Original" / "netflix_tv_shows_detailed_up_to_2025.csv",
    BASE_DIR / "StreamViewAnalytics" / "DataSet_Copy" / "netflix_tv_shows_detailed_up_to_2025_es.csv",
    BASE_DIR / "StreamViewAnalytics" / "dataset_copy" / "netflix_tv_shows_detailed_up_to_2025_es.csv",
    BASE_DIR / "StreamViewAnalytics" / "Data_Movies" / "netflix_tv_shows_detailed_up_to_2025.csv",
    BASE_DIR / "Data_Movies" / "netflix_tv_shows_detailed_up_to_2025.csv",
]
INPUT_PATH = next((path for path in INPUT_CANDIDATES if path.exists()), INPUT_CANDIDATES[0])
OUTPUT_DIR = BASE_DIR / "dataset_utilizado"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

log = []


def log_print(msg):
    print(msg)
    log.append(msg)


# =========================================================
# 1. CARGA
# =========================================================
df = pd.read_csv(INPUT_PATH)
filas_iniciales = len(df)
log_print(f"Filas cargadas: {filas_iniciales}")
log_print(f"Columnas originales: {list(df.columns)}")

# =========================================================
# 2. DUPLICADOS EXACTOS DE ID (a diferencia de peliculas, aqui SI existen)
# =========================================================
dup_id_antes = df["id_muestra"].duplicated().sum()
log_print(f"Duplicados exactos por 'id_muestra' detectados: {dup_id_antes}")

# Se verifico manualmente: son filas 100% identicas (mismo titulo, anio, pais).
# Se eliminan conservando la primera ocurrencia.
df = df.drop_duplicates(subset=["id_muestra"], keep="first")
log_print(
    f"Se eliminaron {dup_id_antes} filas duplicadas exactas de 'id_muestra' "
    f"(mismo titulo/anio/pais). Filas restantes: {len(df)}."
)

# =========================================================
# 3. ELIMINAR COLUMNAS NO UTILIZABLES
# =========================================================
# 'duracion' es constante ("1 Temporadas" en el 100% de los casos) -> no aporta
# informacion real sobre la duracion de cada serie. Se elimina y se documenta.
if df["duracion"].nunique() == 1:
    valor_constante = df["duracion"].unique()[0]
    df = df.drop(columns=["duracion"])
    log_print(
        f"Columna 'duracion' eliminada: valor constante ('{valor_constante}') "
        "en el 100% de los registros. No representa la duracion real de la serie."
    )

# 'clasificacion' es identica a 'promedio_votos' (mismo problema que en peliculas).
if (df["clasificacion"] == df["promedio_votos"]).mean() == 1.0:
    df = df.drop(columns=["clasificacion"])
    log_print(
        "Columna 'clasificacion' eliminada: contenido identico a 'promedio_votos' "
        "(error de mapeo en la fuente). No representa clasificacion por edad; "
        "esa variable NO esta disponible para este dataset."
    )

# 'tipo' es constante ("Serie") -> se mantiene solo como referencia de origen.

# =========================================================
# 4. NORMALIZAR TEXTO
# =========================================================
cols_texto = ["titulo", "director", "reparto", "pais", "generos", "idioma"]
for col in cols_texto:
    df[col] = df[col].astype("string").str.strip()

# =========================================================
# 5. FECHAS
# =========================================================
df["fecha_agregada"] = pd.to_datetime(df["fecha_agregada"], errors="coerce")
n_fechas_invalidas = df["fecha_agregada"].isnull().sum()
log_print(f"Fechas 'fecha_agregada' no parseables: {n_fechas_invalidas}")

# =========================================================
# 6. DUPLICADOS POR TITULO + AÑO (no exactos, se documentan sin eliminar)
# =========================================================
dup_titulo_anio = df.duplicated(subset=["titulo", "anio_estreno"]).sum()
log_print(f"Duplicados por 'titulo' + 'anio_estreno' (no exactos): {dup_titulo_anio} (se conservan, se documentan)")
df["posible_duplicado"] = df.duplicated(subset=["titulo", "anio_estreno"], keep=False)

# =========================================================
# 7. VALORES FALTANTES
# =========================================================
# 'director' tiene un porcentaje de nulos muy alto (~68%). Se imputa igual que
# el resto de columnas de texto, pero se deja advertencia explicita en el log
# para que no se use como variable confiable en analisis por director.
for col in ["director", "reparto", "pais", "generos", "descripcion"]:
    n_nulos = df[col].isnull().sum()
    pct = round(n_nulos / len(df) * 100, 1)
    if n_nulos > 0:
        df[col] = df[col].fillna("Sin informacion")
        log_print(f"Columna '{col}': {n_nulos} nulos ({pct}%) imputados como 'Sin informacion'.")

log_print(
    "ADVERTENCIA: 'director' presenta ~68% de nulos en series. No se recomienda "
    "usar esta variable para analisis o rankings por director en el dataset de series "
    "(insuficiente cobertura de datos)."
)

# =========================================================
# 8. PAIS PRINCIPAL Y GENERO PRINCIPAL
# =========================================================
df["pais_principal"] = df["pais"].str.split(",").str[0].str.strip()
df["genero_principal"] = df["generos"].str.split(",").str[0].str.strip()
df["cantidad_paises"] = df["pais"].apply(
    lambda x: 0 if x == "Sin informacion" else len(str(x).split(","))
)
df["cantidad_generos"] = df["generos"].apply(
    lambda x: 0 if x == "Sin informacion" else len(str(x).split(","))
)
log_print(
    "Se crearon columnas 'pais_principal' y 'genero_principal' "
    "(primer valor de cada lista) para mantener 1 fila = 1 serie."
)

# =========================================================
# 9. VOTOS EN CERO (afecta calificacion promedio si no se filtra)
# =========================================================
df["valido_para_calificacion"] = df["votos"] > 0
n_sin_votos = (~df["valido_para_calificacion"]).sum()
log_print(
    f"Registros marcados como NO validos para KPIs de calificacion "
    f"(votos = 0): {n_sin_votos} de {len(df)} ({round(n_sin_votos/len(df)*100,1)}%)."
)

# =========================================================
# 10. OUTLIERS DE POPULARIDAD
# =========================================================
p99 = df["popularidad"].quantile(0.99)
df["outlier_popularidad"] = df["popularidad"] > p99
log_print(
    f"Se marcaron como 'outlier_popularidad' los registros sobre el percentil 99 "
    f"(> {round(p99,2)}): {df['outlier_popularidad'].sum()} registros. "
    f"No se eliminan, solo se etiquetan para tratamiento visual (ej. escala log)."
)

# =========================================================
# 11. NOTA SOBRE VARIABLES FINANCIERAS (no existen en series)
# =========================================================
log_print(
    "NOTA: El dataset de series no incluye 'presupuesto' ni 'ingresos'. "
    "Segun la regla de negocio del caso, estas variables solo aplican a peliculas. "
    "No se agregan columnas ficticias; los KPIs financieros deben excluir series."
)

# =========================================================
# 12. EXPLODE DE 'pais' DIRECTAMENTE SOBRE EL DATASET LIMPIO (salida unica)
# =========================================================
# En lugar de mantener dos archivos separados (uno con 1 fila = 1 serie y
# otro solo con pais explotado), se deja UN UNICO archivo "series_clean.csv"
# donde 'pais' ya viene explotado: si una serie tiene 3 paises, va a aparecer
# en 3 filas (una por cada pais), pero conservando TODAS las columnas
# limpias generadas.
#
# Esto es correcto para responder preguntas como "¿que paises producen mas
# contenido?" (cada pais debe contar +1 por cada serie en la que participo).
#
# IMPORTANTE (queda documentado y en columna 'cantidad_paises'):
# NO se debe sumar 'popularidad', 'votos' ni ninguna metrica agrupando por
# pais sin considerar que una misma serie puede repetirse varias veces.
# Para conteos totales de series (no por pais), deduplicar por 'id_muestra'
# o usar 'pais_principal'.
df_exploded = df.assign(pais=df["pais"].str.split(",")).explode("pais")
df_exploded["pais"] = df_exploded["pais"].str.strip()
log_print(
    f"Columna 'pais' explotada sobre el dataset limpio: {len(df)} series "
    f"originales -> {len(df_exploded)} filas finales (una fila por cada pais "
    "de produccion). Se conservan todas las columnas limpias. NO sumar "
    "popularidad/votos por pais sin deduplicar por 'id_muestra' o usar "
    "'pais_principal' para evitar multiplicar los valores de series "
    "coproducidas."
)

out_main = OUTPUT_DIR / "series_clean.csv"
df_exploded.to_csv(out_main, index=False)
log_print(f"Archivo generado: {out_main} ({len(df_exploded)} filas, {len(df_exploded.columns)} columnas)")

# =========================================================
# 13. TABLA EXPLOTADA POR GENERO (para rankings de conteo por genero)
# =========================================================
df_genero = df.assign(generos=df["generos"].str.split(",")).explode("generos")
df_genero["generos"] = df_genero["generos"].str.strip()
duplicados_genero = df_genero.duplicated(subset=["id_muestra", "generos"]).sum()
df_genero = df_genero.drop_duplicates(subset=["id_muestra", "generos"], keep="first")
log_print(
    f"Se eliminaron {duplicados_genero} combinaciones repetidas de "
    "'id_muestra' + 'generos' originadas por géneros duplicados en la fuente."
)
cols_genero = [
    "id_muestra", "titulo", "anio_estreno", "generos", "pais_principal",
    "idioma", "popularidad", "promedio_votos", "votos"
]
df_genero = df_genero[cols_genero]
out_genero = OUTPUT_DIR / "series_por_genero.csv"
df_genero.to_csv(out_genero, index=False)
log_print(f"Archivo generado: {out_genero} ({len(df_genero)} filas). USO: solo para conteos/rankings por genero.")

# =========================================================
# 14. LOG DE CALIDAD
# =========================================================
out_log = OUTPUT_DIR / "log_calidad_series.txt"
with open(out_log, "w", encoding="utf-8") as f:
    f.write("LOG DE CALIDAD DE DATOS - SERIES (StreamView Analytics)\n")
    f.write("=" * 65 + "\n\n")
    f.write("\n".join(log))
    f.write(f"\n\nFilas finales en series_clean.csv: {len(df)}\n")
log_print(f"Log de calidad generado: {out_log}")

print("\nETL de SERIES finalizado correctamente.")