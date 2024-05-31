from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
import csv
import os

# Load environment variables from .env file
load_dotenv()

linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

def login_to_linkedin(driver, username, password):
    """
    Logs into LinkedIn using the provided credentials.

    Args:
        driver: The Selenium WebDriver instance.
        username: The LinkedIn username or email address.
        password: The LinkedIn password.

    Returns:
        None
    """
    # Open the LinkedIn login page
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    # Find the email and password fields and enter the credentials
    email_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    
    email_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)
    
    # Check if the checkpoint page is encountered
    current_url = driver.current_url
    if "checkpoint/challenge" in current_url:
        print("Checkpoint challenge detected. Please complete the verification manually.")
        input("Press Enter to continue after completing the verification...")

def get_profile_current_positions(driver):
    # Find all profile cards on the page
    profiles = driver.find_elements(By.CLASS_NAME, "org-people-profile-card")
    current_positions = []
    
    for profile in profiles:
        try:
            # Extract the current position from each profile card
            current_position = profile.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle").text
            current_positions.append(current_position)
            print(f"Extracted: {current_position}")  # Debugging output
        except Exception as e:
            print(f"Error extracting current position: {e}")
            continue
    
    return current_positions

def get_own_current_position(driver):
    # Open the user's own LinkedIn profile page
    driver.get("https://www.linkedin.com/in/me/")
    time.sleep(3)
    
    try:
        # Try multiple possible class names to account for LinkedIn's HTML changes
        current_position_element = driver.find_element(By.CSS_SELECTOR, ".text-body-medium.break-words")
        current_position = current_position_element.text
        print(f"Own current position: {current_position}")  # Debugging output
        return current_position
    except Exception as e:
        print(f"Error extracting own current position: {e}")
        return None

def save_to_csv(data, filename):
    # Save the data to a CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Current Position"])
        for position in data:
            writer.writerow([position])

def infinite_scroll(driver, scroll_pause_time=2):
    # Scroll down the page until the end is reached
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_all_profiles(driver, alumni_url):
    all_current_positions = []
    driver.get(alumni_url)
    time.sleep(5)  # Allow time for the page to load
    
    infinite_scroll(driver)
    
    current_positions = get_profile_current_positions(driver)
    all_current_positions.extend(current_positions)
    
    return all_current_positions

if __name__ == "__main__":
    alumni_url = "https://www.linkedin.com/school/university-of-ljubljana-social-sciences/people/?facetFieldOfStudy=101913"
    
    # Make sure you have the ChromeDriver installed and in PATH
    #If you are not sure run test_chrome_webdriver.py to check if it is installed correctly
    #If driver not installed, download it from https://developer.chrome.com/docs/chromedriver/downloads
    driver = webdriver.Chrome()  
    
    try:
        login_to_linkedin(driver, linkedin_username, linkedin_password)
        
        # Get own current position - this is optional and can be removed if not needed
        #It is only important if you are logged in to linkedin and you are alumni from social informatics
        #otherwise needs to be removed / commented out
        own_current_position = get_own_current_position(driver)
        
        # Get current positions from alumni profiles
        all_current_positions = extract_all_profiles(driver, alumni_url)
        
        # Add own current position to the list if available
        if own_current_position:
            all_current_positions.append(own_current_position)
        
        save_to_csv(all_current_positions, "linkedin_alumni_profiles.csv")
        
        print(f"Saved {len(all_current_positions)} profiles to linkedin_alumni_profiles.csv")
    finally:
        driver.quit()
