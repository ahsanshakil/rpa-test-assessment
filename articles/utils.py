import logging
import re

from robocorp import browser
from articles.article import Article
from datetime import date
from dateutil.relativedelta import relativedelta
from RPA.Assistant import Assistant
from typing import Optional
from constants import *

def user_input_task():
    """
    Collect user input for the search phrase, section, and number of months.

    Returns:
        tuple: A tuple containing the number of months, the section, and the search phrase.
    """
    assistant = Assistant()
    assistant.add_heading("Please Fill this form.")

    assistant.add_text_input(name="search_phrase", label="Search Phrase")
    assistant.add_drop_down(name="section", options=SECTION_LIST, label="Section", default='Any')
    assistant.add_text_input(name="months", label="Months", validation=validate_month_input)
    assistant.add_submit_buttons("Submit", default="Submit")

    result = assistant.run_dialog()
    search_phrase = result.search_phrase
    section = result.section
    months = int(result.months)

    return months, section, search_phrase


def validate_month_input(months: str) -> Optional[str]:
    """
    Validate the months input to ensure it's a single-digit number.

    Args:
        months (str): The input for the number of months.

    Returns:
        Optional[str]: An error message if the input is invalid, otherwise None.
    """
    regex = r"^\d$"
    valid = re.match(regex, months)
    if not valid:
        return "Please enter number of months in single digit only."
    return None


def get_date_range(months: int) -> tuple[str, str]:
    """
    Calculate the start and end dates based on the number of months.

    Args:
        months (int): The number of months for the date range.

    Returns:
        tuple: A tuple containing the start date and end date as strings.
    """
    end_date = date.today()
    start_date = end_date - relativedelta(months=months - 1) if months > 0 else end_date.replace(day=1)
    end_date_str = end_date.strftime("%m/%d/%Y")
    start_date_str = start_date.strftime("%m/%d/%Y")

    return start_date_str, end_date_str


def article_search(data: dict) -> None:
    """
    Perform an article search based on the provided data.

    Args:
        data (dict): A dictionary containing the search phrase, section, and number of months.
    """
    logging.info("Process Start")
    browser.configure(slowmo=5000)
    logging.info("Opening Website")


    search_phrase = data.get('search_phrase', DEFAULT_DATA_TO_PROCESS["search_phrase"])
    section = data.get('section', DEFAULT_DATA_TO_PROCESS["section"])
    months = int(data.get('months', DEFAULT_DATA_TO_PROCESS["months"]))
    start_date, end_date = get_date_range(months)

    search = Article(search_phrase, IMAGE_DIR, start_date, end_date, section, URL)

    search.open_news_website()
    logging.info(f"Searching for the keyword '{search_phrase}'")
    search.search_for_articles()
    search.select_section()
    search.set_date_range()
    search.extract_and_store_articles()
    logging.info("Process End")
