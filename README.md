# plantilla-corrector-ia


GERARD INSTRUCCIONES: 
📑 Guía para el Estudiante B: Programación del Motor de IA (corregir_con_ia.py)
¡Buenas! Nuestro compañero ya ha dejado lista toda la infraestructura de servidores en GitHub Actions, la seguridad de la API Key y los permisos de escritura del bot. Tu misión ahora es crear el "cerebro" del sistema en Python.

Como GitHub Classroom ya no permite nuevos registros, hemos montado un sistema de "Buzón Automático". Los alumnos subirán sus proyectos dentro de la carpeta entregas/NombreAlumno/ (por ejemplo, su aplicación de Flutter entera). Nuestro script de Python se encargará de escanear esa carpeta, extraer solo el código fuente importante para no saturar los tokens de la IA, contrastarlo con la rúbrica y guardar la nota automáticamente en la carpeta correcciones/.

Sigue estos pasos para dejarlo listo hoy:

Paso 1: Preparar tu entorno local
Para trabajar en este script en tu ordenador antes de subirlo a GitHub, haz lo siguiente en tu terminal:

Clona el repositorio que ha creado nuestro compañero.

Instala la librería oficial de Google para usar la IA (Gemini):

Bash
pip install google-generativeai
(Opcional para probar en local): Si quieres probar el script en tu máquina antes de subirlo, crea una variable de entorno temporal en tu terminal con tu propia clave de Google AI Studio:

En Windows (CMD): set GEMINI_API_KEY=tu_clave_aqui

En Mac/Linux/Git Bash: export GEMINI_API_KEY="tu_clave_aqui"

Paso 2: El código del Script (corregir_con_ia.py)
Abre el archivo corregir_con_ia.py que nuestro compañero dejó creado en la raíz del repositorio y pega el siguiente código. Está preparado específicamente para proyectos de Flutter, buscando de forma inteligente todos los archivos .dart dentro de la carpeta lib/ de cada alumno:

Python
import os
import json
import google.generativeai as genai
from pathlib import Path

# 1. Configurar la API Key de Gemini
# GitHub Actions inyectará esto automáticamente de forma segura
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: No se encontró la variable de entorno GEMINI_API_KEY")
    exit(1)

genai.configure(api_key=api_key)

# Usamos gemini-2.5-flash: es gratuito, ultra rápido y tiene una ventana de contexto enorme
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Leer la rúbrica de evaluación que ha configurado el profesor
try:
    with open("rubrica.json", "r", encoding="utf-8") as f:
        rubrica_contenido = f.read()
    print("✅ Rúbrica cargada correctamente.")
except FileNotFoundError:
    print("⚠️ No se encontró rubrica.json. Se usará una evaluación general.")
    rubrica_contenido = "Evalúa la calidad del código, modularidad, funcionalidad y buenas prácticas."

# Asegurar que la carpeta de correcciones existe en el repositorio
os.makedirs("correcciones", exist_ok=True)

# 3. Buscar las entregas de los alumnos en la carpeta 'entregas'
entregas_path = Path("entregas")
if not entregas_path.exists() or not any(entregas_path.iterdir()):
    print("ℹ️ No hay carpetas de alumnos en 'entregas/' para procesar.")
    exit(0)

# Iterar sobre la carpeta de cada alumno
for alumno_dir in entregas_path.iterdir():
    if alumno_dir.is_dir():
        nombre_alumno = alumno_dir.name
        print(f"\n🔍 Analizando la entrega de: {nombre_alumno}...")

        # Para apps completas (como Flutter), nos enfocamos estrictamente en el código fuente
        # (la carpeta /lib y archivos .dart) para evitar enviarle carpetas basura como /build o .dart_tool
        codigo_completo = ""
        archivos_codigo = list(alumno_dir.glob("lib/**/*.dart")) + list(alumno_dir.glob("*.dart"))

        if not archivos_codigo:
            print(f"⚠️ No se encontraron archivos de código (.dart) para {nombre_alumno}. Saltando...")
            continue

        # Leer y empaquetar el contenido de todos los archivos de código del alumno
        for archivo in archivos_codigo:
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    codigo_completo += f"\n\n--- ARCHIVO: {archivo.relative_to(alumno_dir)} ---\n"
                    codigo_completo += f.read()
            except Exception as e:
                print(f"No se pudo leer el archivo {archivo}: {e}")

        # 4. Diseñar el Prompt para la Inteligencia Artificial
        prompt = f"""
        Actúas como un profesor universitario de programación estricto, justo y meticuloso.
        Tu tarea es evaluar el proyecto de desarrollo de software entregado por el alumno basándote exclusivamente en la siguiente rúbrica de evaluación.

        [RÚBRICA DE EVALUACIÓN]
        {rubrica_contenido}

        [CÓDIGO FUENTE ENVIADO POR EL ALUMNO ({nombre_alumno})]
        {codigo_completo}

        Genera un informe de corrección detallado utilizando formato Markdown (.md). 
        El informe debe estructurarse obligatoriamente de la siguiente manera:
        1. Título principal: 'Informe de Corrección Automática - {nombre_alumno}'
        2. Calificación Final: Muestra la nota claramente (ej: 'Nota Final: 8.5 / 10') calculada según los pesos de la rúbrica.
        3. Desglose detallado de los criterios evaluados.
        4. Aspectos Positivos destacados del código.
        5. Errores detectados y propuestas de mejora específicas (indica qué lógicas o archivos concretos debe cambiar el alumno).

        Sé directo. Devuelve únicamente el texto en formato Markdown listo para guardar, sin introducciones ni comentarios adicionales por tu parte.
        """

        # 5. Enviar los datos a Gemini y recibir la corrección
        try:
            print(f"🤖 Enviando código de {nombre_alumno} a la IA...")
            response = model.generate_content(prompt)
            
            # Limpiar posibles bloques de código markdown sobrantes que añada la API
            texto_limpio = response.text.replace("```markdown", "").replace("```", "").strip()

            # 6. Guardar el archivo final en la carpeta de correcciones
            archivo_nota = Path("correcciones") / f"{nombre_alumno}_nota.md"
            with open(archivo_nota, "w", encoding="utf-8") as f:
                f.write(texto_limpio)
            
            print(f"✅ ¡Corrección generada con éxito para {nombre_alumno}!")
            print(f"📁 Archivo guardado en: {archivo_nota}")

        except Exception as e:
            print(f"❌ Error al procesar la solicitud con la IA para {nombre_alumno}: {e}")

print("\n🚀 Proceso de corrección finalizado.")
Paso 3: Cómo probar que todo funcione bien antes de mañana
Para aseguraros el 10 delante del profesor, haced esta simulación juntos en vuestro ordenador:

Modifica el archivo rubrica.json de la raíz si quieres ajustar los criterios que leerá la IA.

Crea una carpeta de prueba simulando a un estudiante. Por ejemplo: entregas/Eric_Lopez/lib/ y mete ahí dentro un par de archivos .dart reales de vuestros proyectos (puedes meter uno que esté impecable y otro que tenga código sucio o mal estructurado).

Haz un git commit y un git push de tu script de Python hacia la rama principal (main o master).

Entra en la web de vuestro repositorio en GitHub y haz clic en la pestaña Actions. Verás que el servidor se enciende solo.

Espera un par de minutos a que termine. Si todo ha ido bien, vuelve a la pestaña Code de vuestro repositorio. ¡Verás que de forma mágica habrá aparecido una carpeta llamada correcciones/ y dentro estará el archivo Eric_Lopez_nota.md con todo el feedback detallado que ha redactado la IA!
