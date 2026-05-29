🤖 Corrector Automático con IA (AI AutoGrader)

Un prototipo funcional (MVP) diseñado para automatizar la corrección de tareas de programación académica. Utiliza GitHub Actions para la orquestación y el modelo Gemini 2.5 Flash de Google para evaluar el código de los alumnos basándose en una rúbrica dinámica y personalizable.

✨ Características Principales

🎯 Evaluación por Rúbrica: El profesor solo necesita editar un archivo rubrica.json. La IA adaptará su corrección a esos criterios exactos.

📂 Buzón Automático: Los alumnos suben sus proyectos a la carpeta entregas/ y el sistema hace el resto.

📝 Feedback Detallado: Genera automáticamente un informe en Markdown (.md) con la nota final, puntos fuertes y sugerencias de mejora línea a línea.

🚀 Multilenguaje: Capaz de analizar Java, Python, Dart (Flutter) y más, ignorando automáticamente carpetas basura (build/, bin/, etc.) para optimizar el contexto.

💸 Coste Cero: Integrado con la capa para desarrolladores de Google AI Studio.

🛠️ ¿Cómo funciona? (El Flujo)

El sistema funciona de manera 100% autónoma a través de eventos de GitHub:

El alumno entrega: Sube la carpeta con su código fuente a entregas/NombreAlumno/.

El servidor despierta: GitHub Actions detecta el nuevo código (evento Push) y levanta un contenedor Ubuntu.

El motor analiza: Un script en Python lee la rúbrica del profesor, agrupa el código limpio del alumno y se lo envía a Gemini 2.5 a través de su API.

La nota se publica: El bot del sistema recibe el feedback de la IA, crea un archivo con la corrección y lo publica automáticamente en la carpeta correcciones/.

👨‍🏫 Guía Rápida para el Profesor (Cómo probarlo)

Para ver el sistema en acción, solo tienes que seguir estos tres pasos directamente desde esta web de GitHub:

Paso 1: Configurar la Rúbrica (Opcional)

Si quieres cambiar los criterios de evaluación, abre el archivo rubrica.json desde el navegador, haz clic en el icono del lápiz (editar) y cambia los textos o las puntuaciones. Guarda los cambios (Commit).

Paso 2: Simular una Entrega

Ve a la carpeta entregas/.

Crea una nueva carpeta simulando a un alumno (ej: entregas/prueba1/main.java).

Escribe un código rápido (puede estar bien o tener errores a propósito).

Haz clic en Commit changes.

Paso 3: Ver la Magia

Ve a la pestaña Actions de este repositorio. Verás que hay un proceso en ejecución (una rueda amarilla girando).

Espera unos segundos a que termine y se ponga en verde ✅.

Vuelve a la página principal del código y entra en la carpeta correcciones/.

¡Ahí estará el archivo prueba1_nota.md con la nota y el informe detallado generado por la IA!

⚙️ Estructura del Repositorio

📁 plantilla-corrector-ia/
├── 📁 .github/workflows/      # Orquestador de GitHub Actions (correccion_ia.yml)
├── 📁 correcciones/           # Aquí publica el bot las notas finales
├── 📁 entregas/               # Buzón donde los alumnos suben su código
├── 📄 corregir_con_ia.py      # Motor principal (Python + Google GenAI)
├── 📄 rubrica.json            # Criterios de evaluación (Editable por el profesor)
└── 📄 README.md               # Este documento


🔒 Seguridad

La API Key necesaria para contactar con el modelo de lenguaje de Google está almacenada de forma segura en los Secrets de este repositorio (GEMINI_API_KEY). Ningún alumno ni visitante externo tiene acceso a ella.

Proyecto desarrollado por Eric López y [Nombre de tu compañero] para la asignatura de Programación.
