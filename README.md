# prueba_tecnica_hb

### tecnologias a utilizar

- Python
- http
- urllib
- json
- requests
- pydantic
- python-dotenv
- pytest
- git


### Abordaje del problema

1.  **Configuración Inicial:**
    *   Creación de la estructura del proyecto.
    *   Configuración del entorno virtual y dependencias iniciales.

2.  **Microservicio de Consulta de Inmuebles (Práctico):**
    *   **Conexión a BD:** Establecer la conexión a la base de datos proporcionada.
    *   **Modelos de Datos:** Definir modelos para las tablas relevantes (`property`, `status_history`, ) y modelos Pydantic para la validación y serialización de datos en la API.
    *   **Lógica de Consulta:** Implementar la lógica para:
        *   Obtener el estado actual de un inmueble a partir de `status_history`.
        *   Aplicar los filtros solicitados (estado, año de construcción, ciudad, estado).
        *   Manejar la aplicación de múltiples filtros simultáneamente.
    *   **Endpoints API:** Crear los endpoints REST necesarios.
    *   **JSON de Ejemplo:** Se creará un archivo `filter_example.json` para ilustrar cómo se esperan los filtros desde el frontend (probablemente como query parameters).
    *   **Pruebas Unitarias:** Desarrollar pruebas para validar la funcionalidad de los endpoints y la lógica de filtrado.


