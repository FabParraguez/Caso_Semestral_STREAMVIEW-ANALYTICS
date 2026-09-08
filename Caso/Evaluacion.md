EVALUACIÓN 1 (EP1) – VISUALIZACIÓN DE DATOS
CASO: STREAMVIEW ANALYTICS
caso-semestral-streamview-analytics
Ejemplo de flujo de trabajo – Público objetivo: Gerente de Contenidos

Público objetivo: Gerente de Contenidos
Necesita información clara para decidir qué contenidos adquirir, producir y promocionar.

Objetivo del análisis: Entregar una visión accionable sobre el desempeño del catálogo para apoyar decisiones de adquisición, producción y promoción de contenidos.

1. Entender el negocio

Reunión con el Gerente de Contenidos para comprender sus desafíos, decisiones y KPIs clave.

Preguntas clave:

¿Qué contenidos generan mayor impacto?
¿Qué géneros o países conviene priorizar?
¿Qué duración es más atractiva para la audiencia?
¿Qué contenidos conviene adquirir o producir?

Resultado: Definición de objetivos y KPIs del análisis.

2. Preparar los datos

Integración y limpieza de los datasets de Películas y Series.

Incluye:

Unificación de formatos
Manejo de valores faltantes
Estandarización de países, géneros e idiomas
Cálculo de métricas derivadas

Resultado: Datos confiables y listos para analizar.

3. Explorar y analizar

Análisis exploratorio para descubrir patrones, tendencias y oportunidades.

Ejemplos de análisis:

Desempeño por género
Ingresos vs. rating
Contenidos por país
Duración vs. popularidad
Clasificación por edad
Evolución en el tiempo

Resultado: Hallazgos clave que responden las preguntas del negocio.

4. Diseñar la visualización

Diseño de un dashboard interactivo y claro, centrado en las decisiones del gerente.

Principios aplicados:

Simplicidad
Enfoque en lo importante
Jerarquía visual
Consistencia de colores
Interactividad
Contexto y storytelling

Resultado: Dashboard entendible, atractivo y enfocado en decisiones.

5. Construir el dashboard

Desarrollo del dashboard en Power BI / Tableau / Excel (según herramienta definida).

Elementos del dashboard:

KPIs principales
Gráficos comparativos
Mapas y distribuciones
Filtros interactivos
Narrativa visual

Resultado: Dashboard funcional e interactivo.

6. Interpretar y comunicar

Generar insights y contar la historia de los datos con claridad y foco en el negocio.

Storytelling:

¿Qué está pasando?
¿Por qué ocurre?
¿Qué implica para el negocio?
¿Qué recomendamos hacer?

Resultado: Historia clara que conecta datos con decisiones.

7. Recomendar y tomar decisiones

Entregar recomendaciones concretas y medibles para apoyar la estrategia de contenidos.

Decisiones posibles:

Adquirir más contenidos de Acción y Comedia
Priorizar producciones de Reino Unido y EE.UU.
Promover contenidos de 90–120 minutos

Resultado: Decisiones informadas que generan impacto en el negocio.

Aún le faltan:

- mejor narrativa ejecutiva,
- más recomendaciones de negocio,
- una redacción más clara en el storytelling,
- un ajuste final de diseño para que se vea más “decisión” y menos “análisis técnico”.

## ⚠️ Lo que aún necesita mejora

### 1) La parte narrativa no está fuerte todavía

El dashboard cumple la parte visual, pero aún le falta una historia ejecutiva clara:

- ¿qué está pasando?
- ¿por qué importa?
- ¿qué recomendación se extrae?
- ¿qué decisión de negocio se toma?

Eso se pide explícitamente en `Descripcion_Caso_Completo.md` y en `EvaluacionParcial1.md`.

### 2) Hay riesgo de interpretación errónea en agregados

Los ETL ya dejan advertencias importantes sobre:

- duplicación por país,
- columnas no confiables,
- conteos por país que pueden inflarse si no se deduplica por id.

Eso es correcto y demuestra rigor, pero en la visualización hay que tener mucho cuidado con:

- sumar por país sin usar la dimensión correcta,
- comparar métricas financieras sin filtrar por película válida.

### 3) El gráfico “plano” no es un error real

La caída final no es un fallo de la base. La evidencia indica que:

- los datos están casi estables año a año,
- 2025 aparece menor porque probablemente es un año incompleto o con cobertura parcial.

Eso no invalida el proyecto; solo hay que interpretarlo bien.

### 4) Falta un mensaje de negocio más claro

El dashboard se ve bien, pero aún parece más técnico que ejecutivo.
Falta una capa final de storytelling para resumir:

- géneros más relevantes,
- países estratégicos,
- oportunidades de adquisición,
- recomendaciones concretas.

