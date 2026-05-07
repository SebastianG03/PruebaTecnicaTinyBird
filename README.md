# Prueba técnica - API de métricas de eventos
Este proyecto expone una API construida con FastAPI para procesar eventos de productos y calcular métricas de negocio como ingresos, tasa de conversión, usuarios únicos y productos más populares.

## Preguntas
1. Cómo modelar en Tinybird
El modelado en Tinybird se base en la estructuración de datos crudos y luego transformarlos para crear vistas materializadas. Los datos provendrán de diferentes fuentes de datos definidas en el proyecto y se procesarán mediante pipes.
2. Qué pipes crear
Para la prueba actual crearía un pipe para filtrar los eventos en base a los filtros definidos, en este caso por código de país y fecha. Además, crearía un pipe para analizar, validar y trasnformar la información de los eventos. 
3. Cómo evitar duplicados
Existen varios métodos para deduplicar, pero considerando que los eventos pueden ser recibidos en masa, eligiría el más eficiente y confiable a largo plazo. Implementaría ReplacingMergeTree para deduplicar y evitar afectar la eficiencia del proceso. También consideraría utilizar funciones lambda en casoo de ser necesario.
4. Cómo escalar 
Antes de escalar, revisaría cuál es el estado actual de la arquitectura y los recursos disponibles. Revisaría los logs, registros y documentación disponibles en los que se detallen el uso periódico de recursos y crearía un plan con el fin de revisar, planificar y optimizar los procesos, modificando la lógica de las querys, generando vistas dónde sea necesario, etc. Después de verificar que no se puede optimizar más el proceso actual escalaría verticalmente ampliando los recursos disponibles.

## Arquitectura del proyecto
La solución está organizada con una arquitectura por capas para separar responsabilidades:

- `main.py`: punto de entrada de la aplicación, configuración de FastAPI, CORS, observabilidad y registro de rutas.
- `app/api/v1/`: capa de presentación (HTTP). Define endpoints y contrato de entrada/salida.
- `app/core/`: capa de negocio. Contiene validación/filtrado de eventos y cálculo de métricas.
- `app/entities/`: capa de dominio. Modelos, tipos e interfaces base.
- `app/config/`: configuración centralizada (Dynaconf).
- `data/`: fuente de datos local en JSON.
- `test/`: pruebas unitarias e integración de API y componentes.

### Flujo principal
1. El cliente invoca `POST /metrics/` con filtros opcionales (`country`, `from_date`, `to_date`).
2. Se cargan eventos desde `data/events.json`, para las pruebas se utiliza `data\test_events.json`.
3. Se validan, depuran duplicados y aplican filtros de país/fechas.
4. Se calculan métricas agregadas en el gestor de métricas.
5. Se responde con un formato unificado (`WebResponse`) y cacheo de respuesta.

## Librerías importantes utilizadas
- **FastAPI**: framework principal para la API REST.
- **Pydantic**: validación fuerte de modelos de entrada y dominio.
- **fastapi-cache2**: cacheo del endpoint de métricas para mejorar rendimiento.
- **logfire**: instrumentación y trazabilidad de errores/eventos de ejecución.
- **pycountry**: validación de códigos ISO de país.
- **Dynaconf**: base para gestión de configuración por entorno.
- **Uvicorn**: servidor ASGI para ejecución local/productiva.
- **Pytest**: framework de pruebas.
- **Ruff**: linting y verificación de formato en CI.

## Patrones de diseño implementados
- **Arquitectura por capas**: separación entre API, lógica de negocio y dominio.
- **Singleton (metaclase)**: `MetricsManager` y validador comparten una única instancia segura en concurrencia.
- **Contrato por interfaz/ABC**: `IEventValidator` define comportamiento común y extensible para validación.
- **DTOs/Modelos de transferencia**: modelos Pydantic (`Events`, `MetricsEntry`, `MetricResponse`) para contratos explícitos y tipados.

## Buenas prácticas implementadas
- **Validaciones de dominio robustas**: reglas de IDs, fechas, precios, tipo de evento y país.
- **Manejo de errores controlado**: respuestas HTTP homogéneas y registro detallado de excepciones.
- **Separación de responsabilidades**: carga de datos, validación y cálculo desacoplados.
- **Tipado estático en firmas**: uso consistente de `typing` para mejorar mantenibilidad.
- **Pruebas automatizadas**:
  - pruebas de API (endpoint de salud y métricas),
  - pruebas de validación,
  - pruebas de cálculo de métricas.
- **Calidad continua en CI**: GitHub Actions ejecuta lint, format-check y test en pushes/PRs.
- **Análisis de seguridad**: escaneo automático con Codacy en la plataforma.
- **Análisis de Gitguardian**: escaneo automático con GitGuardian en cada cambio del proyecto

## Estructura resumida
```text
.
├── app
│   ├── api/v1
│   ├── core
│   ├── entities
│   │   ├── interfaces
│   │   ├── models
│   │   └── types
│   └── config
├── data
├── test
└── .github/workflows
```