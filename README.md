# Azure AI Search Demo - Quick Start Guide

## Setup Instructions

### 1. Install Dependencies

```bash
pip install azure-search-documents python-dotenv azure-identity
```

### 2. Configure Environment Variables

1. Copy `.env.template` to `.env`:

   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and add your Azure credentials:

   ```
   AZURE_SEARCH_ENDPOINT=https://your-service.search.windows.net
   AZURE_SEARCH_KEY=your-admin-key-here
   AZURE_SEARCH_INDEX=hotels
   ```

### 3. Get Azure Search Credentials

From Azure Portal:

1. Navigate to your Azure Search service
2. Go to **Keys** section
3. Copy:
   - **URL** → `AZURE_SEARCH_ENDPOINT`
   - **Primary admin key** → `AZURE_SEARCH_KEY`
4. Note your index name → `AZURE_SEARCH_INDEX`

### 4. Update Semantic Configuration Name (if needed)

If your semantic configuration is not named "default":

- Open `azure-search-demo.ipynb`
- Find `semantic_configuration_name="default"`
- Replace with your actual semantic config name

### 5. Run the Notebook

```bash
jupyter notebook azure-search-demo.ipynb
```

Or use VS Code with Jupyter extension.

## What's Included

The notebook demonstrates:

✅ **Keyword Search** - Examples with filters, field-specific search  
✅ **Semantic Search** - Natural language queries, questions, captions  
✅ **Hybrid Search** - Combining keyword + semantic for best results  
✅ **Advanced Features** - Faceting, suggestions, scoring profiles  
✅ **Comparison Tool** - See all search types side-by-side  

## Troubleshooting

### "Connection failed" error

- Verify endpoint URL is correct (include https://)
- Ensure you're using the **admin key**, not query key
- Check index name matches exactly

### "Semantic configuration not found"

- Semantic search requires Premium tier
- Update `semantic_configuration_name` parameter
- Or skip semantic examples and use keyword search only

### "Suggester not found"

- Autocomplete requires suggester configuration in index
- Skip suggestion examples if not configured

## Next Steps

After running the demo:

1. Modify queries to search your specific hotel data
2. Experiment with filters and facets
3. Try different semantic configurations
4. Implement in your application

## Resources

- [Azure Search Documentation](https://docs.microsoft.com/azure/search/)
- [Python SDK Reference](https://docs.microsoft.com/python/api/azure-search-documents/)
- [Semantic Search Overview](https://docs.microsoft.com/azure/search/semantic-search-overview)
