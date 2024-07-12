from objprint import objprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Config
screenshotDir = "Screenshots"
screenWidth = 400
screenHeight = 800

def __wait_for_page_load(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        print("Page has fully loaded.")
    except Exception as e:
        print("Page did not load within the given time.", e)


def __check_and_click_close(driver, wait):
    try:
        iframe_parent = driver.find_element(By.ID, 'credential_picker_container')
        iframe = iframe_parent.find_element(By.TAG_NAME, 'iframe')
        
        driver.switch_to.frame(iframe)
        
        close_button = wait.until(EC.presence_of_element_located((By.ID, 'close')))
        wait.until(EC.element_to_be_clickable((By.ID, 'close'))).click()
        print("Clicked the 'close' button.")
        
        driver.switch_to.default_content()
    except Exception as e:
        print("No 'accept cookies' button found or it could not be clicked.", e)

def getPostScreenshots(filePrefix, script):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)
    __wait_for_page_load(driver)
    __check_and_click_close(driver, wait)
    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait, f"t3_{script.postId}", By.ID)
    for commentFrame in script.frames:
        commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, f"[thingid=t1_{commentFrame.commentId}]", By.CSS_SELECTOR)
    driver.quit()

def __takeScreenshot(filePrefix, driver, wait, handle, method):
    search = wait.until(EC.presence_of_element_located((method, handle)))
    driver.execute_script("window.focus();")

    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName

def __setupDriver(url: str):
    options = webdriver.FirefoxOptions()
    options.headless = False
    options.enable_mobile = False
    options.add_argument('--disable-notifications')
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    driver.set_window_size(width=screenWidth, height=screenHeight)
    driver.get(url)

    return driver, wait