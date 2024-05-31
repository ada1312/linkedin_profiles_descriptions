# LinkedIn Alumni Scraper

This project provides a script to log into LinkedIn, scrape current positions from alumni profiles of a specific university, and save the data to a CSV file.

## Features

- **Login to LinkedIn:** Automatically log in using your credentials.
- **Scrape Alumni Data:** Extract current positions from alumni profiles of a specified university.
- **Save Data:** Save the scraped data to a CSV file.
- **Handle Checkpoints:** Prompt the user to manually complete checkpoint challenges if encountered.

## Prerequisites

- Python 3.x
- Selenium
- dotenv
- ChromeDriver

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/linkedin-alumni-scraper.git
    cd linkedin-alumni-scraper
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Download ChromeDriver from [here](https://developer.chrome.com/docs/chromedriver/downloads) and ensure it is installed and in your PATH.

5. Create a `.env` file in the root directory of the project and add your LinkedIn credentials:

    ```plaintext
    LINKEDIN_USERNAME=your_linkedin_username
    LINKEDIN_PASSWORD=your_linkedin_password
    ```

## Usage

1. Update the `alumni_url` in the script with the LinkedIn alumni page URL of the desired university.

2. Run the script:

    ```bash
    python linkedin_alumni_scraper.py
    ```

3. The script will log in to LinkedIn, scrape the current positions from the specified alumni profiles, and save the data to `linkedin_alumni_profiles.csv`.

## Script Details

### `login_to_linkedin(driver, username, password)`

Logs into LinkedIn using the provided credentials.

### `get_profile_current_positions(driver)`

Extracts current positions from profile cards on the page.

### `get_own_current_position(driver)`

Gets the current position from the user's own LinkedIn profile.

### `save_to_csv(data, filename)`

Saves the scraped data to a CSV file.

### `infinite_scroll(driver, scroll_pause_time=2)`

Scrolls down the page until the end is reached to load all profiles.

### `extract_all_profiles(driver, alumni_url)`

Combines all functions to extract and return current positions from alumni profiles.

## Notes

- Ensure you have ChromeDriver installed and in your PATH.
- Handle LinkedIn's checkpoint challenges manually if prompted.
- Update the `alumni_url` to target different alumni pages.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to reach out if you encounter any issues or have any questions. Happy scraping!