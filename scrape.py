from selenium import webdriver
chrome_driver_path = "/Users/tianhaoyao/Desktop/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.reddit.com/search/?q=bitcoin")
text = driver.find_element_by_class_name("._1PoD47oSHsBQ37RfRPY-G-");
print(text);
driver.quit();
