from selenium import webdriver

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to a web page
driver.get("http://www.python.org")

# Print the title of the page
print(driver.title)

# Close the browser
driver.quit()
