from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Edge()
driver.minimize_window()

driver.get("https://store.steampowered.com/search/?category1=998&filter=topsellers")
time.sleep(2)

names = driver.find_elements_by_class_name("title")

for g in names:
    print(g.text)
print(len(names))
exit()