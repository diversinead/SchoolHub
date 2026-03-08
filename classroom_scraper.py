from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import base64
import sys

from jproperties import Properties

# Load properties file
configs = Properties()
with open('config/config.properties', 'rb') as config_file:
    configs.load(config_file)

eddie_password = configs.get("eddie_password").data
dara_password = configs.get("dara_password").data

# Get student name from command line argument
if len(sys.argv) > 1:
    student_name = sys.argv[1]
else:
    student_name = input("Enter student name (e.g., 'dara' or 'eddie'): ").lower()

print(f"\nScraping assignments for {student_name}...")

if student_name == 'dara':
    email = "daracullinan@albertparkcollege.vic.edu.au"
    password = dara_password
else:
    email = "eddiecullinan@albertparkcollege.vic.edu.au"
    password = eddie_password

def setup_driver():
    options = Options()
    # Disable Chrome sync and profile popups
    options.add_argument('--no-first-run')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-sync')
    options.add_argument('--disable-features=ChromeWhatsNewUI')
    options.add_experimental_option('prefs', {
        'profile.default_content_setting_values.notifications': 2,
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'signin.allowed': False
    })
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    # options.add_argument('--headless')  # Uncomment to run without opening browser
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login_google(driver, email, password):
    # Start at Google login page
    driver.get("https://accounts.google.com/")
    time.sleep(2)
    
    try:
        # Try to find email field (multiple possible selectors)
        email_field = None
        for selector in [(By.ID, "identifierId"), (By.NAME, "identifier"), (By.CSS_SELECTOR, "input[type='email']")]:
            try:
                email_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(selector)
                )
                break
            except:
                continue
        
        if not email_field:
            print("Could not find email field. Please log in manually.")
            input("Press Enter after logging in manually...")
            return
        
        email_field.send_keys(email)
        
        # Click next button
        for selector in [(By.ID, "identifierNext"), (By.CSS_SELECTOR, "button[type='button']")]:
            try:
                driver.find_element(*selector).click()
                break
            except:
                continue
        
        time.sleep(2)
        
        # Password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        password_field.send_keys(password)
        
        # Click next/sign in button
        for selector in [(By.ID, "passwordNext"), (By.CSS_SELECTOR, "button[type='button']")]:
            try:
                driver.find_element(*selector).click()
                break
            except:
                continue
        
        time.sleep(5)  # Wait for login to complete
        
        # Now navigate to Classroom
        print("Navigating to Google Classroom...")
        driver.get("https://classroom.google.com/u/0/h")
        time.sleep(3)
        
        # Try to handle "Use Chrome without an account" popup
        try:
            print("Looking for Chrome sync popup...")
            # Try multiple text matches for the button
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                button_text = button.text.lower()
                if "without" in button_text or "no thanks" in button_text or "skip" in button_text:
                    print("Clicking 'Use Chrome without an account' button...")
                    button.click()
                    time.sleep(2)
                    break
        except Exception as e:
            print(f"No sync popup found or already dismissed: {e}")
        
        time.sleep(3)
        
    except Exception as e:
        print(f"Login error: {e}")
        print("Please complete login manually in the browser window.")
        input("Press Enter after logging in manually...")

def get_courses(driver):
    time.sleep(5)
    
    current_url = driver.current_url
    if "classroom.google.com" not in current_url or "/h" not in current_url:
        driver.get("https://classroom.google.com/u/0/h")
        time.sleep(5)
    
    script = """
    const courses = [];
    const seen = new Set();
    const links = document.querySelectorAll('a[href*="/c/"]');
    links.forEach(link => {
        const dataId = link.getAttribute('data-id');
        if (dataId && dataId !== '_gd' && !seen.has(dataId)) {
            seen.add(dataId);
            const courseName = (link.innerText || link.textContent).trim();
            if (courseName) {
                courses.push({id: dataId, name: courseName});
            }
        }
    });
    return courses;
    """
    
    courses = driver.execute_script(script)
    return courses

def get_coursework(driver, course_id):
    # Encode course ID to base64 for URL
    encoded_id = base64.b64encode(course_id.encode()).decode().rstrip('=')
    driver.get(f"https://classroom.google.com/u/0/w/{encoded_id}/t/all")
    time.sleep(4)
    
    script = """
    const assignments = [];
    const seen = new Set();
    const allDivs = document.querySelectorAll('div');
    
    allDivs.forEach(div => {
        const text = div.innerText;
        if (text && text.includes('Due') && text.length < 150 && text.length > 15) {
            const lines = text.trim().split('\\n').filter(l => l.trim());
            
            if (lines.length >= 2) {
                let title = lines[0];
                let dueDate = '';
                
                // Find the line with 'Due'
                for (let line of lines) {
                    if (line.includes('Due')) {
                        dueDate = line;
                        break;
                    }
                }
                
                // Clean up title
                if (title.includes('Assignment') || title.includes('Completed')) {
                    title = lines[1] || title;
                }
                
                title = title.replace('Completed Assignment', '').replace('Assignment', '').trim();
                
                if (title && dueDate && !seen.has(title)) {
                    seen.add(title);
                    assignments.push({title: title, due: dueDate});
                }
            }
        }
    });
    
    return assignments;
    """
    
    return driver.execute_script(script)

def main():
    driver = setup_driver()
    
    try:
        login_google(driver, email, password)
        
        courses = get_courses(driver)
        print(f"\nFound {len(courses)} courses\n")
        
        # Load existing data to preserve statuses
        output_file = f'data/classroom_data_{student_name}.json'
        try:
            with open(output_file, 'r') as f:
                existing_data = {item['course']['id']: item for item in json.load(f)}
        except FileNotFoundError:
            existing_data = {}
        
        EXCLUDED_COURSES = {'LLibrary Space'}
        all_data = []
        for course in courses:
            if course['name'] in EXCLUDED_COURSES:
                continue
            print(f"Course: {course['name']}")
            coursework = get_coursework(driver, course['id'])
            
            # Merge with existing assignments
            if course['id'] in existing_data:
                existing_assignments = {a['title']: a for a in existing_data[course['id']]['assignments']}
                for work in coursework:
                    if work['title'] not in existing_assignments:
                        print(f"  NEW: {work['title']} (Due: {work['due']})")
            
            if coursework:
                print(f"  Total assignments: {len(coursework)}")
            else:
                print("  No assignments")
            print()
            
            all_data.append({"course": course, "assignments": coursework})
        
        with open(output_file, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        print(f"Data saved to {output_file}")
        print("\nGenerating HTML...")
        
    finally:
        driver.quit()
    
    # Auto-run create_html after scraping
    import subprocess
    subprocess.run(['python', 'create_html.py', student_name])

if __name__ == "__main__":
    main()
