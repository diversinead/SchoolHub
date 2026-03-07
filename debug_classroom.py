from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

EMAIL = "daracullinan@albertparkcollege.vic.edu.au"
PASSWORD = "APc34583"

def setup_driver():
    options = Options()
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
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login_google(driver, email, password):
    driver.get("https://accounts.google.com/")
    time.sleep(2)
    
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    email_field.send_keys(email)
    driver.find_element(By.ID, "identifierNext").click()
    time.sleep(2)
    
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Passwd"))
    )
    password_field.send_keys(password)
    driver.find_element(By.ID, "passwordNext").click()
    time.sleep(5)
    
    driver.get("https://classroom.google.com/u/0/h")
    time.sleep(5)  # Wait longer for dynamic content
    
    # Handle Chrome sync popup
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if "without" in button.text.lower():
                button.click()
                time.sleep(2)
                break
    except:
        pass
    
    time.sleep(3)

def debug_page(driver):
    print("\n=== DEBUGGING PAGE STRUCTURE ===\n")
    print(f"Current URL: {driver.current_url}\n")
    
    # Wait longer for dynamic content to load
    print("Waiting for courses to fully load...")
    time.sleep(5)
    
    # Save page source
    with open('classroom_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Page source saved to classroom_page.html\n")
    
    # Use JavaScript to extract course data
    print("Extracting course data via JavaScript...\n")
    
    script = """
    const courses = [];
    const links = document.querySelectorAll('a[href*="/c/"]');
    links.forEach(link => {
        const dataId = link.getAttribute('data-id');
        if (dataId && dataId !== '_gd') {
            const allText = link.innerText || link.textContent;
            const h2 = link.querySelector('h2');
            const divs = link.querySelectorAll('div');
            const spans = link.querySelectorAll('span');
            
            courses.push({
                id: dataId,
                href: link.href,
                allText: allText,
                h2Text: h2 ? h2.innerText : '',
                divTexts: Array.from(divs).map(d => d.innerText).filter(t => t),
                spanTexts: Array.from(spans).map(s => s.innerText).filter(t => t)
            });
        }
    });
    return courses;
    """
    
    courses_data = driver.execute_script(script)
    
    print(f"Found {len(courses_data)} courses:\n")
    
    for i, course in enumerate(courses_data[:10]):
        print(f"\n--- Course {i+1} ---")
        print(f"ID: {course['id']}")
        print(f"All text: '{course['allText']}'")
        print(f"H2 text: '{course['h2Text']}'")
        if course['divTexts']:
            print(f"Div texts: {course['divTexts'][:5]}")
        if course['spanTexts']:
            print(f"Span texts: {course['spanTexts'][:5]}")
    
    print("\n\nLeaving browser open for manual inspection...")
    print("Check the browser window to see the courses.")
    input("Press Enter to close...")

driver = setup_driver()
try:
    login_google(driver, EMAIL, PASSWORD)
    debug_page(driver)
except KeyboardInterrupt:
    print("\nInterrupted by user")
finally:
    driver.quit()
