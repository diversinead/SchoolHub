from selenium import webdriver
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
    options.add_argument('--disable-sync')
    options.add_experimental_option('prefs', {'signin.allowed': False})
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

driver = setup_driver()
driver.get("https://classroom.google.com/u/0/c/841405411064/w/all")  # 7ENG.G course

print("Please log in manually and navigate to the Classwork tab if needed.")
print("Once you're on the Classwork page, press Enter...")
input()

time.sleep(3)

script = """
const data = {
    url: window.location.href,
    pageText: document.body.innerText.substring(0, 1000),
    assignments: []
};

// Look for any divs that might contain assignments
const allDivs = document.querySelectorAll('div');
const assignmentDivs = [];

allDivs.forEach(div => {
    const text = div.innerText;
    // Look for divs that contain "Due" text
    if (text && text.includes('Due') && text.length < 300) {
        assignmentDivs.push({
            text: text,
            classes: div.className,
            parent: div.parentElement ? div.parentElement.className : 'none'
        });
    }
});

data.assignments = assignmentDivs.slice(0, 10);

// Also check for specific patterns
data.itemsWithDataId = document.querySelectorAll('[data-item-id]').length;
data.itemsWithAssignment = document.querySelectorAll('[class*="assignment"]').length;
data.itemsWithWork = document.querySelectorAll('[class*="work"]').length;

return data;
"""

result = driver.execute_script(script)

print("\n=== PAGE INFO ===")
print(f"URL: {result['url']}")
print(f"\nPage text (first 500 chars):\n{result['pageText'][:500]}")

print(f"\n\n=== ELEMENT COUNTS ===")
print(f"Items with [data-item-id]: {result['itemsWithDataId']}")
print(f"Items with 'assignment' in class: {result['itemsWithAssignment']}")
print(f"Items with 'work' in class: {result['itemsWithWork']}")

print(f"\n\n=== DIVS CONTAINING 'Due' ({len(result['assignments'])} found) ===")
for i, item in enumerate(result['assignments']):
    print(f"\n{i+1}. Text: {item['text'][:150]}")
    print(f"   Classes: {item['classes'][:100]}")
    print(f"   Parent: {item['parent'][:100]}")

print("\n\nLeaving browser open. Press Enter to close...")
try:
    input()
except KeyboardInterrupt:
    print("\nClosing...")
finally:
    driver.quit()
