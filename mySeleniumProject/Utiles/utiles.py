from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
import random
from .global_variables import user_agent_


print("User-Agent for Chrome:", user_agent_)

chrome_options = Options()

chrome_options.add_argument("--incognito")
chrome_options.add_argument(f"user-agent={user_agent_}")  # Add a real User-Agent string here
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Initialize WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)

# Remove webdriver attribute
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 10)


def human_like_delay(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

def openChrome(URL):
    # Open the Amazon website
    driver.get(f'{URL}')

    human_like_delay()

    # Optional: Maximize the browser window
    driver.maximize_window()


def closeChrome():
    driver.quit()


def login(username,password):
    human_like_delay()

    sign_in = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/identity/global/signin" and @data-track="Notification:Sign In"]')))
    sign_in.click()
    human_like_delay()

    human_like_delay()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    human_like_delay()

    email_input = driver.find_element(By.ID, "fld-e")
    email_input.send_keys(username)


    human_like_delay()

    password_input = driver.find_element(By.ID, "fld-p1")
    password_input.send_keys(password)

    human_like_delay()

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @data-track="Sign In"]')))
    login_button.click()

    skip_phone_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[@class="c-button-link cia-cancel" and @type="button" and @data-track="Add Recovery Phone - Skip for now"]')))
    skip_phone_input.click()

def click_button_by_id(id):
    # find the element you are looking for
    button = wait.until(EC.element_to_be_clickable((By.ID, f"{id}")))
    button.click()


def get_all_product_names(id):
    products = driver.find_elements(By.CLASS_NAME, f"{id}")
    for product in products:
        print(product.text)


def click_img_with_h4_text(text):
    # Wait until the desired element is present in the DOM
    human_like_delay()

    wait = WebDriverWait(driver, 1)

    # Use an XPath expression to find the img element with a direct child h4 element containing the specified text
    xpath = f'//h4[text()="{text}"]/preceding-sibling::img'

    # Wait for the element to be visible and clickable
    img_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    human_like_delay()
    # Click on the image element
    img_element.click()


# Initialize an empty list to store the concatenated strings
concatenated_texts = []
def search_bar():
    search_bar_input = wait.until(EC.element_to_be_clickable((By.ID, "gh-search-input")))
    search_bar_input.send_keys("hello")

    time.sleep(2)
    parent_spans = driver.find_elements(By.XPATH, "//span[@data-testid='Highlighter']")


    # Loop through each parent span element to check if the Hello Kitty string exists.
    for parent_span in parent_spans:
        # Find the child span elements within the parent span
        child_spans = parent_span.find_elements(By.XPATH, "./span")

        # Combine text content of child span elements into a single string
        combined_text = "".join([child_span.text for child_span in child_spans])

        # Append the combined text to the list
        concatenated_texts.append(combined_text)

    # Print the list of concatenated strings
    print(concatenated_texts)
    check_if_contains_hello_kitty(concatenated_texts,"hello kitty")




def check_if_contains_hello_kitty(arr,str):
    for text in arr:
        if f'{str}' in text.lower():
            print(f"Match found: {text}")
        else:
            print(f"No match: {text}")


def hover_over_elements():
    parent_spans = driver.find_elements(By.XPATH, "//span[@data-testid='Highlighter']")

    # Initialize ActionChains object
    actions = ActionChains(driver)

    # Loop through each parent span element
    for parent_span in parent_spans:
        # Hover over each element
        actions.move_to_element(parent_span).perform()

        # Print which element is being hovered over (optional)
        print(f"Hovering over: {parent_span.text}")

        # # Wait for 2 seconds before moving to the next element
        # time.sleep(2)

    # Hover over the third element in the array (index 2 since it's 0-based)
    if len(parent_spans) >= 3:
        actions.move_to_element(parent_spans[3]).perform()
        print(f"Hovering over the third element: {parent_spans[3].text}")

    # # Wait for 2 seconds before moving to the next action
    # time.sleep(2)

    # Find the specific element's parent <a> element with the specified class and click it
    specific_element_parent = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//span[text()='Razer - Kraken Hello Kitty Edition Wireless Gaming Headset - Pink']/ancestor::a[contains(@class, 'clamp lines-3 v-text-tech-black suggest-target')]")
        )
    )
    specific_element_parent.click()
    print("Clicked on the parent <a> element of the specific element.")


def check_if_price_exists_in_page():
    try:
        # Wait for the div with the specified class to be present
        price_div = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "priceView-hero-price.priceView-customer-price"))
        )

        # Find the span inside this div
        price_span = price_div.find_element(By.XPATH, ".//span[contains(text(), '$')]")

        # Check if the span contains a number and a dollar sign
        if re.search(r'\$\d', price_span.text):
            # Get the computed font size of the span
            font_size = driver.execute_script(
                "return window.getComputedStyle(arguments[0], null).getPropertyValue('font-size');", price_span)

            # Check if the font size is 30px
            if font_size == "30px":
                print("The current item has a price mentioned and the font size is indeed 30px: " + price_span.text)
            else:
                print(f"The current item has a price mentioned but the font size is {font_size}: " + price_span.text)
        else:
            print("No price found in the span.")
    except Exception as e:
        print("Price div or span not found. Error: ", e)


def click_and_check_elements(element_xpath):
    # Define the xpaths of the elements to click
    specifications_xpath = "//h5[@class='spec-heading']"
    features_xpath = "//span[@class='label' and contains(text(), 'Features')]"
    questions_xpath = "//span[@class='heading-5' and contains(text(), 'Questions & Answers')]"

    # Define the xpath of the div to check
    check_div_xpath = "//div[@class='drawer large' and @tabindex='-1' and @role='dialog' and contains(@style, 'animation-name: pdpDrawerSlideLeft; height: 100vh;')]"

    def is_element_clickable(element_xpath):
        try:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
            print("true")
            return True
        except Exception:
            print("false")
            return False

    def click_and_check(element_xpath):
        try:
            # Check if the element is clickable
            if is_element_clickable(element_xpath):
                print("1")
                # Find the element to click
                element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))

                # Click the element
                element_to_click.click()

                # Wait and check if the specified div appears
                check_div = wait.until(EC.presence_of_element_located((By.XPATH, check_div_xpath)))

                if check_div:
                    print("2")
                    print(f"The div appeared after clicking the element: {element_xpath}")
                    element_to_click = wait.until(EC.element_to_be_clickable((By.ID, "pdp-drawer-overlay-backdrop")))
                    element_to_click.click()
                    # close the new appearing element
                    time.sleep(2)
                    print("Closing Popped Up element")
                else:
                    print("3")
                    print(f"The div did not appear after clicking the element: {element_xpath}")
            else:
                print("4")
                print(f"Element not clickable: {element_xpath}")

        except Exception as e:
            print("5")
            print(f"Error occurred for element: {element_xpath}. Error: {e}")

    # Call the function for the specified element
    click_and_check(element_xpath)

