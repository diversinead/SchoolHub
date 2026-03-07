import json
import webbrowser
import os
from datetime import datetime, timedelta

with open('classroom_data.json', 'r') as f:
    data = json.load(f)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Dara's Assignments - Gantt Chart</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #1a73e8; text-align: center; }
        .controls { background: white; padding: 20px; margin: 20px auto; max-width: 1400px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .subject-checkboxes { display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px; }
        .subject-checkbox { padding: 8px 12px; background: #f0f0f0; border-radius: 4px; }
        .gantt-container { background: white; margin: 20px auto; max-width: 1400px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow-x: auto; }
        .gantt-chart { min-width: 1200px; }
        .legend { display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px; }
        .legend-item { display: flex; align-items: center; gap: 8px; }
        .legend-color { width: 20px; height: 20px; border-radius: 3px; }
        .gantt-row { display: flex; align-items: center; margin: 8px 0; min-height: 40px; }
        .task-label { width: 300px; padding: 8px; font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .task-subject { font-weight: bold; font-size: 11px; }
        .timeline { flex: 1; position: relative; height: 30px; }
        .task-bar { position: absolute; height: 24px; border-radius: 4px; padding: 4px 8px; color: white; font-size: 11px; white-space: nowrap; overflow: hidden; }
        .date-labels { display: flex; margin-left: 300px; margin-bottom: 10px; }
        .date-label { flex: 1; text-align: center; font-size: 12px; color: #666; }
        button { padding: 10px 20px; background: #1a73e8; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        button:hover { background: #1557b0; }
    </style>
</head>
<body>
    <h1>📊 Gantt Chart View</h1>
    <div class="controls">
        <button onclick="window.location.href='assignments.html'">← Back to Table View</button>
        <h3>Select Subjects to Display:</h3>
        <div class="subject-checkboxes" id="subjectCheckboxes"></div>
    </div>
    <div class="gantt-container">
        <div id="ganttChart" class="gantt-chart"></div>
    </div>
    <script>
        const allData = """ + json.dumps(data) + """;
        
        // Color palette for subjects
        const colors = ['#1a73e8', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#00bcd4', '#009688', '#4caf50', '#ff9800', '#ff5722', '#795548', '#607d8b'];
        const subjectColors = {};
        
        // Parse dates and prepare data
        function parseDueDate(dueStr) {
            const match = dueStr.match(/(\\d{1,2})\\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/i);
            if (match) {
                const day = parseInt(match[1]);
                const monthMap = {Jan:0, Feb:1, Mar:2, Apr:3, May:4, Jun:5, Jul:6, Aug:7, Sep:8, Oct:9, Nov:10, Dec:11};
                const month = monthMap[match[2]];
                const year = new Date().getFullYear();
                return new Date(year, month, day);
            }
            return null;
        }
        
        // Create subject checkboxes
        const subjects = new Set();
        allData.forEach(course => {
            if (course.assignments.length > 0) {
                subjects.add(course.course.name);
            }
        });
        
        // Assign colors to subjects
        Array.from(subjects).sort().forEach((subject, index) => {
            subjectColors[subject] = colors[index % colors.length];
        });
        
        const checkboxContainer = document.getElementById('subjectCheckboxes');
        Array.from(subjects).sort().forEach(subject => {
            const label = document.createElement('label');
            label.className = 'subject-checkbox';
            label.innerHTML = `<input type="checkbox" value="${subject}" checked onchange="updateGantt()"> ${subject}`;
            checkboxContainer.appendChild(label);
        });
        
        function updateGantt() {
            const selectedSubjects = Array.from(document.querySelectorAll('.subject-checkbox input:checked')).map(cb => cb.value);
            
            // Collect all tasks from selected subjects
            const tasks = [];
            allData.forEach(course => {
                if (selectedSubjects.includes(course.course.name)) {
                    course.assignments.forEach(assignment => {
                        const dueDate = parseDueDate(assignment.due);
                        if (dueDate) {
                            tasks.push({
                                subject: course.course.name,
                                title: assignment.title,
                                due: dueDate,
                                dueStr: assignment.due
                            });
                        }
                    });
                }
            });
            
            if (tasks.length === 0) {
                document.getElementById('ganttChart').innerHTML = '<p style="text-align:center;color:#999;">No tasks with valid dates found for selected subjects.</p>';
                return;
            }
            
            // Sort by due date
            tasks.sort((a, b) => a.due - b.due);
            
            // Calculate date range
            const minDate = new Date(Math.min(...tasks.map(t => t.due)));
            const maxDate = new Date(Math.max(...tasks.map(t => t.due)));
            const daysDiff = Math.ceil((maxDate - minDate) / (1000 * 60 * 60 * 24)) + 1;
            
            // Generate date labels
            let dateLabelsHtml = '<div class="date-labels">';
            const numLabels = Math.min(10, daysDiff);
            for (let i = 0; i < numLabels; i++) {
                const date = new Date(minDate);
                date.setDate(date.getDate() + Math.floor(i * daysDiff / numLabels));
                dateLabelsHtml += `<div class="date-label">${date.getDate()} ${date.toLocaleString('default', {month: 'short'})}</div>`;
            }
            dateLabelsHtml += '</div>';
            
            // Generate legend
            let legendHtml = '<div class="legend">';
            selectedSubjects.forEach(subject => {
                legendHtml += `<div class="legend-item"><div class="legend-color" style="background: ${subjectColors[subject]}"></div><span>${subject}</span></div>`;
            });
            legendHtml += '</div>';
            
            // Generate gantt rows
            let ganttHtml = legendHtml + dateLabelsHtml;
            tasks.forEach(task => {
                const position = ((task.due - minDate) / (maxDate - minDate)) * 100;
                const color = subjectColors[task.subject];
                ganttHtml += `
                    <div class="gantt-row">
                        <div class="task-label">
                            <div class="task-subject" style="color: ${color}">${task.subject}</div>
                            <div>${task.title}</div>
                        </div>
                        <div class="timeline">
                            <div class="task-bar" style="left: ${position}%; width: 3%; background: ${color};" title="${task.dueStr}">
                                ${task.due.getDate()} ${task.due.toLocaleString('default', {month: 'short'})}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            document.getElementById('ganttChart').innerHTML = ganttHtml;
        }
        
        // Initial render
        updateGantt();
    </script>
</body>
</html>
"""

with open('gantt.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Opening gantt.html in browser...")
webbrowser.open('file://' + os.path.abspath('gantt.html'))
