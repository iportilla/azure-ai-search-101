import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from render_table import render_product_results

dotenv.load_dotenv()

search_client = SearchClient(
    f"https://{os.environ['AZURE_SEARCH_SERVICE']}.search.windows.net",
    "zava-products-index",
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"]),
)

search_query = "25 foot hose"

results = search_client.search(search_text=search_query, top=5)

render_product_results(results, f"Keyword search results for '{search_query}'")
