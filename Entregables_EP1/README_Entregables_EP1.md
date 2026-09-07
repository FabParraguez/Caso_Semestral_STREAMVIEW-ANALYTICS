# Entregables EP1 — Qué se creó y cómo usarlo

## Archivos creados
- **Informe base para PDF:** `Informe_Ejecutivo_EP1.md`
- **Dashboard interactivo:** `dashboard_streamlit.py`
- **Dependencias del dashboard:** `requirements_dashboard.txt`

## Cobertura de pauta y rúbrica
Este paquete cubre los apartados exigidos del encargo:

1. Problema de negocio (contexto, audiencia, objetivos comunicacionales)
2. Fuentes de datos e integración
3. Análisis exploratorio y hallazgos
4. Justificación de visualizaciones y atributos visuales
5. Dashboard interactivo con KPIs, filtros, navegación e interacción
6. Narrativa visual (storytelling)
7. Evaluación crítica (fortalezas, limitaciones, mejoras)
8. Conclusiones y recomendaciones

También incorpora una matriz de cumplimiento para indicadores:
**IE4, IE5, IE6, IE7, IE9, IE10**.

## Cómo convertir el informe a PDF
1. Abre `Informe_Ejecutivo_EP1.md` en VS Code.
2. Exporta a PDF desde tu extensión de Markdown o imprime a PDF.
3. Inserta capturas del dashboard en secciones 4, 5 y 7 para reforzar evidencia visual.

## Cómo ejecutar el dashboard
1. Instala dependencias con `requirements_dashboard.txt`.
2. Ejecuta Streamlit con el archivo `dashboard_streamlit.py`.
3. Explora por filtros:
   - `tipo`
   - rango de `anio_estreno`
   - `pais_principal`
   - `genero_principal`
   - `idioma`

## Recomendación para máxima calificación
- Mantener consistencia de color por `tipo` en todas las vistas.
- Limitar texto por visual a un mensaje principal.
- Mostrar siempre interpretación de negocio junto al gráfico.
- Agregar 2–3 recomendaciones accionables por página del dashboard.
