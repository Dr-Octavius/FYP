import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
import shutil
from requests.auth import HTTPBasicAuth
from src.config import AIRCALL_USERNAME, AIRCALL_PASSWORD

# Load the CSV file
csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/SA_Singapore_Calls.csv'))
df = pd.read_csv(csv_file_path)

# for aircall
downloads_dir = '' # your downloads directory
# Define the directory and pattern
file_pattern = r'call-\w+\.mp3'  # Replace \w+ with the specific pattern you expect for STRING_ID

# Directory to save recordings
recordings_dir = '/Volumes/HP P900' # Can use relative or absolute for external disk
os.makedirs(recordings_dir, exist_ok=True)

def download_recording(url, output_path):
    print(url)
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Save the MP3 file to disk
        with open(output_path, "wb") as f:
            f.write(response.content)
        print("Recording downloaded successfully.")
    else:
        print("Failed to download the recording. Status code:", response.status_code)

def wait_for_download(download_path, file_pattern, timeout=1000):
    """
    Waits for the download to finish with a specific file pattern.
    :param download_path: The directory where the file is being downloaded.
    :param file_pattern: The regular expression pattern the filename should match.
    :param timeout: Maximum time to wait for the download to finish.
    """
    pattern = re.compile(file_pattern)
    wait_time = 0
    while wait_time < timeout:
        # Sleep for a short time interval
        time.sleep(1)  
        # Check all files in the download directory
        for file_name in os.listdir(download_path):
            # If a file matches the expected pattern and is not a partial download
            if pattern.match(file_name) and not file_name.endswith(('.crdownload', '.part')):
                return os.path.join(download_path, file_name)  # Download completed
        wait_time += 1
    raise Exception('Timeout reached: download did not finish within the specified time.')

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    if index <= 8325:
        continue
    recording_url = row['Recording URL']
    record_id = row['Record ID']
    file_name = f"{record_id}.mp3"  # Construct file name using Record ID
    file_path = os.path.join(recordings_dir, file_name)

    # Make the GET request with HTTP Basic Authentication
    if ("twilio" in recording_url):
        # Download the recording
        download_recording(recording_url, file_path)
        print(index)
    if ("aircall" in recording_url):
        driver = webdriver.Chrome()  # Or any other driver
        driver.get(recording_url)

        # You would need to log in before you can access the recording, if required.
        driver.find_element(By.ID,'email').send_keys(AIRCALL_USERNAME)
        driver.find_element(By.ID,'password').send_keys(AIRCALL_PASSWORD)

        # Wait for the login button to be clickable, then click it
        login_button = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="signin-button"]'))
        )
        login_button.click()

        # Wait for the download button to be clickable and then click it
        download_button = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="download-file-btn"]'))
        )
        download_button.click()

        # Wait for the file to download
        downloaded_file_path = wait_for_download(downloads_dir, file_pattern)

        # Rename and move the file to the recordings directory
        shutil.move(downloaded_file_path, file_path)
        print(f"File downloaded and moved to {file_path}")
    print(index)
print("All twilio recordings processed.") 