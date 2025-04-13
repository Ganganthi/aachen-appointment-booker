import random
import re
import time

from plyer import notification
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


####
current_booked_day = 12
current_booked_month = 4

ONLY_NOTIFY = True

VORNAME = ""
NACHNAME = ""
EMAIL = ""
TELEFON = ""
BDAY = ""
BMONTH = ""
BYEAR = ""
####


def is_date_earlier_than_booked(day: int, month: int) -> bool:
    if month < current_booked_month:
        return True
    elif month > current_booked_month:
        return False

    if day < current_booked_day:
        return True
    return False


options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_experimental_option("detach", True)

while True:
    time.sleep(random.randint(30, 60))

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.minimize_window()

    driver.get("https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1")

    time.sleep(3)
    driver.find_element("id", "cookie_msg_btn_no").click()

    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)
    l1 = driver.find_elements(
        "xpath",
        "//div[contains(@id, 'concerns_accordion-115')]"
        "[.//h3[text()[contains(., 'Aufenthalt')]]]",
    )
    l1[0].click()

    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)
    l2 = driver.find_element(
        "xpath",
        "//button[contains(@id, 'button-plus-202')]",
    )
    l2.click()

    time.sleep(2)
    l3 = driver.find_elements(
        "xpath",
        "//input[contains(@id, 'WeiterButton')]",
    )
    l3[0].click()

    time.sleep(2)
    l4 = driver.find_element(
        "xpath",
        "//button[contains(@id, 'OKButton')]",
    )
    l4.click()

    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)
    l5 = driver.find_elements(
        "xpath",
        "//h1[text()[contains(., 'Kein freier Termin')]]",
    )

    if len(l5) > 0:
        print("Unavailable!")
        driver.close()
        continue
    else:
        print("Booking possible!")

    # Regex pattern to match the day and month
    pattern = r"^[A-Za-z]+, (\d{2})\.(\d{2})\.\d{2}"

    l6 = driver.find_elements("xpath", "//div[contains(@id, 'sugg_accordion')]//h3")
    for elem in l6:
        data = elem.get_attribute("title")
        print(data)

        # Extract day and month using regex search
        mat = re.search(pattern, data)

        if not mat:
            print("No match found.")
            continue

        day = int(mat.group(1))
        month = int(mat.group(2))
        print(f"Day: {day}, Month: {month}")
        if is_date_earlier_than_booked(day, month) is False:
            break

        if ONLY_NOTIFY is True:
            notification.notify(
                title="Booking possible!",
                message=f"Day: {day}, Month: {month}",
                app_icon=None,
                timeout=10,
            )
            break

        panel = elem.get_attribute("aria-controls")

        l7 = driver.find_elements(
            "xpath",
            "//div[contains(@id, 'sugg_accordion')]//div[contains(@id,"
            f" '{panel}')]//form//button",
        )
        l7[0].click()

        time.sleep(1)
        l8 = driver.find_element("xpath", "//button[text()[contains(., 'Ja')]]")
        l8.click()

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)
        input_field = driver.find_element("id", "vorname")
        input_field.send_keys(VORNAME)

        input_field = driver.find_element("id", "nachname")
        input_field.send_keys(NACHNAME)

        input_field = driver.find_element("id", "email")
        input_field.send_keys(EMAIL)

        input_field = driver.find_element("id", "emailwhlg")
        input_field.send_keys(EMAIL)

        input_field = driver.find_element("id", "tel")
        input_field.send_keys(TELEFON)

        input_field = driver.find_element("id", "geburtsdatumDay")
        input_field.send_keys(BDAY)

        input_field = driver.find_element("id", "geburtsdatumMonth")
        input_field.send_keys(BMONTH)

        input_field = driver.find_element("id", "geburtsdatumYear")
        input_field.send_keys(BYEAR)

        time.sleep(1)
        input_field = driver.find_element("id", "chooseTerminButton")
        input_field.click()

        current_booked_day = day
        current_booked_month = month
        break

    time.sleep(4)
    driver.close()
