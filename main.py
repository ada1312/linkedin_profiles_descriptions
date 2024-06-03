from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import time
import csv
import os

# Load environment variables from .env file
load_dotenv()

linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

def login_to_linkedin(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
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

def get_profile_info(driver):
    profiles = driver.find_elements(By.CLASS_NAME, "org-people-profile-card")
    profile_data = []
    
    for profile in profiles:
        try:
            name = profile.find_element(By.CLASS_NAME, "artdeco-entity-lockup__title").text
            link_element = profile.find_element(By.TAG_NAME, "a")
            link = link_element.get_attribute("href")
            current_position = profile.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle").text

            profile_data.append({
                "Name": name, 
                "Profile Link": link, 
                "Current Position": current_position
            })
            print(f"Extracted: {name}, {link}, {current_position}")  # Debugging output
        except NoSuchElementException:
            name = profile.find_element(By.CLASS_NAME, "artdeco-entity-lockup__title").text
            current_position = profile.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle").text
            profile_data.append({
                "Name": name, 
                "Profile Link": "NA", 
                "Current Position": current_position, 
            })
            print(f"Extracted: {name}, NA, {current_position}")  # Debugging output
            continue
        except Exception as e:
            print(f"Error extracting profile info: {e}")
            continue
    
    return profile_data

def get_own_profile_info(driver):
    driver.get("https://www.linkedin.com/in/me/")
    time.sleep(3)
    profile_data = []

    try:
        name = driver.find_element(By.CSS_SELECTOR, ".text-heading-xlarge.inline.t-24.v-align-middle.break-words").text
        current_position = driver.find_element(By.CSS_SELECTOR, ".text-body-medium.break-words").text
        profile_data.append({
            "Name": name,
            "Profile Link": "https://www.linkedin.com/in/me/",
            "Current Position": current_position,
            "Location": "NA",
            "Connections": "NA"
        })
        print(f"Own profile extracted: {name}, {current_position}")
    except Exception as e:
        print(f"Error extracting own profile info: {e}")

    return profile_data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["Name", "Profile Link", "Current Position", "Location", "Connections"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def scrape_alumni_profiles(alumni_url):
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed and in PATH
    try:
        login_to_linkedin(driver, linkedin_username, linkedin_password)
        driver.get(alumni_url)
        time.sleep(5)  # Allow time for the page to load
        scroll_page(driver)
        
        # Extract alumni profiles
        profile_data = get_profile_info(driver)
        
        # Extract own profile
        own_profile_data = get_own_profile_info(driver)
        
        # Add own profile to the profile data
        profile_data.extend(own_profile_data)
        
        save_to_csv(profile_data, "linkedin_alumni_profiles.csv")
        print(f"Scraped {len(profile_data)} profiles to linkedin_alumni_profiles.csv")
    finally:
        driver.quit()

def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

if __name__ == "__main__":
    alumni_url = "https://www.linkedin.com/school/university-of-ljubljana-social-sciences/people/?facetFieldOfStudy=101913"
    scrape_alumni_profiles(alumni_url)
