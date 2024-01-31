import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
action = ActionChains(browser)
browser.get('https://learn.zybooks.com/library')


def login(browser):
    email_input = browser.find_element(By.XPATH, "//input[@type='email']")
    email = input("Enter email: ").strip()
    email_input.send_keys(email)
    password_input = browser.find_element(By.XPATH, "//input[@type='password']")
    password = getpass.getpass("Enter password: ")
    password_input.send_keys(password)
    sign_in = browser.find_element(By.CLASS_NAME, 'signin-button')
    sign_in.click()
    browser.implicitly_wait(5)


def get_class(browser):
    browser.find_element(By.XPATH, "//div[@class='zybooks-container large']/a[1]").click()
    browser.implicitly_wait(5)


def get_week(browser, action):
    xpath = "//div[@class='tabs']//button[3]/i[@aria-label='assignment']"
    assignment = browser.find_element(By.XPATH, xpath)
    (action.move_to_element(assignment).click().perform())
    browser.implicitly_wait(5)
    week_number = int(input("Choose week number: "))
    week_path = "//h3[normalize-space()='Week {} Prep']".format(week_number)
    week_browse = browser.find_element(By.XPATH, week_path)
    action.move_to_element(week_browse).click().perform()
    browser.implicitly_wait(5)


def mult_choice(action):
    for x, y in enumerate(multi_choice):
        if not y.is_enabled() and not y.is_displayed():
            continue
        action.move_to_element(y).perform()
        y.click()


def fill(browser, action):
    for x, y in enumerate(show_answer_list):
        if not y.is_enabled() and not y.is_displayed():
            continue
        action.move_to_element(y).perform()
        y.click()
        time.sleep(0.1)
        y.click()
        time.sleep(0.1)
        answer = browser.find_elements(By.CLASS_NAME, "forfeit-answer")[x].text
        textarea = browser.find_elements(By.CLASS_NAME, "ember-text-area")[x]
        textarea.send_keys(answer)
        time.sleep(0.1)
        browser.find_elements(By.CLASS_NAME, "check-button")[x].click()
        time.sleep(0.5)


def video(browser, action):
    for x, y in enumerate(video_list):
        if not y.is_enabled() and not y.is_displayed():
            continue
        action.move_to_element(y).perform()
        y.click()
        time.sleep(1)
        while True:
            time.sleep(3)
            play_button_img = browser.find_elements(By.CLASS_NAME, "play-button")
            if len(play_button_img) <= x:
                continue
            else:
                play_button_img = play_button_img[x]
            judge_end = play_button_img.get_attribute("class").find("rotate-180")
            judge = play_button_img.get_attribute("class").find("bounce")
            if judge_end != -1:
                break
            if judge != -1:
                play_button_img.click()


login(browser)
time.sleep(0.5)
get_class(browser)
time.sleep(0.5)
get_week(browser, action)

section_list = browser.find_elements(By.XPATH, "//li[@class = 'flex items-center mb-2']")
count = 13
section_path = str("//li[@class = 'flex items-center mb-2']")

for i in range(len(section_list)):
    paths = section_path + "[" + str(count) + "]"
    browser.find_element(By.XPATH, paths).click()
    time.sleep(0.2)
    multi_choice = browser.find_elements(By.CLASS_NAME, "zb-radio-button")
    show_answer_list = browser.find_elements(By.CLASS_NAME, "show-answer-button")
    video_list = browser.find_elements(By.CLASS_NAME, "start-graphic")
    if multi_choice != 0:
        mult_choice(action)
    if show_answer_list != 0:
        fill(browser, action)
    if video_list != 0:
        video(browser, action)
    else:
        continue
    browser.back()
    count += 1

