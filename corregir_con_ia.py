import os
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: No se encontró la variable de entorno GEMINI_API_KEY")
    exit(1)

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

try:
    with open("rubrica.json", "r", encoding="utf-8") as f:
        rubrica_contenido = f.read()
    print("Rúbrica cargada correctamente.")
except FileNotFoundError:
    print("No se encontró rubrica.json. Se usará una evaluación general.")
    rubrica_contenido = "Evalúa la calidad del código, modularidad, funcionalidad y buenas prácticas."

os.makedirs("correcciones", exist_ok=True)

entregas_path = Path("entregas")
if not entregas_path.exists() or not any(entregas_path.iterdir()):
    print("No hay carpetas de alumnos en 'entregas/' para procesar.")
    exit(0)

for alumno_dir in entregas_path.iterdir():
    if alumno_dir.is_dir():
        nombre_alumno = alumno_dir.name
        print(f"\nAnalizando la entrega de: {nombre_alumno}...")

        extensiones_codigo = ['*.java', '*.dart', '*.py']
        archivos_encontrados = []
        
        for ext in extensiones_codigo:
            archivos_encontrados.extend(alumno_dir.rglob(ext))

        carpetas_ignoradas = ['build', 'bin', 'out', '.dart_tool', '__pycache__', 'venv', '.idea', 'target']
        archivos_codigo = [f for f in archivos_encontrados if not any(ignorado in f.parts for ignorado in carpetas_ignoradas)]

        if not archivos_codigo:
            print(f"No se encontraron archivos de código fuente para {nombre_alumno}. Saltando...")
            continue

        codigo_completo = ""
        for archivo in archivos_codigo:
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    codigo_completo += f"\n\n--- ARCHIVO: {archivo.relative_to(alumno_dir)} ---\n"
                    codigo_completo += f.read()
            except Exception as e:
                print(f"No se pudo leer el archivo {archivo}: {e}")

        prompt = f"""
        Actúas como un profesor universitario de programación estricto, justo y meticuloso.
        Tu tarea es evaluar el proyecto de desarrollo de software entregado por el alumno basándote exclusivamente en la siguiente rúbrica de evaluación.
        El código puede estar en diferentes lenguajes (Java, Python, Dart, etc.). Identifica el lenguaje por la extensión de los archivos proporcionados y aplica las buenas prácticas correspondientes a dicho ecosistema.

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

        try:
            print(f"Enviando código de {nombre_alumno} a la IA...")
            response = model.generate_content(prompt)
            
            texto_limpio = response.text.replace("```markdown", "").replace("```", "").strip()

            archivo_nota = Path("correcciones") / f"{nombre_alumno}_nota.md"
            with open(archivo_nota, "w", encoding="utf-8") as f:
                f.write(texto_limpio)
            
            print(f"¡Corrección generada con éxito para {nombre_alumno}!")
            print(f"Archivo guardado en: {archivo_nota}")

        except Exception as e:
            print(f"Error al procesar la solicitud con la IA para {nombre_alumno}: {e}")

print("\nProceso de corrección finalizado.")