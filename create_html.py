import json
import webbrowser
import os
from datetime import datetime

# School term dates
term_dates = {
    'Term 1': [
        ('2026-01-27', '2026-02-02', 1), ('2026-02-02', '2026-02-09', 2), ('2026-02-09', '2026-02-16', 3),
        ('2026-02-16', '2026-02-23', 4), ('2026-02-23', '2026-03-02', 5), ('2026-03-02', '2026-03-09', 6),
        ('2026-03-09', '2026-03-16', 7), ('2026-03-16', '2026-03-23', 8), ('2026-03-23', '2026-03-30', 9),
        ('2026-03-30', '2026-04-02', 10)
    ],
    'Term 2': [
        ('2026-04-20', '2026-04-26', 1), ('2026-04-26', '2026-05-03', 2), ('2026-05-03', '2026-05-10', 3),
        ('2026-05-10', '2026-05-17', 4), ('2026-05-17', '2026-05-24', 5), ('2026-05-24', '2026-05-31', 6),
        ('2026-05-31', '2026-06-07', 7), ('2026-06-07', '2026-06-14', 8), ('2026-06-14', '2026-06-21', 9),
        ('2026-06-21', '2026-06-26', 10)
    ],
    'Term 3': [
        ('2026-07-13', '2026-07-19', 1), ('2026-07-19', '2026-07-26', 2), ('2026-07-26', '2026-08-02', 3),
        ('2026-08-02', '2026-08-09', 4), ('2026-08-09', '2026-08-16', 5), ('2026-08-16', '2026-08-23', 6),
        ('2026-08-23', '2026-08-30', 7), ('2026-08-30', '2026-09-06', 8), ('2026-09-06', '2026-09-13', 9),
        ('2026-09-13', '2026-09-18', 10)
    ],
    'Term 4': [
        ('2026-10-05', '2026-10-11', 1), ('2026-10-11', '2026-10-18', 2), ('2026-10-18', '2026-10-25', 3),
        ('2026-10-25', '2026-11-01', 4), ('2026-11-01', '2026-11-08', 5), ('2026-11-08', '2026-11-15', 6),
        ('2026-11-15', '2026-11-22', 7), ('2026-11-22', '2026-11-29', 8), ('2026-11-29', '2026-12-06', 9),
        ('2026-12-06', '2026-12-13', 10), ('2026-12-13', '2026-12-18', 11)
    ]
}

def get_term_week(date_str):
    try:
        # Parse date from strings like "Due 4 Mar"
        match = date_str.replace('Due ', '').strip()
        for term, weeks in term_dates.items():
            for start, end, week_num in weeks:
                start_date = datetime.strptime(start, '%Y-%m-%d')
                end_date = datetime.strptime(end, '%Y-%m-%d')
                # Try to parse the assignment date
                try:
                    parts = match.split()
                    if len(parts) >= 2:
                        day = int(parts[0])
                        month_map = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
                        month = month_map.get(parts[1], 0)
                        if month:
                            assign_date = datetime(2026, month, day)
                            if start_date <= assign_date <= end_date:
                                return term, week_num
                except:
                    pass
    except:
        pass
    return '', ''

# Load existing status data if it exists
try:
    with open('assignment_status.json', 'r') as f:
        status_data = json.load(f)
except FileNotFoundError:
    status_data = {}

with open('classroom_data.json', 'r') as f:
    data = json.load(f)

# Build table rows
subjects = set()
table_rows = ""
for course_data in data:
    course = course_data['course']
    assignments = course_data['assignments']
    
    if assignments:
        subjects.add(course['name'])
        for assignment in assignments:
            task_key = f"{course['name']}||{assignment['title']}"
            current_status = status_data.get(task_key, 'Not Started')
            
            table_rows += f'<tr>\n'
            table_rows += f'  <td class="subject">{course["name"]}</td>\n'
            table_rows += f'  <td>{assignment["title"]}</td>\n'
            table_rows += f'  <td>{assignment["due"]}</td>\n'
            term, week = get_term_week(assignment["due"])
            table_rows += f'  <td>{term}</td>\n'
            table_rows += f'  <td>Week {week}</td>\n'
            table_rows += f'  <td><select class="status-select" data-key="{task_key}" onchange="saveStatus(this)">\n'
            for status in ['Not Started', 'In Progress', 'Completed']:
                selected = 'selected' if status == current_status else ''
                table_rows += f'    <option value="{status}" {selected}>{status}</option>\n'
            table_rows += f'  </select></td>\n'
            table_rows += f'</tr>\n'

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Dara's Assignments</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #1a73e8; text-align: center; }
        .tabs { display: flex; justify-content: center; gap: 10px; margin: 20px auto; max-width: 1400px; }
        .tab-button { padding: 12px 24px; background: white; border: 2px solid #1a73e8; color: #1a73e8; border-radius: 4px; cursor: pointer; font-size: 16px; }
        .tab-button.active { background: #1a73e8; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .filters { background: white; padding: 20px; margin: 20px auto; max-width: 1400px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        input, select { padding: 8px; margin: 5px; font-size: 14px; border: 1px solid #ddd; border-radius: 4px; }
        table { width: 100%; max-width: 1400px; margin: 20px auto; background: white; border-collapse: collapse; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        th { background: #1a73e8; color: white; padding: 12px; text-align: left; cursor: pointer; }
        th:hover { background: #1557b0; }
        td { padding: 12px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f8f9fa; }
        .subject { font-weight: bold; color: #1a73e8; }
        .status-select { padding: 6px; border: 1px solid #ddd; border-radius: 4px; }
        .subject-checkboxes { display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px; }
        .subject-checkbox { padding: 8px 12px; background: #f0f0f0; border-radius: 4px; }
        .gantt-container { background: white; margin: 20px auto; max-width: 1400px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow-x: auto; }
        .gantt-chart { min-width: 1200px; }
        .legend { display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px; }
        .legend-item { display: flex; align-items: center; gap: 8px; }
        .legend-color { width: 20px; height: 20px; border-radius: 3px; }
        .gantt-row { display: flex; align-items: center; margin: 8px 0; min-height: 40px; }
        .task-label { width: 400px; padding: 8px; font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .task-subject { font-weight: bold; font-size: 11px; }
        .timeline { flex: 1; position: relative; height: 30px; }
        .task-bar { position: absolute; height: 24px; border-radius: 4px; padding: 4px 8px; color: white; font-size: 11px; white-space: nowrap; overflow: hidden; }
        .date-labels { display: flex; margin-left: 400px; margin-bottom: 5px; }
        .date-label { flex: 1; text-align: center; font-size: 12px; color: #666; }
        .term-labels { display: flex; margin-left: 400px; margin-bottom: 2px; font-weight: bold; }
        .term-label { text-align: center; font-size: 12px; color: #1a73e8; border-right: 1px solid #ddd; }
        .week-labels { display: flex; margin-left: 400px; margin-bottom: 5px; }
        .week-label { flex: 1; text-align: center; font-size: 11px; color: #666; font-weight: bold; }
    </style>
</head>
<body>
    <h1>📚 Dara's Assignments</h1>
    
    <div class="filters">
        <input type="text" id="searchBox" placeholder="Search assignments..." onkeyup="applyFilters()">
        <div class="subject-checkboxes" id="subjectCheckboxes"></div>
        <select id="weekFilter" onchange="applyFilters()">
            <option value="">All Weeks</option>
        </select>
        <label style="margin-left: 20px;">
            <input type="checkbox" id="hideCompleted" onchange="applyFilters()"> Hide Completed
        </label>
    </div>
    
    <div class="gantt-container">
        <div id="ganttChart" class="gantt-chart"></div>
    </div>
    
    <table id="assignmentTable">
        <thead>
            <tr>
                <th onclick="sortTable(0)">Subject</th>
                <th onclick="sortTable(1)">Assignment</th>
                <th onclick="sortTable(2)">Due Date</th>
                <th onclick="sortTable(3)">Term</th>
                <th onclick="sortTable(4)">Week</th>
                <th onclick="sortTable(5)">Status</th>
            </tr>
        </thead>
        <tbody>
""" + table_rows + """
        </tbody>
    </table>
    
    <script>
        const subjects = """ + json.dumps(sorted(list(subjects))) + """;
        const checkboxContainer = document.getElementById('subjectCheckboxes');
        subjects.forEach(s => {
            const label = document.createElement('label');
            label.className = 'subject-checkbox';
            label.innerHTML = `<input type="checkbox" value="${s}" checked onchange="applyFilters()"> ${s}`;
            checkboxContainer.appendChild(label);
        });
        
        // Populate week filter
        const weeks = new Set();
        const rows = document.querySelectorAll('#assignmentTable tbody tr');
        rows.forEach(row => {
            const term = row.cells[3].textContent;
            const week = row.cells[4].textContent;
            if (term && week) weeks.add(`${term} ${week}`);
        });
        const weekFilter = document.getElementById('weekFilter');
        [...weeks].sort((a, b) => {
            const [aTerm, aWeek] = a.split(' Week ');
            const [bTerm, bWeek] = b.split(' Week ');
            const termOrder = {'Term 1': 1, 'Term 2': 2, 'Term 3': 3, 'Term 4': 4};
            if (termOrder[aTerm] !== termOrder[bTerm]) return termOrder[aTerm] - termOrder[bTerm];
            return parseInt(aWeek) - parseInt(bWeek);
        }).forEach(week => {
            const opt = document.createElement('option');
            opt.value = week;
            opt.textContent = week;
            weekFilter.appendChild(opt);
        });
        
        function saveStatus(selectElement) {
            const key = selectElement.getAttribute('data-key');
            const status = selectElement.value;
            
            let statuses = JSON.parse(localStorage.getItem('assignmentStatuses') || '{}');
            statuses[key] = status;
            localStorage.setItem('assignmentStatuses', JSON.stringify(statuses));
            filterTable();
        }
        
        window.onload = function() {
            const statuses = JSON.parse(localStorage.getItem('assignmentStatuses') || '{}');
            document.querySelectorAll('.status-select').forEach(select => {
                const key = select.getAttribute('data-key');
                if (statuses[key]) {
                    select.value = statuses[key];
                }
            });
        };
        
        function applyFilters() {
            filterTable();
            updateGantt();
        }
        
        function filterTable() {
            const search = document.getElementById('searchBox').value.toLowerCase();
            const selectedSubjects = Array.from(document.querySelectorAll('.subject-checkbox input:checked')).map(cb => cb.value);
            const week = document.getElementById('weekFilter').value;
            const hideCompleted = document.getElementById('hideCompleted').checked;
            const table = document.getElementById('assignmentTable');
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                const subjectCell = cells[0].textContent;
                const assignmentCell = cells[1].textContent.toLowerCase();
                const termCell = cells[3].textContent;
                const weekCell = cells[4].textContent;
                const statusSelect = cells[5].querySelector('select');
                const status = statusSelect.value;
                
                const matchesSearch = assignmentCell.includes(search) || subjectCell.toLowerCase().includes(search);
                const matchesSubject = selectedSubjects.includes(subjectCell);
                const matchesWeek = !week || `${termCell} ${weekCell}` === week;
                const matchesStatus = !hideCompleted || status !== 'Completed';
                
                rows[i].style.display = (matchesSearch && matchesSubject && matchesWeek && matchesStatus) ? '' : 'none';
            }
        }
        
        function sortTable(col) {
            const table = document.getElementById('assignmentTable');
            const rows = Array.from(table.rows).slice(1);
            const sorted = rows.sort((a, b) => {
                const aVal = a.cells[col].textContent;
                const bVal = b.cells[col].textContent;
                return aVal.localeCompare(bVal);
            });
            sorted.forEach(row => table.tBodies[0].appendChild(row));
        }
        
        // Gantt chart code
        const allData = """ + json.dumps(data) + """;
        const colors = ['#1a73e8', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#00bcd4', '#009688', '#4caf50', '#ff9800', '#ff5722', '#795548', '#607d8b'];
        const subjectColors = {};
        
        function parseDueDate(dueStr) {
            const match = dueStr.match(/(\\d{1,2})\\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/i);
            if (match) {
                const day = parseInt(match[1]);
                const monthMap = {Jan:0, Feb:1, Mar:2, Apr:3, May:4, Jun:5, Jul:6, Aug:7, Sep:8, Oct:9, Nov:10, Dec:11};
                const month = monthMap[match[2]];
                return new Date(2026, month, day);
            }
            return null;
        }
        
        const ganttSubjects = new Set();
        allData.forEach(course => {
            if (course.assignments.length > 0) {
                ganttSubjects.add(course.course.name);
            }
        });
        
        Array.from(ganttSubjects).sort().forEach((subject, index) => {
            subjectColors[subject] = colors[index % colors.length];
        });
        
        function updateGantt() {
            const selectedWeek = document.getElementById('weekFilter').value;
            const selectedSubjects = Array.from(document.querySelectorAll('.subject-checkbox input:checked')).map(cb => cb.value);
            const hideCompleted = document.getElementById('hideCompleted').checked;
            
            const tasks = [];
            const statuses = JSON.parse(localStorage.getItem('assignmentStatuses') || '{}');
            const termDates = """ + json.dumps(term_dates) + """;
            
            allData.forEach(course => {
                if (selectedSubjects.includes(course.course.name)) {
                    course.assignments.forEach(assignment => {
                        const dueDate = parseDueDate(assignment.due);
                        if (dueDate) {
                            const taskKey = `${course.course.name}||${assignment.title}`;
                            const status = statuses[taskKey] || 'Not Started';
                            
                            if (hideCompleted && status === 'Completed') return;
                            
                            let termWeek = '';
                            const dueStr = assignment.due.replace('Due ', '').trim();
                            const parts = dueStr.split(' ');
                            if (parts.length >= 2) {
                                const day = parseInt(parts[0]);
                                const monthMap = {Jan:0, Feb:1, Mar:2, Apr:3, May:4, Jun:5, Jul:6, Aug:7, Sep:8, Oct:9, Nov:10, Dec:11};
                                const month = monthMap[parts[1]];
                                if (month !== undefined) {
                                    const assignDate = new Date(2026, month, day);
                                    for (const [term, weeks] of Object.entries(termDates)) {
                                        for (const [start, end, weekNum] of weeks) {
                                            const startDate = new Date(start);
                                            const endDate = new Date(end);
                                            if (assignDate >= startDate && assignDate <= endDate) {
                                                termWeek = `${term} Week ${weekNum}`;
                                                break;
                                            }
                                        }
                                        if (termWeek) break;
                                    }
                                }
                            }
                            
                            if (!selectedWeek || termWeek === selectedWeek) {
                                tasks.push({
                                    subject: course.course.name,
                                    title: assignment.title,
                                    due: dueDate,
                                    dueStr: assignment.due,
                                    status: status,
                                    termWeek: termWeek
                                });
                            }
                        }
                    });
                }
            });
            
            if (tasks.length === 0) {
                document.getElementById('ganttChart').innerHTML = '<p style="text-align:center;color:#999;">No tasks with valid dates found for selected subjects.</p>';
                return;
            }
            
            tasks.sort((a, b) => a.due - b.due);
            
            const minDate = new Date(Math.min(...tasks.map(t => t.due)));
            const maxDate = new Date(Math.max(...tasks.map(t => t.due)));
            const daysDiff = Math.ceil((maxDate - minDate) / (1000 * 60 * 60 * 24)) + 1;
            
            const termDates2 = """ + json.dumps(term_dates) + """;
            const labelData = [];
            const numLabels = Math.min(10, daysDiff);
            
            for (let i = 0; i < numLabels; i++) {
                const date = new Date(minDate);
                date.setDate(date.getDate() + Math.floor(i * daysDiff / numLabels));
                
                let term = '';
                let week = '';
                for (const [termName, weeks] of Object.entries(termDates2)) {
                    for (const [start, end, weekNum] of weeks) {
                        const startDate = new Date(start);
                        const endDate = new Date(end);
                        if (date >= startDate && date <= endDate) {
                            term = termName;
                            week = `W${weekNum}`;
                            break;
                        }
                    }
                    if (term) break;
                }
                labelData.push({ date, term, week });
            }
            
            // Build term row (merge consecutive same terms)
            let termLabelsHtml = '<div class="term-labels">';
            let currentTerm = '';
            let termSpan = 0;
            
            for (let i = 0; i < labelData.length; i++) {
                if (labelData[i].term !== currentTerm) {
                    if (currentTerm) {
                        const width = (termSpan / numLabels) * 100;
                        termLabelsHtml += `<div class="term-label" style="width: ${width}%; flex: none;">${currentTerm}</div>`;
                    }
                    currentTerm = labelData[i].term;
                    termSpan = 1;
                } else {
                    termSpan++;
                }
            }
            if (currentTerm) {
                const width = (termSpan / numLabels) * 100;
                termLabelsHtml += `<div class="term-label" style="width: ${width}%; flex: none;">${currentTerm}</div>`;
            }
            termLabelsHtml += '</div>';
            
            // Build week row
            let weekLabelsHtml = '<div class="week-labels">';
            labelData.forEach(item => {
                weekLabelsHtml += `<div class="week-label">${item.week}</div>`;
            });
            weekLabelsHtml += '</div>';
            
            // Build date row
            let dateLabelsHtml = '<div class="date-labels">';
            labelData.forEach(item => {
                dateLabelsHtml += `<div class="date-label">${item.date.getDate()} ${item.date.toLocaleString('default', {month: 'short'})}</div>`;
            });
            dateLabelsHtml += '</div>';
            
            let legendHtml = '<div class="legend">';
            const displayedSubjects = [...new Set(tasks.map(t => t.subject))];
            displayedSubjects.forEach(subject => {
                legendHtml += `<div class="legend-item"><div class="legend-color" style="background: ${subjectColors[subject]}"></div><span>${subject}</span></div>`;
            });
            legendHtml += '</div>';
            
            let ganttHtml = legendHtml + termLabelsHtml + weekLabelsHtml + dateLabelsHtml;
            tasks.forEach(task => {
                const position = ((task.due - minDate) / (maxDate - minDate)) * 100;
                const color = task.status === 'Completed' ? '#999' : subjectColors[task.subject];
                const opacity = task.status === 'Completed' ? '0.5' : '1';
                
                ganttHtml += `
                    <div class="gantt-row">
                        <div class="task-label">
                            <div class="task-subject" style="color: ${color}">${task.subject}</div>
                            <div>${task.title}</div>
                        </div>
                        <div class="timeline">
                            <div class="task-bar" style="left: ${position}%; width: 3%; background: ${color}; opacity: ${opacity};" title="${task.dueStr} - ${task.termWeek}">
                                ${task.due.getDate()} ${task.due.toLocaleString('default', {month: 'short'})}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            document.getElementById('ganttChart').innerHTML = ganttHtml;
        }
        
        updateGantt();
    </script>
</body>
</html>
"""

with open('assignments.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Opening assignments.html in browser...")
webbrowser.open('file://' + os.path.abspath('assignments.html'))
