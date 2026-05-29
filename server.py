import os
import json
import re
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path

PORT = 5000

class AIAutoGraderHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == '/':
            self.serve_file('index.html', 'text/html')
        elif path == '/api/rubrica':
            self.serve_rubrica()
        elif path == '/api/alumnos':
            self.serve_alumnos()
        elif path == '/api/informe':
            self.serve_informe(query)
        else:
            local_path = path.lstrip('/')
            if local_path and os.path.exists(local_path):
                content_type = 'text/plain'
                if local_path.endswith('.html'): content_type = 'text/html'
                elif local_path.endswith('.css'): content_type = 'text/css'
                elif local_path.endswith('.js'): content_type = 'application/javascript'
                elif local_path.endswith('.json'): content_type = 'application/json'
                self.serve_file(local_path, content_type)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not found")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''

        if path == '/api/rubrica':
            self.save_rubrica(post_data)
        elif path == '/api/corregir':
            self.execute_corrector()
        elif path == '/api/git-push':
            self.execute_git_push()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

    def serve_file(self, filename, content_type):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error reading file: {e}".encode('utf-8'))

    def serve_rubrica(self):
        rubrica_path = 'rubrica.json'
        if os.path.exists(rubrica_path):
            self.serve_file(rubrica_path, 'application/json')
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{}')

    def save_rubrica(self, data):
        try:
            payload = json.loads(data.decode('utf-8'))
            with open('rubrica.json', 'w', encoding='utf-8') as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Rúbrica guardada correctamente."}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

    def serve_alumnos(self):
        entregas_path = Path("entregas")
        alumnos_list = []

        if entregas_path.exists():
            for alumno_dir in entregas_path.iterdir():
                if alumno_dir.is_dir():
                    nombre = alumno_dir.name
                    if nombre.startswith('.') or nombre == '__pycache__': continue

                    # Find language
                    language = "Desconocido"
                    for ext in ['*.py', '*.java', '*.dart']:
                        if list(alumno_dir.rglob(ext)):
                            if ext == '*.py': language = "Python"
                            elif ext == '*.java': language = "Java"
                            elif ext == '*.dart': language = "Dart"
                            break
                    
                    # Check modifications
                    mtime = os.path.getmtime(alumno_dir)
                    import datetime
                    fecha_mod = datetime.datetime.fromtimestamp(mtime).strftime('%d/%m/%Y, %H:%M')

                    # Check grade/report in correcciones
                    report_path = Path("correcciones") / f"{nombre}_nota.md"
                    estado = "pendiente"
                    grade = None

                    if report_path.exists():
                        estado = "corregido"
                        try:
                            with open(report_path, "r", encoding="utf-8") as f:
                                report_text = f.read()
                            # Parse grade (e.g. 'Nota Final: 8.5 / 10' or 'Calificación Final: 9.0')
                            match = re.search(r'(?:Nota Final|Calificación Final|Calificación|Nota):\s*([\d\.,]+)', report_text, re.IGNORECASE)
                            if match:
                                grade = float(match.group(1).replace(',', '.'))
                        except Exception as e:
                            print(f"Error parsing grade for {nombre}: {e}")

                    avatar = "".join([part[0].upper() for part in nombre.replace('_', ' ').replace('-', ' ').split() if part])[:2]
                    if not avatar: avatar = nombre[:2].upper()

                    alumnos_list.append({
                        "nombre": nombre.replace('_', ' '),
                        "nombre_raw": nombre,
                        "avatar": avatar,
                        "lenguaje": language,
                        "fecha": fecha_mod,
                        "estado": estado,
                        "nota": grade
                    })

        # Sort list by name
        alumnos_list.sort(key=lambda x: x["nombre"])

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(alumnos_list, ensure_ascii=False).encode('utf-8'))

    def serve_informe(self, query):
        alumno = query.get('alumno', [None])[0]
        if not alumno:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing 'alumno' query parameter")
            return

        report_path = Path("correcciones") / f"{alumno}_nota.md"
        if report_path.exists():
            try:
                with open(report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "report": content}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Informe no encontrado"}).encode('utf-8'))

    def execute_corrector(self):
        try:
            python_executable = sys.executable
            # Execute script and wait for completion
            result = subprocess.run([python_executable, 'corregir_con_ia.py'], capture_output=True, text=True, encoding='utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            if result.returncode == 0:
                self.wfile.write(json.dumps({
                    "status": "success", 
                    "message": "Auditoría completada exitosamente.",
                    "log": result.stdout
                }, ensure_ascii=False).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({
                    "status": "error", 
                    "message": "Error durante la ejecución de la corrección.",
                    "log": result.stderr or result.stdout
                }, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

    def execute_git_push(self):
        try:
            # Add all, commit, push
            subprocess.run(['git', 'add', '.'], capture_output=True)
            commit_res = subprocess.run(['git', 'commit', '-m', 'feat: actualización desde el panel de control del profesor'], capture_output=True, text=True)
            
            # Git push origin main
            push_res = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
            
            log_output = f"=== COMMIT LOG ===\n{commit_res.stdout}\n{commit_res.stderr}\n\n=== PUSH LOG ===\n{push_res.stdout}\n{push_res.stderr}"
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "message": "Sincronización con GitHub completada.",
                "log": log_output
            }, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

def run():
    print(f"Iniciando Servidor Backend para AI Grader en http://localhost:{PORT}")
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, AIAutoGraderHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("\nServidor detenido.")

if __name__ == '__main__':
    run()
