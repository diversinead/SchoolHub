from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

PORT = 8082
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'assignments_data.json')


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path in ('/', '/assignments', '/assignments.html'):
            self.serve_file('assignments.html', 'text/html')
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

            student = body['student']
            new_id  = data['next_id']
            entry   = {
                'id':      new_id,
                'subject': body['subject'].strip(),
                'title':   body['title'].strip(),
                'due':     body['due'].strip(),
                'term':    int(body['term']),
                'week':    int(body['week']),
                'status':  body.get('status', 'Not Started')
            }
            if not entry['title']:
                self.send_json('{"ok": false, "error": "Empty title"}')
                return

            data[student].append(entry)
            data['next_id'] += 1

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.send_json('{"ok": true}')

        elif self.path == '/api/update_status':
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            assignment_id = int(body['id'])
            new_status    = body['status']
            for student in ('eddie', 'dara'):
                for entry in data[student]:
                    if entry['id'] == assignment_id:
                        entry['status'] = new_status
                        break

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.send_json('{"ok": true}')

        elif self.path == '/api/edit':
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            assignment_id = int(body['id'])
            for student in ('eddie', 'dara'):
                for entry in data[student]:
                    if entry['id'] == assignment_id:
                        if 'subject' in body: entry['subject'] = body['subject'].strip()
                        if 'title' in body:   entry['title'] = body['title'].strip()
                        if 'due' in body:     entry['due'] = body['due'].strip()
                        if 'term' in body:    entry['term'] = int(body['term'])
                        if 'week' in body:    entry['week'] = int(body['week'])
                        if 'status' in body:  entry['status'] = body['status']
                        break

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.send_json('{"ok": true}')

        elif self.path == '/api/delete':
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            assignment_id = int(body['id'])
            student       = body['student']
            data[student] = [e for e in data[student] if e['id'] != assignment_id]

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
        pass


if __name__ == '__main__':
    print(f"Assignments server running at http://localhost:{PORT}/")
    print(f"Admin GUI:   http://localhost:{PORT}/admin")
    print(f"View page:   http://localhost:{PORT}/")
    print("Press Ctrl+C to stop")
    HTTPServer(('localhost', PORT), Handler).serve_forever()
