# School Hub – Albert Park College 2026

A local web app for tracking **assessments** and **assignments** for Eddie (Year 11) and Dara (Year 7).

---

## Quick Start

```bash
python start.py
```

This starts both servers and opens `launcher.html` in your browser. From the launcher you can navigate to any section.

---

## Project Structure

```
├── Assessments/              # Assessment dates system
├── Assignments/              # Assignments tracking system
├── ClassroomScraper/         # Legacy Google Classroom scraper (kept for reference)
├── launcher.html             # Main entry point (open this in a browser)
└── start.py                  # Starts both servers and opens the launcher
```

---

## Assessments

Tracks scheduled assessment dates by term and week for both students.

**Server:** `python Assessments/assessments_server.py` → [http://localhost:8081](http://localhost:8081)

| URL | Page |
|-----|------|
| `http://localhost:8081/` | View assessments table |
| `http://localhost:8081/admin` | Add / delete assessments |

### View page (`assessments.html`)
- Filter by **All / Eddie only / Dara only**
- Switch between **Term 1 – 4**
- Eddie's assessments shown in **teal**, Dara's in **blue**

### Admin page (`admin.html`)
- Select student, term, and week (dates auto-fill from known term calendar)
- Type the assessment name and click **Add**
- Right panel shows all current assessments — tick/untick terms and weeks to collapse them, click **✕** to delete

### Data file (`Assessments/assessments_data.json`)
All assessment data is stored here. Structure:
```json
{
  "eddie": { "1": [ {"week": 5, "date": "23–27 Feb", "assessments": ["..."]} ], "2": [...], "3": [...], "4": [...] },
  "dara":  { "1": [...], "2": [...], "3": [...], "4": [...] }
}
```

---

## Assignments

Tracks individual assignments (homework, tasks, projects) for both students.

**Server:** `python Assignments/assignments_server.py` → [http://localhost:8082](http://localhost:8082)

| URL | Page |
|-----|------|
| `http://localhost:8082/` | View assignments table |
| `http://localhost:8082/admin` | Add / delete assignments |

### View page (`assignments.html`)
- Filter by student, term, week, subject, and status
- Sort by any column
- Update **status** (Not Started / In Progress / Completed) inline — saves automatically

### Admin page (`admin.html`)
- Select student → subject dropdown updates to that student's subjects
- Fill in title, due date, term, week, and starting status
- Right panel lists all assignments — update status or delete with **✕**

### Data file (`Assignments/assignments_data.json`)
```json
{
  "next_id": 5,
  "eddie": [
    {"id": 1, "subject": "English", "title": "Essay draft", "due": "Mar 27", "term": 1, "week": 9, "status": "In Progress"}
  ],
  "dara": []
}
```

### Known subjects
| Eddie (Year 11) | Dara (Year 7) |
|-----------------|---------------|
| Accounting, Business Mgt, English, Maths, Physical Education, Pos Ed, Sociology | Digital Art, English, Food, French, Humanities, Leadership, Maths, Philosophy, Pos Ed, Science, Volleyball |

---

## Term Calendar

| Term | Dates |
|------|-------|
| Term 1 | 27 Jan – 2 Apr 2026 |
| Term 2 | 20 Apr – 26 Jun 2026 |
| Term 3 | 13 Jul – 18 Sep 2026 |
| Term 4 | 5 Oct – onwards |

---

## ClassroomScraper (Legacy)

The original system that scraped assignments directly from Google Classroom via Selenium. Kept in `ClassroomScraper/` in case it's needed again.

```bash
# Scrape fresh data from Google Classroom
python ClassroomScraper/classroom_scraper.py eddie
python ClassroomScraper/classroom_scraper.py dara

# Generate HTML and serve it
python ClassroomScraper/server.py eddie
python ClassroomScraper/server.py dara
```

| File | Description |
|------|-------------|
| `classroom_scraper.py` | Logs into Google Classroom via Selenium, scrapes assignments |
| `create_html.py` | Generates `assignments_<student>.html` from scraped + manual data |
| `server.py` | Serves the generated HTML at `http://localhost:8080/` |
| `data/classroom_data_*.json` | Scraped assignment data |
| `data/manual_tasks_*.json` | Manually added tasks |
| `data/assignment_status_*.json` | Persisted task statuses |
| `config/config.properties` | Login credentials (not committed to git) |
