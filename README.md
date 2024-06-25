
# Articles Search Robot with Robocorp

## Overview

This project demonstrates a consumer-producer pattern using the Robocorp platform. The producer generates work items with search criteria for articles, and the consumer retrieves these work items, performs searches on the New York Times website, and extracts and saves relevant articles. The robots use Robocorp’s work items, browser automation, and data extraction capabilities.

## Table of Contents

1.  [Prerequisites](#prerequisites)
2.  [Setup](#setup)
3.  [Project Structure](#project-structure)
4.  [Usage](#usage)
5.  [Flow Diagram](#flow-diagram)

## Prerequisites

-   Robocorp Lab
-   Python 3.8 or later
-   An internet connection to access the New York Times website if you are running locally.

## Setup

### Clone the Repository

Clone this repository to your local machine:

`git clone https://github.com/ahsanshakil/rpa-test-assessment`

`cd` into the root directory. 


### Configure Robocorp Lab

Open Robocorp Lab and configure your robot using the cloned repository. Ensure the project path points to your cloned directory.

## Project Structure



-   **`articles/`**: Contains the modules for searching and extracting articles.
-   **`tasks/`**: Contains the Robocorp task files for the consumer and producer.
-   **`constants.py`**: Contains constants used across the project.

## Usage

### Producer

The producer generates work items with search parameters. To run the producer task:

1.  Open Robocorp Lab in vs code extension.
2.  Select the producer task (`tasks/producer.robot`).
3.  Run the task.

This will create a work item with predefined search criteria. For running locally and providing custom search parameters, uncomment the lines in `create_workitem_from_user` function and comment `create_workitem_for_cloud`.
If you do so, you will get a dialog box to add the search criteria.

### Consumer

The consumer processes the work items, performs searches on the New York Times website, and saves the results. To run the consumer task:

1.  Open Robocorp Lab in vs code extension.
2.  Select the consumer task (`tasks/consumer.robot`).
3.  Run the task.

The consumer will fetch the work item created by the producer, perform the article search, and save the results in a CSV file.

### Custom Configuration

To use custom search terms, modify the `DEFAULT_DATA_TO_PROCESS` in `constants.py` or provide input through the user interface in `utils.py`.

## Flow Diagram

Here's a flow diagram of the process:


[![](https://mermaid.ink/img/pako:eNp1kWFLwzAQhv9KyOftD1QQZHXgB4fYoox2H27prQ1rGrlcnLLtv3uNdA7RQODN8b5PjrujNr5Bneld7w-mA2JV5vWgnsg30SBVk1DPfut5o-bz29OCEBiDevW0Vw-MLpySTrL6qaqCPUGLmxshyln4IUQn0ElcQ5fIpvsP-guQAtKZwRAkckdsTY8SWK3LaoUHtR4hpXUjD7fB8qUHcaT0_QcTGL4OT_S_PivgXVg5MIiveKnkqqXtE3a065kWqwPbyCyPY6XW3KHDWmciG6B9revhLD6I7IvPweiMKeJMk49tp7Md9EFe8a2R2eYWWgJ3qWJjZZSP36tKGzt_AQwbmLE?type=png)](https://mermaid.live/edit#pako:eNp1kWFLwzAQhv9KyOftD1QQZHXgB4fYoox2H27prQ1rGrlcnLLtv3uNdA7RQODN8b5PjrujNr5Bneld7w-mA2JV5vWgnsg30SBVk1DPfut5o-bz29OCEBiDevW0Vw-MLpySTrL6qaqCPUGLmxshyln4IUQn0ElcQ5fIpvsP-guQAtKZwRAkckdsTY8SWK3LaoUHtR4hpXUjD7fB8qUHcaT0_QcTGL4OT_S_PivgXVg5MIiveKnkqqXtE3a065kWqwPbyCyPY6XW3KHDWmciG6B9revhLD6I7IvPweiMKeJMk49tp7Md9EFe8a2R2eYWWgJ3qWJjZZSP36tKGzt_AQwbmLE)

----------

## Detailed Breakdown

### 1. Producer Robot

The producer robot (`tasks/producer.robot`) creates work items with search parameters. There are two ways to generate work items:

-   **Predefined Search Terms**: The `create_workitem_for_cloud` function sets hardcoded search parameters suitable for running in the Control Room.
-   **User Input**: The `create_workitem_from_user` function takes input from the user via a dialog box. Uncomment the relevant lines in `set_search_data` to use this method.

#### The reason for having two criteria: 

RoboCloud does not support assistant to open dialog boxes on cloud. Therefore, in order to get data from user in terms of a form could be achievable by hosting a webform on a different server and then hitting onto the REST API of Robocorp. 
The scope of this assessment forbade the use of any APIs. 

### 2. Consumer Robot

The consumer robot (`tasks/consumer.robot`) retrieves work items created by the producer, performs searches on the New York Times website, and extracts relevant articles. The extracted data is saved in a CSV file for further use.

### 3. Article Search Logic

The `Article` class in `articles/article.py` encapsulates the logic for searching and extracting articles from the New York Times website. It handles:

-   Opening the website
-   Performing the search
-   Setting the date range
-   Selecting the section
-   Extracting and downloading images
-   Storing the results in a CSV file

### 4. Utility Functions

The utility functions in `articles/utils.py` provide support for user input, date range calculations, and search logic. They include:

-   `user_input_task`: Collects user input for search parameters.
-   `validate_month_input`: Validates the month input.
-   `get_date_range`: Calculates the date range based on the number of months.
-   `article_search`: Orchestrates the search and extraction process.

### Constants

The `constants.py` file defines:

-   `SECTION_LIST`: Available sections for article search.
-   `IMAGE_DIR`: Directory for saving images.
-   `URL`: New York Times website URL.
-   `DEFAULT_DATA_TO_PROCESS`: Default search parameters.
