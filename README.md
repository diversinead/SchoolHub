# GetClassroomTasks

Scrapes Google Classroom assignments for Dara and Eddie and displays them in a filterable table with Gantt chart.

## Usage

```bash
python classroom_scraper.py dara
python classroom_scraper.py eddie
```
This will scrape fresh data from Google classroom

```bash
python server.py dara
python server.py eddie
```

this will generate the HTML, start a local server, and open the browser automatically.

## Files

### Scripts

| File | Description |
|------|-------------|
| `classroom_scraper.py` | Logs into Google Classroom via Selenium and scrapes assignments into `classroom_data_<student>.json` |
| `create_html.py` | Reads classroom data + manual tasks + saved statuses and generates `assignments_<student>.html` |
| `server.py` | Runs `create_html.py`, serves the HTML at `http://localhost:8080/`, and handles saving/loading task statuses |

### Data Files (`data/`)

| File | Description |
|------|-------------|
| `classroom_data_dara.json` | Scraped assignment data for Dara (written by `classroom_scraper.py`) |
| `classroom_data_eddie.json` | Scraped assignment data for Eddie (written by `classroom_scraper.py`) |
| `manual_tasks_dara.json` | Manually added tasks for Dara (e.g. weekly Education Perfect due dates) |
| `manual_tasks_eddie.json` | Manually added tasks for Eddie |
| `assignment_status_dara.json` | Persisted task statuses for Dara (Not Started / In Progress / Completed) |
| `assignment_status_eddie.json` | Persisted task statuses for Eddie |
| `config/config.properties` | Login credentials (not committed to version control) |

### Generated Files

| File | Description |
|------|-------------|
| `assignments_dara.html` | Generated HTML for Dara (do not edit manually) |
| `assignments_eddie.html` | Generated HTML for Eddie (do not edit manually) |
