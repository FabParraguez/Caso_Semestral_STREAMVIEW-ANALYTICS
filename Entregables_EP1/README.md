# Dashboard de Gerencia de Contenidos — StreamView Analytics

Dashboard interactivo orientado a la Evaluación Parcial 2 (diseño de dashboards) y a las decisiones de adquisición, gestión y promoción de contenidos.

## Puesta en marcha

Desde la raíz del proyecto:

```powershell
pip install -r .\Entregables_EP1\requirements_dashboard.txt
streamlit run .\Entregables_EP1\dashboard_gerencia_contenidos.py
```

Streamlit indicará la URL local para abrir el dashboard, normalmente `http://localhost:8501`.

## Alcance e interacción

- Síntesis ejecutiva y KPI de catálogo y finanzas de películas.
- Filtros globales por tipo, año, país productor, género e idioma, con opción para restablecerlos.
- Navegación lateral hacia composición, desempeño por género, países, finanzas y recomendaciones.
- Tablas de detalle y visualizaciones interactivas para profundizar en segmentos del catálogo.
- Justificación de diseño, metodología y limitaciones disponible al final del dashboard.

**Criterios de lectura:** popularidad es un índice del dataset, no reproducciones; el país corresponde a producción; ROI considera películas con presupuesto e ingresos positivos. Las series no tienen indicadores financieros comparables en la fuente.

## Datos requeridos

El dashboard carga `Dataset_Utilizado/peliculas_clean.csv` y `Dataset_Utilizado/series_clean.csv` desde la raíz del proyecto.
