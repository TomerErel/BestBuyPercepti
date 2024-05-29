import time

from Utiles.utiles import openChrome, closeChrome, login, click_img_with_h4_text, search_bar, hover_over_elements,check_if_price_exists_in_page, click_and_check_elements

openChrome("https://www.bestbuy.com/")

click_img_with_h4_text("United States")

login("checking@percepti.co","checking@percepti.co")

search_bar()

hover_over_elements()

check_if_price_exists_in_page()

# Call the function for each element
click_and_check_elements("//h5[@class='spec-heading']")
time.sleep(2)  # Wait between clicks
click_and_check_elements("//span[@class='label' and contains(text(), 'Features')]")
time.sleep(2)  # Wait between clicks
click_and_check_elements("/html/body/div[4]/main/div[5]/div/div/div/div/div/div/div[7]/div[1]/div[3]/div[3]/div/div/button")

time.sleep(200)

# Close the browser window
closeChrome()




