from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

PORT = 8081
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'assessments_data.json')


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path in ('/', '/assessments', '/assessments.html'):
            self.serve_file('assessments.html', 'text/html')
        elif self.path in ('/admin', '/admin.html'):
            self.serve_file('admin.html', 'text/html')
        elif self.path == '/api/data':
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.send_json(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))

        if self.path == '/api/add':
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            student = body['student']       # 'eddie' or 'dara'
            term    = str(body['term'])     # '1' or '2'
            week_n  = int(body['week'])
            date    = body['date'].strip()
            text    = body['assessment'].strip()

            if not text:
                self.send_json('{"ok": false, "error": "Empty assessment"}')
                return

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry:
                entry['assessments'].append(text)
            else:
                weeks.append({'week': week_n, 'date': date, 'assessments': [text]})
                weeks.sort(key=lambda w: w['week'])

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.send_json('{"ok": true}')

        elif self.path == '/api/edit':
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            student = body['student']
            term    = str(body['term'])
            week_n  = int(body['week'])
            idx     = int(body['index'])
            text    = body['assessment'].strip()

            if not text:
                self.send_json('{"ok": false, "error": "Empty assessment"}')
                return

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'][idx] = text

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.send_json('{"ok": true}')

        elif self.path == '/api/delete':
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            student = body['student']
            term    = str(body['term'])
            week_n  = int(body['week'])
            idx     = int(body['index'])

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'].pop(idx)
                # Remove week entirely if no assessments left
                if not entry['assessments']:
                    data[student][term] = [w for w in weeks if w['week'] != week_n]

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.send_json('{"ok": true}')

        else:
            self.send_response(404)
            self.end_headers()

    def serve_file(self, filename, content_type):
        path = os.path.join(BASE_DIR, filename)
        try:
            with open(path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type + '; charset=utf-8')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def send_json(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        pass  # Suppress request logs


if __name__ == '__main__':
    print(f"Assessments server running at http://localhost:{PORT}/")
    print(f"Admin GUI:   http://localhost:{PORT}/admin")
    print(f"View page:   http://localhost:{PORT}/")
    print("Press Ctrl+C to stop")
    HTTPServer(('localhost', PORT), Handler).serve_forever()
