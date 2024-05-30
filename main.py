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

def get_profile_details(driver):
    profiles = driver.find_elements(By.CLASS_NAME, "entity-result__content")
    details = []
    
    for profile in profiles:
        try:
            description = profile.find_element(By.CLASS_NAME, "entity-result__primary-subtitle").text
            current_position = profile.find_element(By.CLASS_NAME, "entity-result__secondary-subtitle").text
            education = None
            additional_info = profile.find_elements(By.CLASS_NAME, "entity-result__summary")
            for info in additional_info:
                if "Education" in info.text:
                    education = info.text
                    break
            details.append((description, current_position, education))
        except Exception as e:
            print(f"Error extracting profile details: {e}")
            continue
    
    return details

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Profile Description", "Current Position", "Education"])
        writer.writerows(data)

if __name__ == "__main__":
    alumni_url = "https://www.linkedin.com/school/university-of-ljubljana-social-sciences/people/?facetFieldOfStudy=101913"
    
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed and in PATH
    
    try:
        login_to_linkedin(driver, linkedin_username, linkedin_password)
        
        driver.get(alumni_url)
        time.sleep(2)
        
        all_details = get_profile_details(driver)
        
        save_to_csv(all_details, "linkedin_alumni_profiles.csv")
        
        print(f"Saved {len(all_details)} profiles to linkedin_alumni_profiles.csv")
    finally:
        driver.quit()
