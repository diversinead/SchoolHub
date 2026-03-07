import json
from datetime import datetime

with open('classroom_data.json', 'r') as f:
    data = json.load(f)

print("=" * 60)
print("DARA'S ASSIGNMENTS")
print("=" * 60)

for course_data in data:
    course = course_data['course']
    assignments = course_data['assignments']
    
    if assignments:
        print(f"\n{course['name']}")
        print("-" * 60)
        
        for assignment in assignments:
            print(f"  • {assignment['title']}")
            print(f"    {assignment['due']}")
        
print("\n" + "=" * 60)
