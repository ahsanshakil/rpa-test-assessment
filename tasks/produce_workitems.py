import logging

from robocorp import workitems
from robocorp.tasks import task
# from articles.utils import user_input_task    # uncomment this if you want to run this locally and get the dialog box for user input.
from constants import *

def create_workitem_from_user(search_phrase: str, section: str, months: int) -> None:
    """
    Create a work item from user input.

    This function sets search terms dynamically by taking input from the user in the form of a dialog box.

    Args:
        search_phrase (str): The search phrase provided by the user.
        section (str): The section selected by the user.
        months (int): The number of months specified by the user.
    """
    output = workitems.outputs.create()
    output.payload = {"search_phrase": search_phrase, "section": section, "months": months}
    output.save()
    logging.info("The user input has been saved as a work item")


def create_workitem_for_cloud() -> None:
    """
    Create a work item with hardcoded search terms for running in the Control Room.

    This function generates a work item with predefined search terms to run on Control Room.
    """

    workitems.outputs.create(payload=DEFAULT_DATA_TO_PROCESS)


@task
def set_search_data() -> None:
    """
    Set search terms for looking up articles on the New York Times.

    The producer process sets the search terms to look up articles on the New York Times.
    """
    create_workitem_for_cloud()

    """
    The following lines of code would trigger a dialog box when run locally.
    In order to run the robot and provide custom parameters, please uncomment the following lines of code,
    Furthermore, comment the 'create_workitem_for_cloud()' function."""

    # months, section, search_phrase = user_input_task()
    # if months and section and search_phrase:
    #     create_workitem_from_user(search_phrase, section, months)
    # else:
    #     logging.info("User cancelled or did not provide all parameters.")
