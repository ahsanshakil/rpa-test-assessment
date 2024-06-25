import csv
import re
import requests
import os
import logging

from robocorp import browser
from typing import List, Dict, Optional


class Article:
    def __init__(self, search_phrase: str, image_dir: str, start_date: str, end_date: str, section: str, url: str):
        """
        Initialize the ArticleSearch class with search parameters.

        Args:
            search_phrase (str): The phrase to search for in articles.
            image_dir (str): The directory to save downloaded images.
            start_date (str): The start date for the search range.
            end_date (str): The end date for the search range.
            section (str): The section of the website to search within.
        """
        self.search_phrase = search_phrase
        self.image_dir = image_dir
        self.start_date = start_date
        self.end_date = end_date
        self.section = section
        self.url = url

    def open_news_website(self) -> None:
        """
        Open the New York Times website and handle potential loading issues with retries.
        """
        logging.info(f"Opening website: {self.url}")

        retry_count = 3
        wait_time_seconds = 5
        success = False

        for attempt in range(retry_count):
            try:
                browser.goto(self.url)
                success = True
                break
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                logging.warning("Retrying...")
                wait_time_seconds *= 2
                page = browser.page()
                page.reload()
                page.wait_for_load_state()

        if not success:
            logging.error(f"Failed to open website after {retry_count} attempts.")

    def search_for_articles(self) -> None:
        """
        Perform a search on the New York Times website using the specified search phrase.
        """
        page = browser.page()
        page.wait_for_timeout(1000)

        accept_all_button = "button:text('Accept all')"
        search_input_aria_controls = "[aria-controls='search-input']"
        search_input_aria_label = "[aria-label='Search the new york times']"
        go_button = "button:text('Go')"

        if page.is_visible(accept_all_button):
            page.click(accept_all_button)
        page.focus(search_input_aria_controls)
        page.press(search_input_aria_controls, "Enter")
        page.fill(search_input_aria_label, self.search_phrase)
        page.click(go_button)

    def set_date_range(self) -> None:
        """
        Set the date range for the search using the specified start and end dates.
        """
        page = browser.page()
        date_input_css = ".css-p5555t"
        specific_dates_button = "button:text('Specific Dates')"
        start_date_input = "#startDate"
        end_date_input = "#endDate"

        page.focus(date_input_css)
        page.press(date_input_css, "Enter")
        page.click(specific_dates_button)
        page.fill(start_date_input, self.start_date)
        page.fill(end_date_input, self.end_date)
        page.press(end_date_input, "Enter")

    def select_section(self) -> None:
        """
        Select the section of the website to search within.
        """
        page = browser.page()
        section_button = "[data-testid='search-multiselect-button']"
        section_dropdown_list = "[data-testid='multi-select-dropdown-list']"
        section_xpath = f"//input[@data-testid='DropdownLabelCheckbox'][@value[contains(., '{self.section}')]]"

        page.click(section_button)
        page.wait_for_selector(section_dropdown_list)
        page.click(section_xpath)

    def download_image(self, url: str) -> str:
        """
        Download an image from the specified URL and save it to the image directory.

        Args:
            url (str): The URL of the image to download.

        Returns:
            str: The filename of the downloaded image, or an empty string if the download failed.
        """
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(self.image_dir, os.path.basename(url) + ".png")
            with open(filename, "wb") as file:
                file.write(response.content)
            return filename
        return ""

    def click_button_until_element_appears(self, button_selector: str, wait_time: int = 2) -> bool:
        """
        Click a button on the page repeatedly until a specified element appears or the button is no longer found.

        Args:
            button_selector (str): The CSS selector of the button to click.
            wait_time (int): The wait time between clicks in seconds.

        Returns:
            bool: True if the element appeared, False otherwise.
        """
        page = browser.page()
        while True:
            try:
                if page.is_visible(button_selector):
                    logging.info(f"Clicking button '{button_selector}'")
                    page.click(button_selector)
                    page.wait_for_load_state('networkidle', timeout=wait_time * 1000)
                else:
                    logging.info(f"Button '{button_selector}' not found.")
                    break
            except Exception as e:
                logging.error(f"Error while clicking the button: {e}")
                break

        logging.warning(f"Button '{button_selector}' not found anymore.")
        return False

    def extract_and_store_articles(self) -> None:
        """
        Extract articles from the search results and store them in a CSV file.
        """
        page = browser.page()
        self.click_button_until_element_appears(button_selector="[data-testid='search-show-more-button']")

        search_results = page.query_selector_all("ol[data-testid='search-results'] > li")
        data: List[Dict[str, Optional[str]]] = []

        lower_search_phrase = self.search_phrase.lower()

        for result in search_results:
            h4_element = result.query_selector("h4")
            p_elements = result.query_selector_all("p")
            img_element = result.query_selector("img")
            date_element = result.query_selector("[data-testid='todays-date']")
            date = date_element.get_attribute("aria-label") if date_element else ""

            if h4_element and p_elements:
                title = h4_element.inner_text()
                description = " ".join([p.inner_text() for p in p_elements])
                img_url = img_element.get_attribute("src") if img_element else ""
                picture_filename = self.download_image(img_url) if img_url else ""
                search_phrase_count = title.lower().count(lower_search_phrase) + description.lower().count(lower_search_phrase)
                money_pattern = re.compile(r"(\$\d+(\.\d{1,2})?|\$\d{1,3}(,\d{3})*(\.\d{2})?|(\d+\s+(dollars|USD)))")
                contains_money = bool(money_pattern.search(title) or money_pattern.search(description))
                data.append({
                    "title": title,
                    "description": description,
                    "date": date,
                    "picture_filename": picture_filename,
                    "search_phrase_count": search_phrase_count,
                    "contains_money": contains_money
                })

        csv_filename = f'output/news_articles_{self.search_phrase}.csv'
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "description", "date", "picture_filename", "search_phrase_count", "contains_money"])
            writer.writeheader()
            writer.writerows(data)

        logging.info(f"Data has been written to {csv_filename}")
