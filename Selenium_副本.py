import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
browser = webdriver.Chrome()
action = ActionChains(browser)
browser.get('https://learn.zybooks.com/library')


def login(browser):
    email = input("Enter email: ").strip()
    password = input("Enter Password: ").strip()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
    browser.find_element(By.XPATH, "//input[@type='email']").send_keys(email)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    browser.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
    browser.find_element(By.CLASS_NAME, 'signin-button').click()



def get_class(browser):
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".zybooks-container.large a:first-child")))
    browser.find_element(By.CSS_SELECTOR, ".zybooks-container.large a:first-child").click()


def get_week(browser):
    xpath = "//div[@class='tabs']//button[3]/i[@aria-label='assignment']"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    browser.find_element(By.XPATH, xpath).click()
    browser.implicitly_wait(5)
    assignment_name = input("Enter your assignment name(matching exactly as what displayed on web): ")
    week_path = f"//h3[@class = 'assignment-title my-auto primary-font-regular'][normalize-space()='{assignment_name}']"
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, week_path)))
    browser.find_element(By.XPATH, week_path).click()


def mult_choice(browser):
    elements = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'zb-radio-button')))
    for element in elements:
        if element.is_displayed():
            element.click()
            time.sleep(0.1)

def fill(browser):
    for x, y in enumerate(show_answer_list):
        if not y.is_enabled() and not y.is_displayed():
            continue
        action.move_to_element(y).perform()
        y.click()
        browser.implicitly_wait(3)
        y.click()
        browser.implicitly_wait(3)
        # get answer
        answer = browser.find_elements(By.CLASS_NAME, "forfeit-answer")[x].text
        textarea = browser.find_elements(By.CLASS_NAME, "ember-text-area")[x]
        textarea.send_keys(answer)
        browser.implicitly_wait(3)
        browser.find_elements(By.CLASS_NAME, "check-button")[x].click()
        browser.implicitly_wait(3)




def video(browser, action):
    for x, y in enumerate(video_list):
        action.move_to_element(y).perform()
        if not y.is_enabled() and not y.is_displayed():
            continue
        y.click()
        time.sleep(0.2)
        while True:
            time.sleep(0.2)
            play_button_img = browser.find_elements(By.CLASS_NAME, "play-button")
            if len(play_button_img) <= x:
                continue
            else:
                play_button_img = play_button_img[x]
            judge_end = play_button_img.get_attribute("class").find("rotate-180")
            judge = play_button_img.get_attribute("class").find("bounce")
            speed_button = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
            if judge_end != -1:
                action.move_to_element(speed_button).click().perform()
                break
            if judge != -1:
                play_button_img.click()



login(browser)
time.sleep(0.5)
get_class(browser)
time.sleep(0.5)
get_week(browser)
time.sleep(5)


section_list = browser.find_elements(By.XPATH, "//li[@class = 'flex items-center mb-2']")

section_path = str("//li[@class = 'flex items-center mb-2']")

for i in range(len(section_list)):
    path = f"{section_path}[{1+ i}]"
    browser.find_element(By.XPATH, path).click()

    multi_elements = browser.find_elements(By.CLASS_NAME, "zb-radio-button")
    show_answer_list = browser.find_elements(By.XPATH, "//button[normalize-space()='Show answer']")
    video_list = browser.find_elements(By.CLASS_NAME, "start-graphic")

    if multi_elements:
        mult_choice(browser)
    if show_answer_list:
        fill(browser)
    if video_list:
        video(browser, action)

    browser.back()

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, path)))
