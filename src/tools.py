from pydoc import doc
from langchain_core.tools import tool
from typing import List, Dict, Tuple
from vectorstore import UfoSiteVectorStore

vector_store = UfoSiteVectorStore()

@tool
def query_ufo_faqs(query: str) -> Tuple[str, List[Dict[str, str]]]:
    '''
    Use this tool to get information about UFOs.

    Args:
        query: The query to search for.

    Returns:
        A list of dictionaries containing the question and answer.
    '''
    print("querying faqs...")
    results = vector_store.query_faqs(query)
    print(results["documents"][0])
    return results["documents"][0]

@tool(response_format="content_and_artifact")
def query_aliens(query: str) ->Tuple[str, List[Dict[str, str]]]:
    '''
    Use this tool to get information about aliens.

    Args:
        query: The query to search for.

    Returns:
        A list of dictionaries containing the name, home system, description, and details about an alien species.
    '''
    print("querying aliens...")
    results = vector_store.query_aliens(query)
    print(results["documents"][0])
    return (results["documents"][0], results)

def reset():
    print("resetting...")
    vector_store.reset()
