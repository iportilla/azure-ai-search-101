import os

import dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import OpenAI

from render_table import render_product_results

dotenv.load_dotenv()

openai_client = OpenAI(
    base_url=f"https://{os.environ['AZURE_OPENAI_SERVICE']}.openai.azure.com/openai/v1",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

search_client = SearchClient(
    f"https://{os.environ['AZURE_SEARCH_SERVICE']}.search.windows.net",
    "zava-products-index",
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"]),
)

search_query = "100 foot hose that won't break"

search_vector = (
    openai_client.embeddings.create(model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"], input=search_query)
    .data[0]
    .embedding
)

results = search_client.search(
    search_query,
    top=5,
    vector_queries=[VectorizedQuery(vector=search_vector, k_nearest_neighbors=50, fields="embedding")],
)

render_product_results(results)
