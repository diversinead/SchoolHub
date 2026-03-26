from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import re

from datetime import date

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSESSMENTS_FILE = os.path.join(BASE_DIR, 'Assessments', 'assessments_data.json')
HOMEWORK_FILE = os.path.join(BASE_DIR, 'Homework', 'homework_data.json')
TODOS_FILE = os.path.join(BASE_DIR, 'TodoLists', 'todo_data.json')


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def singular_date(date_str):
    """Convert date range like '23-27 Feb' to singular '23 Feb'."""
    if not date_str:
        return date_str
    if '\u2013' not in date_str and '-' not in date_str:
        return date_str
    m = re.match(r'(\d+)', date_str)
    months = re.findall(r'[A-Z][a-z]{2}', date_str)
    if m and months:
        return f"{m.group(1)} {months[0]}"
    return date_str


def reset_todos_if_new_day(data):
    """Reset all checked states when the date changes."""
    today = date.today().isoformat()
    if data.get('last_reset') != today:
        for student in ('eddie', 'dara'):
            for period in ('morning', 'afterschool', 'bedtime'):
                for item in data.get(student, {}).get(period, []):
                    item['checked'] = False
        data['last_reset'] = today
    return data


def normalize_assessments(data):
    """Convert legacy string assessments to {text, status, due} objects."""
    for student in ('eddie', 'dara'):
        for term in data.get(student, {}):
            for week_entry in data[student][term]:
                week_date = week_entry.get('date', '')
                new_assessments = []
                for a in week_entry.get('assessments', []):
                    if isinstance(a, str):
                        a = {'text': a, 'status': 'Not Started'}
                    if 'due' not in a:
                        a['due'] = singular_date(week_date)
                    if 'notes' not in a:
                        a['notes'] = ''
                    new_assessments.append(a)
                week_entry['assessments'] = new_assessments
    return data


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.serve_file('launcher.html', 'text/html')
        elif self.path in ('/eddie', '/dara'):
            self.serve_file('student.html', 'text/html')
        elif self.path == '/favicon.svg':
            self.serve_file('favicon.svg', 'image/svg+xml')
        elif self.path in ('/apple-touch-icon.png', '/apple-touch-icon-precomposed.png'):
            self.serve_file('apple-touch-icon.png', 'image/png')
        elif self.path == '/api/assessments/data':
            data = read_json(ASSESSMENTS_FILE)
            self.send_json(json.dumps(normalize_assessments(data), ensure_ascii=False))
        elif self.path == '/api/homework/data':
            data = read_json(HOMEWORK_FILE)
            self.send_json(json.dumps(data, ensure_ascii=False))
        elif self.path == '/api/todos/data':
            data = read_json(TODOS_FILE)
            if data.get('last_reset') != date.today().isoformat():
                reset_todos_if_new_day(data)
                write_json(TODOS_FILE, data)
            self.send_json(json.dumps(data, ensure_ascii=False))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))

        # ── Assessment routes ──────────────────────────────────────────────
        if self.path == '/api/assessments/add':
            data = read_json(ASSESSMENTS_FILE)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            date = body['date'].strip()
            text = body['assessment'].strip()

            if not text:
                self.send_json('{"ok": false, "error": "Empty assessment"}')
                return

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            item = {'text': text, 'status': body.get('status', 'Not Started'), 'due': body.get('date', '').strip(), 'notes': '', 'grade': body.get('grade', '')}
            if entry:
                entry['assessments'].append(item)
            else:
                weeks.append({'week': week_n, 'date': date, 'assessments': [item]})
                weeks.sort(key=lambda w: w['week'])

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/edit':
            data = read_json(ASSESSMENTS_FILE)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])
            text = body['assessment'].strip()

            if not text:
                self.send_json('{"ok": false, "error": "Empty assessment"}')
                return

            normalize_assessments(data)
            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'][idx]['text'] = text
                if 'due' in body:
                    entry['assessments'][idx]['due'] = body['due'].strip()
                if 'grade' in body:
                    entry['assessments'][idx]['grade'] = body['grade']

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/update_grade':
            data = read_json(ASSESSMENTS_FILE)
            normalize_assessments(data)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])
            grade = body.get('grade', '')

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'][idx]['grade'] = grade

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/update_status':
            data = read_json(ASSESSMENTS_FILE)
            normalize_assessments(data)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])
            status = body['status']

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'][idx]['status'] = status

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/delete':
            data = read_json(ASSESSMENTS_FILE)
            normalize_assessments(data)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'].pop(idx)
                if not entry['assessments']:
                    data[student][term] = [w for w in weeks if w['week'] != week_n]

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/assessments/update_notes':
            data = read_json(ASSESSMENTS_FILE)
            normalize_assessments(data)

            student = body['student']
            term = str(body['term'])
            week_n = int(body['week'])
            idx = int(body['index'])
            notes = body.get('notes', '')

            weeks = data[student][term]
            entry = next((w for w in weeks if w['week'] == week_n), None)
            if entry and 0 <= idx < len(entry['assessments']):
                entry['assessments'][idx]['notes'] = notes

            write_json(ASSESSMENTS_FILE, data)
            self.send_json('{"ok": true}')

        # ── Homework routes ────────────────────────────────────────────────
        elif self.path == '/api/homework/add':
            data = read_json(HOMEWORK_FILE)

            student = body['student']
            new_id = data['next_id']
            entry = {
                'id': new_id,
                'subject': body['subject'].strip(),
                'title': body['title'].strip(),
                'due': body['due'].strip(),
                'term': int(body['term']),
                'week': int(body['week']),
                'status': body.get('status', 'Not Started'),
                'notes': ''
            }
            if not entry['title']:
                self.send_json('{"ok": false, "error": "Empty title"}')
                return

            data[student].append(entry)
            data['next_id'] += 1

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/homework/edit':
            data = read_json(HOMEWORK_FILE)

            homework_id = int(body['id'])
            for student in ('eddie', 'dara'):
                for entry in data[student]:
                    if entry['id'] == homework_id:
                        if 'subject' in body: entry['subject'] = body['subject'].strip()
                        if 'title' in body:   entry['title'] = body['title'].strip()
                        if 'due' in body:     entry['due'] = body['due'].strip()
                        if 'term' in body:    entry['term'] = int(body['term'])
                        if 'week' in body:    entry['week'] = int(body['week'])
                        if 'status' in body:  entry['status'] = body['status']
                        break

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/homework/update_status':
            data = read_json(HOMEWORK_FILE)

            homework_id = int(body['id'])
            new_status = body['status']
            for student in ('eddie', 'dara'):
                for entry in data[student]:
                    if entry['id'] == homework_id:
                        entry['status'] = new_status
                        break

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/homework/update_notes':
            data = read_json(HOMEWORK_FILE)

            homework_id = int(body['id'])
            notes = body.get('notes', '')
            for s in ('eddie', 'dara'):
                for entry in data[s]:
                    if entry['id'] == homework_id:
                        entry['notes'] = notes
                        break

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/homework/delete':
            data = read_json(HOMEWORK_FILE)

            homework_id = int(body['id'])
            student = body['student']
            data[student] = [e for e in data[student] if e['id'] != homework_id]

            write_json(HOMEWORK_FILE, data)
            self.send_json('{"ok": true}')

        # ── Todo routes ──────────────────────────────────────────────────
        elif self.path == '/api/todos/toggle':
            data = read_json(TODOS_FILE)
            reset_todos_if_new_day(data)

            student = body['student']
            period = body['period']
            idx = int(body['index'])

            items = data.get(student, {}).get(period, [])
            if 0 <= idx < len(items):
                items[idx]['checked'] = not items[idx]['checked']

            write_json(TODOS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/todos/add':
            data = read_json(TODOS_FILE)
            reset_todos_if_new_day(data)

            student = body['student']
            period = body['period']
            text = body['text'].strip()

            if not text:
                self.send_json('{"ok": false, "error": "Empty item"}')
                return

            data[student][period].append({'text': text, 'checked': False})

            write_json(TODOS_FILE, data)
            self.send_json('{"ok": true}')

        elif self.path == '/api/todos/delete':
            data = read_json(TODOS_FILE)

            student = body['student']
            period = body['period']
            idx = int(body['index'])

            items = data.get(student, {}).get(period, [])
            if 0 <= idx < len(items):
                items.pop(idx)

            write_json(TODOS_FILE, data)
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
            ct = content_type if content_type.startswith('image/') else content_type + '; charset=utf-8'
            self.send_header('Content-Type', ct)
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
    # One-time migration: normalize assessments data and persist
    data = read_json(ASSESSMENTS_FILE)
    normalize_assessments(data)
    write_json(ASSESSMENTS_FILE, data)

    print(f"Server running at http://0.0.0.0:{PORT}/")
    print(f"Local: http://localhost:{PORT}/")
    HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
