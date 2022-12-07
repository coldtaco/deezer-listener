import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-play', '--PLAY_DURATION', help = 'Duration in seconds to play playlist before pausing', type=int, default = -1)
parser.add_argument('-pause', '--PAUSE_DURATION', help = 'Duration in seconds to pause playlist after playing', type=int, default = -1)
parser.add_argument('-repeat', '--REPEAT', help = 'Number of times to repeat play pause cycle', type=int, default = -1)
args = parser.parse_args()

# -1 Play duration: Infinite play
PLAY_DURATION = args.PLAY_DURATION
# -1 Play once per day, ignored if PLAY_DURATION = -1
PAUSE_DURATION = args.PAUSE_DURATION
# Times to repeat, -1 = infinite repeat
REPEAT = args.REPEAT

def get_webdriver():
    """
        Returns a muted instance of webdriver
    """
    # Get muted firefox webdriver instance
    options = webdriver.FirefoxOptions()
    # Mute browser
    options.set_preference("media.volume_scale", "0.0")
    # No visible browser
    # options.headless = True
    return webdriver.Firefox(options=options)

    # Use chrome instead of firefox
    chrome_options = webdriver.ChromeOptions()
    # Mute browser
    chrome_options.add_argument("--mute-audio")
    # No visible browser
    chrome_options.add_argument("--headless")

    return webdriver.Chrome(chrome_options=chrome_options)

def get_credentials():
    with open('cred.json', 'r') as f:
        return json.load(f)

def setup(browser):
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
        print('Looks like either your credentials are wrong or we\'ve hit a captcha, check credentials in cred.json or try again later.')
        terminate(browser)

    print('Logged in')
    browser.get(credentials['playlist-link'])
    print('Got playlist')

    try:
        close_popup = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.ID, 'modal-close'))
        close_popup.click()
    except:
        # No premium upgrade popup
        pass

def repeat_all_tracks(browser):

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

def play_tracks(browser):
    play_button = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, "[data-testid='playlist-play-button']"))

    # Mute button on deezer, might mess with deezers logging of number of listens
    # browser.find_element(By.CSS_SELECTOR, "[data-testid='volume-unmute']").click()

    browser.execute_script("arguments[0].click()", play_button)
    print('Playing')

def play(browser):
    """
        Clicks play button
    """
    print(f'Play: {datetime.datetime.now()}')
    play_button = browser.find_element(By.CSS_SELECTOR, '[aria-label="Play"]')
    browser.execute_script("arguments[0].click()", play_button)

def pause(browser):
    """
        Clicks pause button
    """
    print(f'Pause: {datetime.datetime.now()}')
    play_button = browser.find_element(By.CSS_SELECTOR, '[aria-label="Pause"]')
    browser.execute_script("arguments[0].click()", play_button)

def terminate(browser):
    print('\nExiting')
    browser.quit()
    exit()

def playing_loop(browser):
    if PLAY_DURATION == -1:
        while True:
            try:
                wait = input('Type exit or send Ctrl+C to stop')
                if wait.lower().strip() == 'exit':
                    terminate(browser)
            except:
                terminate(browser)
    else:
        try:
            play_counter = 0
            if PAUSE_DURATION == -1:
                PAUSE_DURATION = 24*60*60 - PLAY_DURATION
            while True:
                time.sleep(PLAY_DURATION)
                pause(browser)
                time.sleep(PAUSE_DURATION)
                play(browser)
                play_counter += 1
                if (REPEAT != -1) and (play_counter >= REPEAT):
                    terminate(browser)
        except:
            terminate()
                


if __name__ == '__main__':
    browser = get_webdriver()
    setup(browser)
    play_tracks(browser)
    repeat_all_tracks(browser)
    playing_loop(browser)
