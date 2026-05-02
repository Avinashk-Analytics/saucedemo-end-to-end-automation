#Import Required Selenium Dependencies
from logging import error

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait

#------------------Setup Browser-----------------------------------------------------

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.saucedemo.com/")
driver.implicitly_wait(5)

#------------------------Locate Signup------------------------------------------------

#Using Valid Credential
driver.find_element(By.NAME, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.CLASS_NAME,"btn_action").click()

#Using Invalid Credential
# try:
#     driver.find_element(By.NAME, "user-name").send_keys("standard")
#     driver.find_element(By.ID, "password").send_keys("secret")
#     driver.find_element(By.CLASS_NAME,"btn_action").click()
#
#     if error:
#         print("Please enter correct username and password")
# except Exception:
#     pass

#Filter
dropDown= driver.find_element(By.CLASS_NAME,"product_sort_container")
select = Select(dropDown)
select.select_by_visible_text("Price (low to high)")

#Select Product
products = driver.find_elements(By.CLASS_NAME, "inventory_item")

for product in products:
    name = product.find_element(By.CLASS_NAME, "inventory_item_name").text

    if name == "Sauce Labs Fleece Jacket":
        # click using LINK_TEXT
        driver.find_element(By.LINK_TEXT, name).click()

        # now you're on product detail page → click add to cart
        driver.find_element(By.ID, "add-to-cart").click()
        break


#Checkout the product
driver.find_element(By.XPATH, "//a[@class = 'shopping_cart_link']").click()

#Checkout
driver.find_element(By.CSS_SELECTOR, "#checkout").click()

#Handle Scrollbar
driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")

time.sleep(3)
#Checkout Information
driver.find_element(By.XPATH,"//input[@name = 'firstName']").send_keys("John")
driver.find_element(By.XPATH,"//input[@id = 'last-name']").send_keys("khan")
driver.find_element(By.NAME,"postalCode").send_keys("12345")

#Click on continue
driver.find_element(By.XPATH,"//input[@type='submit']").click()

#Check out overview
driver.find_element(By.ID,"finish").click()
time.sleep(5)

#Order placed
order_Placed = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))).text
assert "Thank you for your order!" in order_Placed
print("Your Order Placed Successfully!!")
time.sleep(2)
driver.quit()
