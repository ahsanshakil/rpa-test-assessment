from robocorp import workitems
from robocorp.tasks import task
from articles.utils import article_search


@task
def get_work_items() -> None:
    """
    Retrieve the current work item, process the data using the article_search function,
    and mark the work item as done.
    """
    item = workitems.inputs.current
    data = item.payload
    article_search(data)
    item.done()
