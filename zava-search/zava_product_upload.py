
"""Script to create an Azure AI Search index for product data and upload products."""

import json
import os
from typing import Any

import azure.identity
import dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    HnswParameters,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)
from openai import OpenAI

dotenv.load_dotenv()

EMBEDDING_DIMENSIONS = 1536  # text-embedding-3-small dimensions


def create_product_index_schema(index_name: str) -> SearchIndex:
    """Create the schema for the product index.

    Args:
        index_name: Name of the index to create

    Returns:
        SearchIndex object with the schema
    """
    fields = [
        SimpleField(
            name="sku",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True,
            sortable=True,
        ),
        SearchableField(
            name="name",
            type=SearchFieldDataType.String,
            sortable=True,
        ),
        SearchableField(
            name="description",
            type=SearchFieldDataType.String,
        ),
        SimpleField(
            name="price",
            type=SearchFieldDataType.Double,
            filterable=True,
            sortable=True,
            facetable=True,
        ),
        SimpleField(
            name="stock_level",
            type=SearchFieldDataType.Int32,
            filterable=True,
            sortable=True,
            facetable=True,
        ),
        SearchField(
            name="categories",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            searchable=True,
            filterable=True,
            facetable=True,
        ),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=EMBEDDING_DIMENSIONS,
            vector_search_profile_name="embedding-profile",
        ),
    ]

    # Configure vector search
    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="embedding-profile",
                algorithm_configuration_name="hnsw-config",
            )
        ],
        algorithms=[
            HnswAlgorithmConfiguration(
                name="hnsw-config",
                parameters=HnswParameters(metric="cosine"),
            )
        ],
    )

    # Configure semantic search for better relevance
    semantic_config = SemanticConfiguration(
        name="products-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="name"),
            content_fields=[SemanticField(field_name="description")],
            keywords_fields=[SemanticField(field_name="categories")],
        ),
    )

    semantic_search = SemanticSearch(
        default_configuration_name="products-semantic-config",
        configurations=[semantic_config],
    )

    return SearchIndex(
        name=index_name,
        fields=fields,
        semantic_search=semantic_search,
        vector_search=vector_search,
    )


def create_index(index_client: SearchIndexClient, index_name: str) -> None:
    """Create the search index, deleting any existing one first.

    Args:
        index_client: Azure Search Index Client
        index_name: Name of the index to create
    """
    try:
        index_client.delete_index(index_name)
        print(f"Deleted existing index '{index_name}'.")
    except Exception:
        pass
    print(f"Creating index '{index_name}'...")
    index_schema = create_product_index_schema(index_name)
    index_client.create_or_update_index(index_schema)
    print(f"Index '{index_name}' created successfully.")


def generate_embeddings(openai_client: OpenAI, products: list[dict[str, Any]]) -> None:
    """Generate embeddings for products using OpenAI.

    Args:
        openai_client: OpenAI client
        products: List of product dictionaries (modified in place)
    """
    print("Generating embeddings for products...")

    for i, product in enumerate(products):
        # Create text to embed from name, description, and categories
        text_to_embed = f"{product['name']} {product['description']} {' '.join(product['categories'])}"

        # Generate embedding
        response = openai_client.embeddings.create(
            model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"], input=text_to_embed
        )
        product["embedding"] = response.data[0].embedding

        if (i + 1) % 100 == 0:
            print(f"  Generated embeddings for {i + 1}/{len(products)} products")

    print(f"Generated embeddings for all {len(products)} products.")


def upload_products(search_client: SearchClient, products: list[dict[str, Any]]) -> None:
    """Upload products to the search index.

    Args:
        search_client: Azure Search Client
        products: List of product dictionaries
    """
    print(f"Uploading {len(products)} products...")

    # Upload in batches of 1000 (Azure AI Search limit)
    batch_size = 1000
    for i in range(0, len(products), batch_size):
        batch = products[i : i + batch_size]
        search_client.upload_documents(documents=batch)
        print(f"Uploaded batch {i // batch_size + 1} ({len(batch)} products)")

    print(f"Successfully uploaded {len(products)} products.")


def main() -> None:
    """Main function to create index and upload products."""
    # Get configuration from environment
    search_service = os.environ["AZURE_SEARCH_SERVICE"]
    search_api_key = os.environ["AZURE_SEARCH_API_KEY"]
    index_name = "zava-products-index"
    tenant_id = os.environ["AZURE_TENANT_ID"]

    # Create search credential
    search_credential = AzureKeyCredential(search_api_key)

    # Create clients
    search_endpoint = f"https://{search_service}.search.windows.net"
    index_client = SearchIndexClient(endpoint=search_endpoint, credential=search_credential)
    search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=search_credential)

    openai_client = OpenAI(
        base_url=f"https://{os.environ['AZURE_OPENAI_SERVICE']}.openai.azure.com/openai/v1",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Create the index
    create_index(index_client, index_name)

    # Load product data
    print("Loading product data from product_data_flat.json...")
    with open("zava_product_data/product_data_flat.json") as f:
        products = json.load(f)
    print(f"Loaded {len(products)} products.")

    # Generate embeddings
    generate_embeddings(openai_client, products)

    # Upload products
    upload_products(search_client, products)

    print("\n✓ All operations completed successfully!")
    print(f"  - Index: {index_name}")
    print(f"  - Products uploaded: {len(products)}")


if __name__ == "__main__":
    main()
