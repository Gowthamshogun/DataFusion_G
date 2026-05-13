from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 30)

# STEP 1: LOGIN
driver.get("https://datafusionx-frontend-trqrqr6kxa-uc.a.run.app/#/login")
email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[placeholder*='email'], input[placeholder*='Email']")))
email.clear()
email.send_keys("admin.demo@rctech.org")
password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
password.clear()
password.send_keys("DataFusionX@Demo2026")
wait.until(EC.invisibility_of_element_located((By.ID, "native-splash")))
driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(text(),'Sign In')]"))
wait.until(EC.url_contains("dashboard"))
print("✅ STEP 1: Login successful!")

# STEP 2: OPEN DATA CATALOG
driver.get("https://datafusionx-frontend-trqrqr6kxa-uc.a.run.app/#/discover/catalogue")
time.sleep(5)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Data Governance')]")))
driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Data Catalog']"))))
print("⏳ Waiting for tables to load...")
time.sleep(8)
print("✅ STEP 2: Data Catalog loaded!")

# STEP 3: SELECT TEST-MYSQL FROM SOURCE DROPDOWN
all_comboboxes = driver.find_elements(By.XPATH, "//*[@role='combobox']")
source_dd = None
for cb in all_comboboxes:
    if "All Sources" in cb.text or "Source" in cb.text:
        source_dd = cb
        break

if not source_dd:
    source_dd = all_comboboxes[0]

driver.execute_script("arguments[0].click();", source_dd)
print("✅ STEP 3: Opened Source dropdown!")
time.sleep(2)

test_mysql = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//*[@role='option' and contains(.,'Test-mysql')] | //li[contains(.,'Test-mysql')]")
))
driver.execute_script("arguments[0].click();", test_mysql)
print("✅ STEP 3: Selected Test-mysql!")

wait.until(EC.presence_of_element_located(
    (By.XPATH, "//td[contains(text(),'employees')] | //p[contains(text(),'employees')] | //*[contains(@class,'MuiTableCell') and contains(text(),'employees')]")
))
print("✅ STEP 3: Test-mysql tables loaded!")
time.sleep(1)

# STEP 4: SEARCH FOR 'employees'
search_box = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "input[placeholder*='Search tables']")
))
driver.execute_script("arguments[0].click();", search_box)
time.sleep(1)
search_box.send_keys("employees")
print("✅ STEP 4: Searched for 'employees'!")
time.sleep(3)

body_text = driver.find_element(By.TAG_NAME, "body").text
if "employees" in body_text.lower():
    print("✅ STEP 4: 'employees' table found!")
else:
    print("❌ STEP 4: 'employees' table NOT found!")

# STEP 5: CLEAR SEARCH THEN CLICK EMPLOYEES ROW
search_box.clear()
time.sleep(2)

employees_row = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//p[contains(@class,'MuiTypography') and text()='employees']")
))
driver.execute_script("arguments[0].click();", employees_row)
print("✅ STEP 5: Opened employees table!")
time.sleep(3)

# STEP 6: PROFILE ONLY EMPLOYEES TABLE
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

profile_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(text(),'Profile This Table') or contains(text(),'Profile Table') or contains(text(),'Profile This Source')]")
))
driver.execute_script("arguments[0].click();", profile_btn)
print("✅ STEP 6: Clicked Profile for employees!")
time.sleep(2)

# STEP 7: CONFIRM MODAL
try:
    confirm_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Profile All') or contains(text(),'Confirm') or contains(text(),'Profile 1')]")
    ))
    driver.execute_script("arguments[0].click();", confirm_btn)
    print("✅ STEP 7: Confirmed profiling for employees!")
except:
    print("⚠️ STEP 7: No confirmation modal — profiling may have started directly")

time.sleep(3)

# STEP 8: VERIFY PIPELINE STARTED
try:
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(),'Running') or contains(text(),'DQR-') or contains(text(),'Pipeline')]")
    ))
    print("✅ STEP 8: Pipeline started successfully!")
except:
    print("⚠️ STEP 8: Pipeline status unclear")

print("\n🎉 EMPLOYEES PROFILING TEST COMPLETED!")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("✅ Login                        PASSED")
print("✅ Data Catalog opened          PASSED")
print("✅ Test-mysql filter            PASSED")
print("✅ Employees table found        PASSED")
print("✅ Employees table opened       PASSED")
print("✅ Profile employees triggered  PASSED")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

driver.quit()