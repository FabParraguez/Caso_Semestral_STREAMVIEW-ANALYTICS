# Entregable EP2 — StreamView Analytics

Este entregable utiliza el **dashboard interactivo en Streamlit** como solución principal,
manteniendo informe ejecutivo, resumen ejecutivo y estructura profesional reproducible.

## 1) Estructura del entregable

- `dashboard/dashboard_ep2_streamview.py`: dashboard principal en Streamlit.
- `notebooks/`: scripts `.py` de proceso ETL y espacio para notebooks de análisis.
- `data/input/`: archivos CSV de entrada.
- `outputs/`: archivos CSV y logs de salida del ETL.
- `src/analysis_ep2.py`: funciones de carga, filtros y cálculo de KPIs.
- `informe_ejecutivo_EP2.md`: informe técnico-ejecutivo del proyecto.
- `resumen_ejecutivo_EP2.md`: síntesis de hallazgos y recomendaciones.
- `requirements.txt`: dependencias para ejecución.
- `data/`, `images/`, `notebooks/`, `outputs/`: carpetas de apoyo del proyecto.

## 2) Cobertura de la pauta

El desarrollo cubre los apartados exigidos:
1. Problema de negocio.
2. Integración de fuentes de datos.
3. Análisis exploratorio con visualizaciones.
4. Dashboard en Streamlit con KPIs, filtros, navegación e interacción.
5. Storytelling para comunicar hallazgos.
6. Evaluación crítica de fortalezas, limitaciones y mejoras.
7. Conclusiones y recomendaciones orientadas a decisión.

## 3) Cómo ejecutar

Desde la raíz del repositorio:

1. Instalar dependencias:
   - `pip install -r Entregables_EP2/requirements.txt`
2. Ejecutar app:
   - `streamlit run Entregables_EP2/dashboard/dashboard_ep2_streamview.py`

## 4) Datos utilizados

Se consumen directamente los archivos del proyecto:
- `Entregables_EP2/outputs/peliculas_clean.csv`
- `Entregables_EP2/outputs/series_clean.csv`

### Reproceso ETL (opcional)
Si necesitas regenerar los datasets limpios desde EP2:

1. Crear copia en español (si aplica):
   - `python Entregables_EP2/notebooks/create_dataset_copy_es.py`
2. Ejecutar ETL de películas:
   - `python Entregables_EP2/notebooks/etl_dataset_Movies.py`
3. Ejecutar ETL de series:
   - `python Entregables_EP2/notebooks/etl_dataset_TvShows.py`

## 5) Criterios de evaluación cubiertos

- Visualizaciones estáticas y comparativas.
- Visualizaciones interactivas con filtros globales.
- Integración de múltiples fuentes.
- Diseño de dashboard orientado a negocio.
- Implementación de KPIs pertinentes.
- Organización profesional y reproducibilidad.

## 6) Próximo paso para entrega formal

Convertir los archivos markdown a PDF:
- `informe_ejecutivo_EP2.md` → `informe_ejecutivo_EP2.pdf`
- `resumen_ejecutivo_EP2.md` → `resumen_ejecutivo_EP2.pdf`

Además:
- incluir capturas/exportes del dashboard en PDF o PPT para respaldo ejecutivo.

## 7) Checklist de entrega final

- [ ] Dashboard Streamlit operativo en `Entregables_EP2/dashboard/dashboard_ep2_streamview.py`.
- [ ] Filtros globales funcionando (tipo, año, país, género, idioma).
- [ ] KPIs visibles y validados (títulos, rating, votos y ROI).
- [ ] Página de conclusiones/recomendaciones incluida en el dashboard.
- [ ] `informe_ejecutivo_EP2.pdf` generado.
- [ ] `resumen_ejecutivo_EP2.pdf` generado.
- [ ] Estructura de carpeta completa y ordenada.
- [ ] Evidencia visual exportada (PDF/PPT) para presentación.
