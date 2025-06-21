import time, platform, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import requests # Added requests for potential network error handling

def report_url(url_to_report: str) -> tuple[bool, str]:
    """
    Reports a given URL to Google Safe Browsing using Selenium automation.
    """
    driver = None # Initialize driver to None

    google_url = "https://safebrowsing.google.com/safebrowsing/report_phish/"

    if not url_to_report or not isinstance(url_to_report, str):
        return False, "Invalid URL provided for reporting. Please enter a valid URL."

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Dynamically set the chromedriver path based on OS
        system_platform = platform.system()
        if system_platform == "Windows":
            driver_path = "driver/chromedriver.exe"
        elif system_platform == "Linux":
            driver_path = "driver/chromedriver"
        else:
            return False, f"Unsupported operating system: {system_platform}"

        # Ensure the driver is executable on Linux
        if system_platform == "Linux":
            os.chmod(driver_path, 0o755)

        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(google_url)

        # Wait for the main form element to be visible, indicating the page has loaded
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.TAG_NAME, "sbsfe-form"))
        )

        # Click the dropdown to open it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//mat-form-field[1]//mat-select"))
        ).click()

        # Click the "This page is not safe" option (mat-option-1 can be dynamic, adjust if needed)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "mat-option-1"))
        ).click()

        # Input the URL to report
        url_input_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//mat-form-field[2]//input"))
        )
        url_input_element.send_keys(url_to_report)
        time.sleep(1)    # Wait for the input to be processed

        # Define status element XPath
        status_element_xpath = "/html/body/sbsfe-root/sbsfe-form/form/div/status-tile/mat-card"
        
        max_retries = 3
        current_retry = 0
        
        while current_retry < max_retries:
            # Find and click the submit button (on first attempt or retry)
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            submit_button.click()
            
            # Wait for the status message to appear or change
            time.sleep(3) # Give some time for the status to update
            
            try:
                status_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, status_element_xpath))
                )
                status_text = status_element.text

                if "Submission was successful." in status_text:
                    return True, "URL successfully reported to Google Safe Browsing."
                elif "Something went wrong there. Try again." in status_text:
                    current_retry += 1
                else:
                    return False, f"Unknown response from Google Safe Browsing: '{status_text}'"
            except TimeoutException:
                current_retry += 1
            except Exception as e:
                current_retry += 1

        return False, f"Failed to report URL after {max_retries} attempts. Please try again later."

    except TimeoutException as e:
        return False, f"Operation timed out: Could not interact with the page. This might be due to network issues or page changes."
    except NoSuchElementException as e:
        return False, f"Required element not found on the page. The Google Safe Browsing page structure might have changed, or an XPath is incorrect."
    except WebDriverException as e:
        return False, f"A browser automation error occurred (e.g., Chromedriver issue, browser crash): {e}. Ensure Chromedriver is compatible with your Chrome version."
    except requests.exceptions.RequestException as e: # Catch network errors during initial page load if any
        return False, f"Network error: Could not reach Google Safe Browsing page."
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"
    finally:
        if driver:
            driver.quit() # Close browser after user input or after failed attempts
