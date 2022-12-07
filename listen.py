import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import json

def get_webdriver():
    """
        Returns a muted instance of webdriver
    """
    # Get muted firefox webdriver instance
    options = webdriver.FirefoxOptions()
    options.headless = True
    options.set_preference("media.volume_scale", "0.0")
    return webdriver.Firefox(options=options)

    # Use chrome instead of firefox
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    # No visible browser
    chrome_options.add_argument("--headless")

    return webdriver.Chrome(chrome_options=chrome_options)

def get_credentials():
    with open('cred.json', 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    browser = get_webdriver()
    browser.get('https://www.deezer.com/us/login')
    time.sleep(2)
    browser.find_element(By.ID, 'gdpr-btn-refuse-all').click()

    credentials = get_credentials()

    email_el = browser.find_element(By.ID, 'login_mail')
    pw_el = browser.find_element(By.ID, 'login_password')
    enter_el = browser.find_element(By.ID, 'login_form_submit')

    email_el.send_keys(credentials['username'])
    pw_el.send_keys(credentials['password'])
    enter_el.click()
    # Wait for login redirect
    time.sleep(5)
    try:
        WebDriverWait(browser, 10).until(lambda x: x.find_element(By.ID, 'page_topbar'))
    except TimeoutException:
        print('Looks like either your credentials are wrong or we\'ve hit a captcha, check credentials or try again later.')
        browser.quit()
        exit()
    

    browser.get(credentials['playlist-link'])
    play_button = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, "[data-testid='playlist-play-button']"))

    try:
        close_popup = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.ID, 'modal-close'))
        close_popup.click()
    except:
        # No premium upgrade popup
        pass

    # Mute button on deezer, might mess with deezers logging of number of listens
    # browser.find_element(By.CSS_SELECTOR, "[data-testid='volume-unmute']").click()

    play_button = browser.find_element(By.CSS_SELECTOR, "[data-testid='playlist-play-button']")
    browser.execute_script("arguments[0].click()", play_button)

    # Get to repeat all tracks in list
    # Loops through 3 phases, no repeat, repeat all tracks, repeat single track
    try:
        # Currently in repeat single track
        repeat_button = browser.find_element(By.CSS_SELECTOR, '[aria-label="Turn off repeat"]')
        repeat_button.click()
        repeat_button.click()
    except:
        pass

    try:
        # Currently in no repeat
        repeat_button = browser.find_element(By.CSS_SELECTOR, '[aria-label="Repeat all tracks in list"]').click()
    except:
        pass

    # Must be repeat all tracks here

    while True:
        try:
            wait = input('Type exit or send Ctrl+C to stop')
            if wait.lower().strip() == 'exit':
                browser.quit()
                print('Exiting')
                exit()
        except:
            browser.quit()
            exit()
