import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        self.service = ChromeService()
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

    def test_form_submission_failure(self):
        # Navigate to the page

        self.driver.get("http://localhost:8001")
        # Find the input text box and submit button
        input_box = self.driver.find_element(By.ID, "Input")
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        # Enter text into the input box
        input_box.send_keys("password")

        # Click the submit button
        submit_button.click()

        # Check the result
        result = self.driver.page_source
        self.assertIn("Invalid", result)

    def test_form_submission_success(self):
        # Navigate to the page

        self.driver.get("http://localhost:8001")
        # Find the input text box and submit button
        input_box = self.driver.find_element(By.ID, "Input")
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        # Enter text into the input box
        input_box.send_keys("test input")

        # Click the submit button
        submit_button.click()

        # Check the result
        result = self.driver.page_source
        self.assertIn("Input accepted: test input", result)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

