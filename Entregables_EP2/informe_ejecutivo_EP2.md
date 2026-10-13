# Informe Ejecutivo — StreamView Analytics (EP2)

## 1. Descripción del problema de negocio
StreamView Analytics requiere fortalecer decisiones de contenido para mejorar retención de clientes, nivel de interacción (engagement) y desempeño global del catálogo. Para ello, se analiza el comportamiento de películas y series considerando volumen de títulos, popularidad, valoración, distribución por segmentos y desempeño financiero de películas.

### 1.1 Contexto de decisión
Actualmente, las áreas de contenido y marketing enfrentan dos desafíos simultáneos:
- alta disponibilidad de datos, pero baja estandarización de criterios para priorización,
- dificultad para traducir señales analíticas en decisiones tácticas de corto plazo.

La consecuencia es una brecha entre el análisis y la ejecución: se identifica información útil, pero no siempre se convierte en acciones concretas de portafolio, promoción o inversión.

### 1.2 Preguntas de negocio que aborda el informe
1. ¿Qué segmentos (género, país, idioma, tipo) sostienen mejor desempeño relativo?
2. ¿Cómo evoluciona el catálogo en el tiempo y qué implicancias tiene para la estrategia de crecimiento?
3. ¿Qué evidencia financiera disponible permite priorizar decisiones de inversión en películas?
4. ¿Qué acciones concretas se pueden ejecutar en contenido y marketing con base en los hallazgos?

## 2. Objetivos del proyecto
1. Integrar fuentes de datos de películas y series en una base analítica unificada.
2. Construir KPIs ejecutivos para monitorear desempeño de catálogo.
3. Diseñar visualizaciones estáticas e interactivas para detectar patrones relevantes.
4. Implementar un dashboard navegable con filtros para exploración autónoma.
5. Comunicar hallazgos mediante una narrativa visual orientada a decisión.

### 2.1 Criterios de éxito
Se considera exitoso el entregable cuando:
- permite comparar segmentos bajo un marco homogéneo de lectura,
- reduce la ambigüedad en la interpretación de desempeño,
- habilita decisiones priorizadas con respaldo cuantitativo,
- es reutilizable y actualizable sin rediseñar toda la solución.

## 3. Audiencia objetivo y propósito comunicacional
- **Audiencia primaria**: gerencia de contenidos y áreas de marketing.
- **Audiencia secundaria**: dirección ejecutiva y analistas de negocio.
- **Propósito**: traducir datos complejos en señales accionables para priorizar inversiones, campañas y expansión del portafolio.

### 3.1 Uso esperado por audiencia
- **Dirección ejecutiva**: lectura de KPIs de síntesis y tendencias generales.
- **Gerencia de contenidos**: identificación de segmentos con potencial de expansión.
- **Marketing**: focalización de campañas según tracción observada.
- **Analistas**: validación de hipótesis y profundización por filtros.

## 4. Fuentes de datos utilizadas
- `Dataset_Utilizado/peliculas_clean.csv`
- `Dataset_Utilizado/series_clean.csv`

### Variables relevantes
- Identificación: `id_muestra`, `tipo`, `titulo`
- Segmentación: `anio_estreno`, `pais_principal`, `genero_principal`, `idioma`
- Engagement/calidad: `popularidad`, `votos`, `promedio_votos`
- Finanzas (películas): `presupuesto`, `ingresos`, `roi`

### 4.1 Alcances y supuestos de datos
- El análisis financiero se aplica solo a películas con `presupuesto` e `ingresos` válidos.
- Las comparaciones por segmentos se interpretan como evidencia descriptiva, no causal.
- La calidad de inferencia depende de la densidad de títulos por segmento (evitar conclusiones con muestras pequeñas).

## 5. Análisis exploratorio (EDA)
Se aplicaron filtros globales por tipo, año, país, género e idioma, con análisis en cinco ejes:
1. **Vista ejecutiva**: KPIs y tendencia temporal del catálogo.
2. **Segmentación**: concentración por género y país.
3. **Rendimiento financiero**: presupuesto vs ingresos y ranking por ROI.
4. **Storytelling**: síntesis de hallazgos y recomendaciones.
5. **Evaluación crítica**: fortalezas, limitaciones y mejoras.

### 5.1 Hallazgos de lectura transversal
- La composición del catálogo presenta concentración en segmentos dominantes, útil para explotar eficiencias, pero con riesgo de saturación.
- La relación entre popularidad, rating y volumen de votos no es lineal en todos los segmentos; por ello se recomienda una lectura combinada de KPIs.
- En películas, el comportamiento de ROI evidencia heterogeneidad: mayor presupuesto no garantiza mayor retorno relativo.

### 5.2 Implicancias para decisión
- Priorizar segmentos con equilibrio entre tracción (popularidad) y calidad percibida (rating + votos).
- Diferenciar decisiones de expansión (nuevos segmentos) versus optimización (segmentos actuales con mejor retorno esperado).
- Usar el módulo financiero para definir umbrales mínimos de viabilidad en nuevas iniciativas audiovisuales.

## 6. Justificación de representaciones gráficas
- **Líneas**: evolución temporal de títulos por tipo.
- **Barras horizontales**: comparación clara de rankings (géneros/países).
- **Dispersión**: relación presupuesto-ingresos y detección de desempeño relativo.
- **Tabla interactiva**: detalle operacional para seguimiento de títulos.

Estas opciones favorecen lectura rápida para negocio y profundidad para analistas.

### 6.1 Criterios de diseño aplicados
- minimizar carga cognitiva en vistas ejecutivas,
- mantener consistencia visual entre páginas,
- privilegiar comparabilidad entre segmentos,
- permitir drill-down mediante filtros sin perder contexto global.

## 7. Desarrollo de narrativa visual (Data Storytelling)
Se estructuró en cuatro pasos:
1. Contexto y objetivo estratégico.
2. Hallazgos clave de desempeño de catálogo.
3. Implicancias para priorización de inversión.
4. Recomendaciones accionables por portafolio, marketing y finanzas.

### 7.1 Mensaje central
La evidencia sugiere que la ventaja competitiva no depende solo de aumentar volumen de títulos, sino de gestionar selectivamente el portafolio con criterios de desempeño combinado (alcance, valoración y retorno).

### 7.2 Enfoque comunicacional
Se priorizó una narrativa orientada a acción: cada hallazgo se vincula con una decisión sugerida, evitando reportes descriptivos sin consecuencia operativa.

## 8. Diseño e implementación del dashboard interactivo
Archivo principal de entrega:
- `Entregables_EP2/dashboard/dashboard_ep2_streamview.py`

Características implementadas en Streamlit:
- Navegación por secciones temáticas (vista ejecutiva, segmentación, finanzas y recomendaciones).
- Filtros globales por tipo, año, país, género e idioma.
- KPIs ejecutivos y visualizaciones interactivas para exploración de detalle.
- Sección de evaluación crítica de la solución.

### 8.1 Valor operativo del dashboard
- centraliza la conversación entre áreas bajo un mismo marco de indicadores,
- acelera ciclos de decisión al reducir dependencia de análisis manuales ad hoc,
- deja trazabilidad de criterios al trabajar con una capa visual consistente.

## 9. Evaluación crítica de la solución
### Fortalezas
- Integración unificada de películas y series.
- Lectura ejecutiva y técnica en una sola herramienta.
- Alto potencial de reutilización del flujo analítico.

### Limitaciones
- Falta de datos de churn/sesiones a nivel usuario.
- Enfoque descriptivo (no causal).
- Datos financieros concentrados en películas.

### Oportunidades de mejora
- Incorporar eventos transaccionales y cohortes.
- Agregar modelos predictivos de demanda.
- Automatizar actualización y versionado de reportes.

### 9.1 Riesgos de interpretación a gestionar
- confundir correlación con causalidad en decisiones estratégicas,
- sobrerreaccionar ante segmentos con alta volatilidad y poca base muestral,
- extrapolar señales financieras de películas a series sin evidencia equivalente.

## 10. Conclusiones y recomendaciones
1. Priorizar contenido en géneros y países de mayor tracción.
2. Enfocar campañas en segmentos con mayor rating y volumen de votos.
3. Asignar inversión con criterio de ROI histórico y desempeño de engagement.
4. Fortalecer gobierno de datos para ampliar análisis de retención real.

### 10.1 Plan de continuidad sugerido
1. Institucionalizar una revisión mensual de KPIs y segmentos críticos.
2. Definir umbrales de decisión para promoción, adquisición y continuidad de contenido.
3. Integrar métricas de consumo por usuario para avanzar desde analítica descriptiva a analítica predictiva.
4. Consolidar una versión ejecutiva periódica del dashboard para comités de dirección.
