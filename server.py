from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import subprocess
import webbrowser

PORT = 8080
student_name = sys.argv[1] if len(sys.argv) > 1 else 'dara'
STATUS_FILE = f'data/assignment_status_{student_name}.json'
HTML_FILE = f'assignments_{student_name}.html'


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', f'/{HTML_FILE}'):
            try:
                with open(HTML_FILE, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()

        elif self.path == '/statuses':
            try:
                with open(STATUS_FILE, 'r') as f:
                    data = f.read()
            except FileNotFoundError:
                data = '{}'
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(data.encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/save_status':
            length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(length))
            try:
                with open(STATUS_FILE, 'r') as f:
                    statuses = json.load(f)
            except FileNotFoundError:
                statuses = {}
            statuses[body['key']] = body['status']
            with open(STATUS_FILE, 'w') as f:
                json.dump(statuses, f, indent=2)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress request logs


if __name__ == '__main__':
    print(f"Generating HTML for {student_name}...")
    subprocess.run([sys.executable, 'create_html.py', student_name, '--no-browser'])

    print(f"Server running at http://localhost:{PORT}/")
    print("Press Ctrl+C to stop")
    webbrowser.open(f'http://localhost:{PORT}/')
    HTTPServer(('localhost', PORT), Handler).serve_forever()
