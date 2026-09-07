# Informe Ejecutivo EP1 — StreamView Analytics

## Portada
- **Proyecto:** StreamView Analytics — Visualización de Datos
- **Evaluación:** EP1 (Comprensión del negocio y exploración visual)
- **Fecha:** 7 de septiembre de 2026
- **Equipo:** Tabatha Gamboa, Fabián Parragues

---

## Resumen ejecutivo
StreamView Analytics, plataforma de streaming orientada al mercado latinoamericano, enfrenta un desafío de gestión analítica: si bien dispone de un volumen amplio de datos sobre su catálogo audiovisual, las áreas internas trabajan con reportes aislados y criterios no homogéneos. Esto provoca inconsistencias en indicadores, dificulta la comparación entre segmentos y reduce la velocidad de decisión para adquisición, promoción y posicionamiento de contenidos.

Para responder a este problema, se desarrolló una base analítica integrada sobre dos fuentes oficiales (películas y series), aplicando procesos de limpieza, estandarización semántica y reglas de calidad. A partir de esta integración se propuso una solución de Visual Analytics con foco en: (1) estado del catálogo, (2) tendencias de producción/disponibilidad, (3) desempeño por país, género e idioma, y (4) métricas de engagement y financieras cuando corresponde.

El resultado de EP1 es una propuesta estructurada de comunicación de datos que alinea audiencia, objetivos y representaciones visuales, minimizando carga cognitiva y mejorando interpretación para la toma de decisiones ejecutivas.

---

## 1) Descripción del problema de negocio

### 1.1 Contexto organizacional
StreamView Analytics mantiene crecimiento sostenido del catálogo y opera en un entorno competitivo. La organización requiere transformar datos de contenidos en decisiones concretas de negocio. Sin embargo, la fragmentación de reportes por área genera:

- múltiples versiones del mismo indicador,
- dificultad para identificar tendencias transversales,
- baja trazabilidad sobre criterios de cálculo,
- decisiones de adquisición y promoción con evidencia parcial.

El problema central es **comunicacional y analítico**: convertir información dispersa en una narrativa visual clara y consistente para distintos niveles de decisión.

### 1.2 Audiencia objetivo
- **Directorio y Gerencia General:** visión consolidada del catálogo, comparaciones y prioridades estratégicas.
- **Gerencia de Contenidos y Adquisición:** identificación de segmentos con mayor potencial para licencias y renovaciones.
- **Gerencia de Marketing:** priorización de campañas según popularidad, valoración y volumen de contenidos.
- **Equipo Data & Analytics y Producto:** estandarización de indicadores y mantenimiento de dashboards corporativos.

### 1.3 Objetivos de comunicación de la solución
La solución propuesta busca:

1. sintetizar el estado del catálogo en indicadores clave comparables,
2. evidenciar patrones y tendencias relevantes para priorización,
3. facilitar exploración interactiva por filtros de negocio,
4. comunicar hallazgos mediante una narrativa visual orientada a acción.

---

## 2) Objetivos del proyecto

### 2.1 Objetivo general
Diseñar una solución de Visual Analytics que comunique información estratégica del catálogo audiovisual para apoyar la toma de decisiones en StreamView Analytics.

### 2.2 Objetivos específicos
- Caracterizar el catálogo por `tipo`, `país`, `género`, `idioma` y `año de estreno`.
- Analizar desempeño mediante `popularidad`, `votos` y `promedio_votos`.
- Incorporar análisis financiero de películas con `presupuesto`, `ingresos` y `roi`.
- Diseñar visualizaciones de alta legibilidad y baja carga cognitiva.
- Construir un dashboard interactivo con KPIs, filtros y navegación.
- Elaborar una narrativa visual clara para públicos ejecutivos y tácticos.

---

## 3) Descripción e integración de las fuentes de datos

### 3.1 Fuentes utilizadas
- **Netflix Movies Detailed up to 2025** (películas; ~16.000 registros).
- **Netflix TV Shows Detailed up to 2025** (series; ~16.000 registros).

### 3.2 Integración aplicada
Se aplicó una integración por etapas:

1. **Estandarización semántica y de idioma**
   - Traducción y homologación de encabezados (`show_id` → `id_muestra`, `title` → `titulo`, etc.).
   - Homologación de catálogos de `tipo`, `generos`, `idioma` y `pais`.

2. **Limpieza y calidad de datos**
   - Parseo de `fecha_agregada`.
   - Normalización de texto y manejo de nulos en variables descriptivas.
   - Control de duplicados por `id_muestra` y marcaje de `posible_duplicado`.
   - Remoción de atributos no confiables/no informativos (`duracion`, `clasificacion` según regla ETL documentada).

3. **Variables derivadas para análisis**
   - `pais_principal`, `genero_principal`.
   - `cantidad_paises`, `cantidad_generos`.
   - Banderas de validez: `valido_para_financiero` (películas), `valido_para_calificacion` (series).
   - `roi` para películas con datos financieros válidos.

4. **Salidas para visualización**
   - `peliculas_clean.csv`, `series_clean.csv`.
   - `peliculas_por_genero.csv`, `series_por_genero.csv`.
   - logs de trazabilidad de calidad por dominio.

### 3.3 Variables relevantes para visualizaciones
- Identidad y segmentación: `id_muestra`, `tipo`, `anio_estreno`, `pais`, `pais_principal`, `generos`, `genero_principal`, `idioma`.
- Engagement: `popularidad`, `votos`, `promedio_votos`.
- Finanzas (películas): `presupuesto`, `ingresos`, `roi`, `valido_para_financiero`.

---

## 4) Análisis exploratorio mediante visualizaciones

### 4.1 Preguntas analíticas
1. ¿Cómo evoluciona la cantidad de títulos por año?
2. ¿Qué géneros y países concentran mayor volumen de contenidos?
3. ¿Existe relación entre popularidad, votos y valoración promedio?
4. En películas, ¿cómo se relacionan presupuesto e ingresos?

### 4.2 Visualizaciones exploratorias propuestas
- **Serie temporal de títulos por año** (`anio_estreno`) para detectar crecimiento y ciclos.
- **Barras horizontales Top 10 géneros** para ranking y comparación de magnitudes.
- **Barras horizontales Top 10 países** para concentración geográfica del catálogo.
- **Dispersión `popularidad` vs `promedio_votos`** para identificar segmentos de percepción del público.
- **Dispersión `presupuesto` vs `ingresos` (solo películas válidas)** para evaluar eficiencia relativa y retornos.

### 4.3 Hallazgos esperables (línea base)
- concentración en pocos países productores,
- dominios de géneros específicos en volumen,
- presencia de títulos con alta popularidad pero valoración media,
- relación no lineal entre inversión y recaudación.

---

## 5) Justificación de representaciones gráficas

### 5.1 Selección de gráficos según naturaleza de datos
- **Barras:** variables categóricas nominales (`género`, `país`) y comparación de frecuencias.
- **Líneas/área:** datos temporales (`anio_estreno`) y lectura de tendencia.
- **Dispersión:** relación entre variables continuas (`popularidad`, `votos`, `presupuesto`, `ingresos`).
- **Tarjetas KPI:** síntesis ejecutiva de indicadores críticos.

### 5.2 Atributos visuales aplicados
- **Color:** codificación semántica por `tipo` (película/serie) y énfasis en métricas clave.
- **Tamaño/posición:** orden descendente en rankings para reducir esfuerzo de búsqueda.
- **Contraste:** paleta sobria con acentos para outliers y focos narrativos.
- **Forma:** consistencia visual para facilitar reconocimiento de patrones.

### 5.3 Carga cognitiva y legibilidad
- layout por bloques (KPIs → tendencias → comparativos → detalle),
- máximo 1 mensaje principal por visual,
- eliminación de elementos decorativos no informativos,
- filtros globales consistentes en todas las vistas.

---

## 6) Desarrollo de narrativa visual (Data Storytelling)

### 6.1 Estructura narrativa
1. **Situación:** crecimiento del catálogo y necesidad de consolidación.
2. **Hallazgos:** concentración por segmentos, diferencias de desempeño y focos de oportunidad.
3. **Implicancias:** impacto en adquisición, promoción y posicionamiento.
4. **Acción recomendada:** priorización por evidencia y revisión periódica de KPIs.

### 6.2 Mensaje por audiencia
- **Directorio/Gerencia General:** dónde concentrar inversión y expansión de catálogo.
- **Contenidos:** qué perfiles de títulos optimizan valor estratégico.
- **Marketing:** qué segmentos priorizar en campañas por potencial de tracción.

---

## 7) Diseño e implementación del dashboard interactivo

### 7.1 Estructura funcional
Se propone una arquitectura de 4 páginas:

1. **Vista Ejecutiva**
   - KPIs globales.
   - Evolución anual de títulos.

2. **Catálogo por segmentos**
   - Top géneros.
   - Top países.

3. **Engagement**
   - `popularidad` vs `promedio_votos`.
   - `popularidad` vs `votos`.

4. **Finanzas de películas**
   - `presupuesto` vs `ingresos`.
   - distribución de `roi`.

### 7.2 Interacciones mínimas incorporadas
- Filtros por `tipo`, `anio_estreno`, `pais_principal`, `genero_principal`, `idioma`.
- Segmentación cruzada entre visuales.
- Navegación por páginas/secciones.
- Tooltips para detalle contextual.

---

## 8) Evaluación crítica de la solución

### 8.1 Fortalezas
- Integración y limpieza con trazabilidad técnica.
- Alineación explícita entre objetivos de negocio y visualizaciones.
- Estructura visual orientada a públicos no técnicos.

### 8.2 Limitaciones
- Variables financieras no disponibles para series.
- Cobertura desigual en algunas variables textuales (ej. director en series).
- Riesgo de sobreconteo al analizar coproducciones por país si no se deduplica por `id_muestra`.

### 8.3 Oportunidades de mejora
- Incorporar métricas de consumo real de plataforma (horas vistas, retención).
- Añadir vistas de cohortes temporales y segmentación por mercado.
- Implementar validación con usuarios de negocio (test de usabilidad).

---

## 9) Conclusiones y recomendaciones
1. Consolidar el dashboard como fuente corporativa única de indicadores.
2. Mantener separación metodológica entre métricas de engagement (catálogo total) y financieras (películas válidas).
3. Priorizar decisiones de adquisición y promoción según combinación de volumen, popularidad y valoración.
4. Institucionalizar control de calidad de datos con revisión periódica de logs y reglas.

En síntesis, la solución propuesta fortalece la comunicación analítica y mejora la capacidad de decisión basada en evidencia para StreamView Analytics.

---

## 10) Matriz de cumplimiento de pauta (IE4, IE5, IE6, IE7, IE9, IE10)

| Indicador | Evidencia en la solución | Criterio para 100% |
|---|---|---|
| **IE4** Organización y jerarquía visual | Estructura por bloques, orden de lectura ejecutivo, diseño por páginas de decisión | Jerarquía consistente y foco por objetivo |
| **IE5** Uso de atributos visuales | Color semántico, contraste, tamaño/posición por ranking | Atributos aplicados para comprensión inmediata |
| **IE6** Minimización de carga cognitiva | Pocas visuales por vista, etiquetas claras, filtros globales | Lectura intuitiva con bajo esfuerzo mental |
| **IE7** Selección de gráficos | Barras, líneas y dispersión según tipo de variable | Correspondencia completa dato-gráfico |
| **IE9** Coherencia con audiencia y propósito | Mensajes diferenciados para directivo/táctico, KPIs alineados al negocio | Coherencia total visualización-mensaje-audiencia |
| **IE10** Narrativa visual | Secuencia situación-hallazgo-implicancia-acción | Historia clara, lógica y accionable |

---

## 11) Anexos sugeridos para versión PDF final
- Capturas del dashboard por página.
- Diccionario resumido de variables utilizadas.
- Tabla de KPIs con fórmulas.
- Registro de decisiones de diseño y cambios iterativos.
