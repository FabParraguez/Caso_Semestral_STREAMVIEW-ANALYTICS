"""
ETL - Netflix Movies Detailed up to 2025 (ES)
StreamView Analytics - Proyecto Visual Analytics
------------------------------------------------
Aplica limpieza y transformaciones documentadas para dejar el dataset
de PELICULAS listo para análisis y visualización.

Salidas:
 1. peliculas_clean.csv        -> UNA FILA POR PAIS (dataset limpio ya explotado por 'pais').
                                   Si una pelicula tiene 3 paises, aparece 3 veces (una por pais),
                                   conservando TODAS las columnas limpias (incluidas financieras).
                                   Incluye 'cantidad_paises' para saber cuando NO sumar dinero.
 2. peliculas_por_genero.csv   -> explode de genero (para rankings/gráficos por género)
 3. log_calidad_peliculas.txt  -> resumen de decisiones tomadas (trazabilidad)
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_CANDIDATES = [
    BASE_DIR / "StreamViewAnalytics" / "DataSet_Espanol" / "netflix_movies_detailed_up_to_2025_es.csv",
    BASE_DIR / "StreamViewAnalytics" / "DataSet_Original" / "netflix_movies_detailed_up_to_2025.csv",
    BASE_DIR / "StreamViewAnalytics" / "DataSet_Copy" / "netflix_movies_detailed_up_to_2025_es.csv",
    BASE_DIR / "StreamViewAnalytics" / "Data_Movies" / "netflix_movies_detailed_up_to_2025.csv",
    BASE_DIR / "Data_Movies" / "netflix_movies_detailed_up_to_2025.csv",
]
INPUT_PATH = next((p for p in INPUT_CANDIDATES if p.exists()), INPUT_CANDIDATES[0])
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
# 2. ELIMINAR COLUMNAS NO UTILIZABLES
# =========================================================
# 'duracion' esta 100% vacia -> se elimina y se documenta como limitacion.
if df["duracion"].isnull().mean() == 1.0:
    df = df.drop(columns=["duracion"])
    log_print("Columna 'duracion' eliminada: 100% de valores nulos (no disponible en la fuente).")

# 'clasificacion' es identica a 'promedio_votos' (no es clasificacion por edad real).
# Se elimina para evitar interpretarla erroneamente como rating de edad.
if (df["clasificacion"] == df["promedio_votos"]).mean() == 1.0:
    df = df.drop(columns=["clasificacion"])
    log_print(
        "Columna 'clasificacion' eliminada: contenido identico a 'promedio_votos' "
        "(error de mapeo en la fuente). No representa clasificacion por edad; "
        "esa variable NO esta disponible para este dataset."
    )

# 'tipo' es constante ("Pelicula") -> se mantiene solo como referencia de origen.

# =========================================================
# 3. NORMALIZAR TEXTO (espacios, mayusculas/minusculas consistentes)
# =========================================================
cols_texto = ["titulo", "director", "reparto", "pais", "generos", "idioma"]
for col in cols_texto:
    df[col] = df[col].astype("string").str.strip()

# =========================================================
# 4. FECHAS Y TIPOS
# =========================================================
df["fecha_agregada"] = pd.to_datetime(df["fecha_agregada"], errors="coerce")
n_fechas_invalidas = df["fecha_agregada"].isnull().sum()
log_print(f"Fechas 'fecha_agregada' no parseables: {n_fechas_invalidas}")

# =========================================================
# 5. DUPLICADOS
# =========================================================
dup_id = df["id_muestra"].duplicated().sum()
log_print(f"Duplicados por 'id_muestra': {dup_id}")

dup_titulo_anio = df.duplicated(subset=["titulo", "anio_estreno"]).sum()
log_print(f"Duplicados por 'titulo' + 'anio_estreno': {dup_titulo_anio} (se conservan, se documentan)")
# Nota: se decide NO eliminarlos automaticamente porque pueden ser ediciones
# distintas (ej. remasterizaciones). Se deja marcado para revision manual.
df["posible_duplicado"] = df.duplicated(subset=["titulo", "anio_estreno"], keep=False)

# =========================================================
# 6. VALORES FALTANTES (nulos)
# =========================================================
for col in ["director", "reparto", "pais", "generos", "descripcion"]:
    n_nulos = df[col].isnull().sum()
    if n_nulos > 0:
        df[col] = df[col].fillna("Sin informacion")
        log_print(f"Columna '{col}': {n_nulos} nulos imputados como 'Sin informacion'.")

# =========================================================
# 7. PAIS PRINCIPAL Y GENERO PRINCIPAL (para tablas 1 fila = 1 contenido)
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
    "(primer valor de cada lista) para mantener 1 fila = 1 pelicula."
)

# =========================================================
# 8. REGLAS DE NEGOCIO FINANCIERAS (presupuesto / ingresos)
# =========================================================
# Regla de negocio #6 del caso: contenidos sin presupuesto o ingresos
# NO deben considerarse en indicadores financieros.
df["valido_para_financiero"] = (df["presupuesto"] > 0) & (df["ingresos"] > 0)
n_no_validos = (~df["valido_para_financiero"]).sum()
log_print(
    f"Registros marcados como NO validos para KPIs financieros "
    f"(presupuesto o ingresos en 0): {n_no_validos} de {len(df)} "
    f"({round(n_no_validos/len(df)*100,1)}%)."
)

# ROI solo calculado donde es valido, para evitar divisiones por cero
df["roi"] = None
mask = df["valido_para_financiero"]
df.loc[mask, "roi"] = (df.loc[mask, "ingresos"] - df.loc[mask, "presupuesto"]) / df.loc[mask, "presupuesto"]
log_print("Columna 'roi' calculada solo para registros validos: (ingresos - presupuesto) / presupuesto.")

# =========================================================
# 9. OUTLIERS DE POPULARIDAD (se marcan, no se eliminan)
# =========================================================
p99 = df["popularidad"].quantile(0.99)
df["outlier_popularidad"] = df["popularidad"] > p99
log_print(
    f"Se marcaron como 'outlier_popularidad' los registros sobre el percentil 99 "
    f"(> {round(p99,2)}): {df['outlier_popularidad'].sum()} registros. "
    f"No se eliminan, solo se etiquetan para tratamiento visual (ej. escala log)."
)

# =========================================================
# 10. EXPLODE DE 'pais' DIRECTAMENTE SOBRE EL DATASET LIMPIO (salida unica)
# =========================================================
# En lugar de mantener dos archivos separados (uno con 1 fila = 1 pelicula y
# otro solo con pais explotado), se deja UN UNICO archivo "peliculas_clean.csv"
# donde 'pais' ya viene explotado: si una pelicula tiene 3 paises, va a
# aparecer en 3 filas (una por cada pais), pero conservando TODAS las columnas
# limpias generadas (incluidas presupuesto, ingresos, roi, etc.).
#
# Esto es correcto para responder preguntas como "¿que paises producen mas
# contenido?" (cada pais debe contar +1 por cada pelicula en la que participo).
#
# IMPORTANTE (queda documentado y en columna 'cantidad_paises'):
# NO se debe sumar 'presupuesto', 'ingresos' ni 'roi' agrupando por pais sin
# considerar que una misma pelicula puede repetirse varias veces. Para KPIs
# financieros agregados, filtrar primero por 'pais_principal' o deduplicar
# por 'id_muestra'.
df_exploded = df.assign(pais=df["pais"].str.split(",")).explode("pais")
df_exploded["pais"] = df_exploded["pais"].str.strip()
log_print(
    f"Columna 'pais' explotada sobre el dataset limpio: {len(df)} peliculas "
    f"originales -> {len(df_exploded)} filas finales (una fila por cada pais "
    "de produccion). Se conservan todas las columnas limpias, incluidas las "
    "financieras. NO sumar presupuesto/ingresos/roi por pais sin deduplicar "
    "por 'id_muestra' o usar 'pais_principal' para evitar multiplicar los "
    "montos de peliculas coproducidas."
)

out_main = OUTPUT_DIR / "peliculas_clean.csv"
df_exploded.to_csv(out_main, index=False)
log_print(f"Archivo generado: {out_main} ({len(df_exploded)} filas, {len(df_exploded.columns)} columnas)")

# =========================================================
# 11. TABLA EXPLOTADA POR GENERO (para rankings de conteo por genero)
# =========================================================
df_genero = df.assign(generos=df["generos"].str.split(",")).explode("generos")
df_genero["generos"] = df_genero["generos"].str.strip()
cols_genero = [
    "id_muestra", "titulo", "anio_estreno", "generos", "pais_principal",
    "idioma", "popularidad", "promedio_votos", "votos"
]
df_genero = df_genero[cols_genero]
out_genero = OUTPUT_DIR / "peliculas_por_genero.csv"
df_genero.to_csv(out_genero, index=False)
log_print(
    f"Archivo generado: {out_genero} ({len(df_genero)} filas). "
    "USO: solo para conteos/rankings por genero. NO sumar presupuesto/ingresos aqui."
)

# =========================================================
# 12. LOG DE CALIDAD
# =========================================================
out_log = OUTPUT_DIR / "log_calidad_peliculas.txt"
with open(out_log, "w", encoding="utf-8") as f:
    f.write("LOG DE CALIDAD DE DATOS - PELICULAS (StreamView Analytics)\n")
    f.write("=" * 65 + "\n\n")
    f.write("\n".join(log))
    f.write(f"\n\nFilas finales en peliculas_clean.csv: {len(df)}\n")
log_print(f"Log de calidad generado: {out_log}")

print("\nETL de PELICULAS finalizado correctamente.")