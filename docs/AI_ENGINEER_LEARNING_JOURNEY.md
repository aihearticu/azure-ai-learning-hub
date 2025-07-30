# Azure AI Engineer Learning Journey

## Overview
This document captures key learnings, troubleshooting experiences, and best practices discovered during my Azure AI Engineer certification journey.

---

## 🐳 Lab 1: Azure AI Services Containers

### Date: 2025-07-21
### Topic: Deploying Azure AI Services in Docker Containers

#### Key Learnings

1. **Container vs Cloud API**
   - **Cloud API**: Like ordering pizza delivery (needs internet)
   - **Container**: Like having a pizza oven at home (fully self-contained)
   - Containers include the ENTIRE AI model - no cloud calls needed once running

2. **Local vs Remote Endpoints**
   ```bash
   # Local Container (offline)
   http://localhost:5000/text/analytics/v3.1/sentiment
   
   # Azure Container Instance (online)
   http://azurecontainer.azurecontainer.io:5000/text/analytics/v3.1/sentiment
   ```

3. **Common Pitfalls Encountered**
   - **JSON Format Error**: Accidentally copied HTML into API key field ("404-use-a-container.html")
   - **Solution**: Always validate JSON and double-check copy-paste operations
   - **Container Initialization**: Takes 5-10 minutes to start - be patient!

4. **Sentiment Analysis Results**
   - AI accurately detected:
     - Positive sentiment: 99% confidence
     - Negative sentiment: 99% confidence  
     - Mixed sentiment: 73% positive (correctly identified overall tone)

#### Commands to Remember
```bash
# Run sentiment analysis demo
curl -X POST http://localhost:5000/text/analytics/v3.1/sentiment \
  -H "Content-Type: application/json" \
  --data '{"documents":[{"id":"1","text":"Your text here"}]}' \
  | python3 -m json.tool

# Check container status
docker ps
docker logs <container-name>
```

#### Twitter-worthy Insight
"Container = AI model you can run anywhere (planes, ships, secure facilities). No internet needed, full data privacy, consistent performance. Mind = blown 🤯"

---

## 🔍 Lab 2: Azure Cognitive Search with Custom Skills

### Date: 2025-07-21
### Topic: Building Knowledge Mining Solutions with Custom Functions

#### Key Learnings

1. **Azure Search Components**
   - **Data Source**: Where your documents live (Blob Storage)
   - **Skillset**: AI enrichment pipeline (sentiment, entities, key phrases)
   - **Index**: Searchable data structure
   - **Indexer**: Process that ties everything together

2. **Storage Connection Strings**
   - Portal format (concise): `DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=...`
   - Script format (verbose): Includes all endpoint URLs explicitly
   - Both work identically - Azure constructs endpoints automatically

3. **Custom Skill Development**
   
   **Problem**: Create word count functionality not available in built-in skills
   
   **Solution Path**:
   - Function App provides HTTP endpoint for custom processing
   - Must match Azure Cognitive Search expected schema
   - Integrate via skillset definition

4. **Troubleshooting Journey**

   **Issue 1: Region Quota**
   ```bash
   # Error: Quota exceeded for : 0 VMs allowed, 1 VMs requested
   # Solution: Try different regions programmatically
   REGIONS=("eastus2" "centralus" "westus2")
   ```

   **Issue 2: CORS Blocking**
   ```bash
   # Error: Portal requires CORS configuration
   # Solution:
   az functionapp cors add --name <app> --resource-group <rg> \
       --allowed-origins "https://portal.azure.com"
   ```

   **Issue 3: Output Format Mismatch**
   - Expected: `{ text: ["word1", "word2"] }`
   - Not: `{ wordCount: 10, topWords: "word(2)" }`
   - Lesson: Always verify integration schemas first!

#### Best Practices Discovered

1. **Automation is Key**
   - Created scripts to check region availability
   - Saved all credentials in structured formats
   - Automated CORS configuration

2. **Credential Management**
   ```bash
   # Save in multiple formats
   - AZURE_SEARCH_CREDENTIALS.md (human-readable)
   - .env (application use)
   - function-app-details.json (deployment record)
   ```

3. **Function App Requirements**
   - Always needs a storage account
   - CORS must be configured for portal testing
   - Output must match consumer's expected schema

#### Useful Script Patterns

```bash
#!/bin/bash
# Pattern: Find available Azure region
for region in "${REGIONS[@]}"; do
    if check_region_availability "$region"; then
        SELECTED_REGION=$region
        break
    fi
done

# Pattern: Safe JSON storage
cat > config.json << EOF
{
    "setting": "$VARIABLE",
    "url": "https://${DYNAMIC_URL}"
}
EOF
```

#### Architecture Insights

```
Documents (PDFs) → Blob Storage → Indexer → Skillset → Index
                                             ↓
                                    Custom Skill (Function App)
```

---

## 🎯 Key Takeaways So Far

1. **Always Check Requirements First**
   - Storage accounts for Function Apps
   - CORS for cross-domain access
   - Expected input/output schemas

2. **Automate Everything**
   - Region selection
   - Credential storage
   - Configuration updates

3. **Error Messages Are Friends**
   - "Quota exceeded" → Try different region
   - "CORS error" → Configure allowed origins
   - "Invalid JSON" → Check your copy-paste

4. **Test Incrementally**
   - Get service created
   - Fix access issues
   - Verify functionality
   - Integrate with other services

5. **Documentation Patterns**
   - Keep credentials organized
   - Document error solutions
   - Save working commands
   - Track architecture decisions

---

## 📚 Resources & References

- [Azure AI Services Containers](https://docs.microsoft.com/azure/cognitive-services/containers/)
- [Azure Cognitive Search Custom Skills](https://docs.microsoft.com/azure/search/cognitive-search-custom-skill-interface)
- [Function App CORS Configuration](https://docs.microsoft.com/azure/azure-functions/functions-how-to-use-azure-function-app-settings#cors)

---

## 📊 Lab 7: Optimize Data Indexing with Push API

### Date: 2025-07-22
### Topic: Bulk Data Indexing Optimization in Azure Cognitive Search

#### Key Learnings

1. **Batch Size Optimization**
   - Tested batch sizes from 100 to 1000 documents
   - Found optimal batch size: **900-1000 documents**
   - Best throughput achieved: **1.482 MB/second**
   - Trade-off between batch size and processing time

2. **Multi-Threading Implementation**
   - Used **8 concurrent threads** for parallel uploads
   - Result: Indexed **100,000 documents in 58.84 seconds**
   - Average time per document: **0.5884 ms**
   - Pattern: Thread pool with automatic thread replacement

3. **Performance Comparison**
   ```
   Single-threaded batch testing: ~2-3 seconds per batch
   Multi-threaded with optimization: <1 minute for 100K docs
   ```

4. **Exponential Backoff Strategy**
   - Implemented retry logic for resilient uploads
   - Prevents overwhelming the service
   - Automatic recovery from transient failures

#### Technical Implementation Details

1. **Configuration Setup**
   ```json
   {
     "SearchServiceUri": "https://acs118245-lab-search.search.windows.net",
     "SearchServiceAdminApiKey": "[API_KEY]",
     "SearchIndexName": "optimize-indexing"
   }
   ```

2. **Code Modification Pattern**
   ```csharp
   // From: Single-threaded batch testing
   await TestBatchSizesAsync(searchClient, numTries: 3);
   
   // To: Multi-threaded bulk upload
   await ExponentialBackoff.IndexDataAsync(searchClient, hotels, 1000, 8);
   ```

3. **Test Data Characteristics**
   - All 100,000 documents were identical (by design)
   - Same hotel: "Mount Rainier Lodge" in Ashford, WA
   - Only HotelId varied (0-99999)
   - Purpose: Focus on indexing performance, not data variety

#### Troubleshooting Journey

**Issue 1: Search Service Provisioning**
- Problem: Original service stuck in "provisioning" state
- Solution: Created new free-tier service for immediate availability

**Issue 2: Finding API Keys**
```bash
# Solution: Use Azure CLI
az search admin-key show --service-name "acs118245-lab-search" \
  --resource-group "cog-search-language-exe" \
  --query "primaryKey" --output tsv
```

**Issue 3: Console Input Error**
- Error: `Cannot read keys when console input has been redirected`
- Cause: Non-interactive terminal environment
- Impact: Harmless - program completed successfully

#### Best Practices Discovered

1. **Service Tier Selection**
   - Free tier sufficient for development/testing
   - Quick provisioning vs Standard tier delays

2. **Data Verification Methods**
   ```bash
   # Check index statistics via REST API
   curl -X GET "https://[service].search.windows.net/indexes/[index]/stats?api-version=2023-11-01" \
     -H "api-key: [API_KEY]"
   ```

3. **Search Query Patterns**
   ```json
   // Full-text search with highlighting
   {
     "search": "Mount St. Helens",
     "searchFields": "Description",
     "highlight": "Description"
   }
   
   // Filtering with count
   {
     "search": "*",
     "filter": "ParkingIncluded eq true",
     "count": true
   }
   ```

#### Performance Metrics Summary

| Operation | Time | Documents | Rate |
|-----------|------|-----------|------|
| Batch Testing | Variable | 100-1000 | 0.34-1.48 MB/s |
| Bulk Upload | 58.84s | 100,000 | 1,700 docs/sec |
| Per Document | 0.5884ms | 1 | N/A |

#### Architecture Insights

```
Application → Azure Search Service
    ↓              ↓
8 Threads    Exponential Backoff
    ↓              ↓
Batches      Retry Logic
(1000 docs)       ↓
    └──────→ Search Index
```

#### Key Takeaways

1. **Batch Size Matters**
   - Too small: Network overhead dominates
   - Too large: Memory/timeout issues
   - Sweet spot: 900-1000 documents

2. **Threading Transforms Performance**
   - 8x speedup with proper thread management
   - Automatic thread replacement on completion

3. **Resilience is Essential**
   - Exponential backoff prevents service overload
   - Retry logic handles transient failures

4. **Test Data Simplicity**
   - Lab exercises often use simplified data
   - Focus on the technique, not data variety
   - Real-world would have diverse documents

---

## 🔮 Lab 10: Vector Search with Azure AI Search

### Date: 2025-07-22
### Topic: Implementing Semantic Similarity Search with Vector Embeddings

#### Key Learnings

1. **Vector Search Fundamentals**
   - Converts text into 1536-dimensional vectors (embeddings)
   - Vectors represent semantic meaning, not just keywords
   - Similar meanings = similar vectors = closer in vector space
   - Uses cosine similarity to find nearest neighbors

2. **Traditional vs Vector Search**
   ```
   Traditional: "container" → finds only "container" keyword matches
   Vector: Kubernetes vector → finds App Service, Service Fabric (89% similar!)
   ```

3. **Real Results from Lab**
   
   **Finding Similar to Kubernetes:**
   - Azure Kubernetes Service: 99.99% (itself)
   - Azure App Service: 89.78% (web hosting)
   - Azure Service Fabric: 89.71% (orchestration)
   - Azure Key Vault: 88.52% (security)
   
   **Finding Similar to Machine Learning:**
   - Azure Machine Learning: 100% (itself)
   - Azure Batch AI: 93.35% (AI compute)
   - Azure Cognitive Services: 92.45% (AI APIs)

4. **Vector Search Capabilities**
   - **Pure Vector Search**: Find semantically similar documents
   - **Filtered Vector Search**: Apply metadata filters + similarity
   - **Hybrid Search**: Combine keyword search + vector similarity
   - **Cross-field Search**: Search across multiple vector fields

#### Technical Implementation

1. **Index Configuration**
   ```json
   {
     "name": "titleVector",
     "type": "Collection(Edm.Single)",
     "dimensions": 1536,
     "vectorSearchProfile": "my-vector-config"
   }
   ```

2. **Vector Search Algorithm**
   - HNSW (Hierarchical Navigable Small World)
   - Cosine similarity metric
   - Efficient approximate nearest neighbor search

3. **API Syntax Evolution**
   ```json
   // 2024 API version
   "vectorQueries": [{
     "vector": [0.00366, -0.0292, ...],
     "fields": "titleVector",
     "k": 5
   }]
   ```

#### Troubleshooting Journey

**Issue 1: API Version Compatibility**
- Problem: `vectors` parameter not recognized
- Solution: Use `vectorQueries` with 2024-07-01 API version

**Issue 2: Service Tier Requirements**
- Free tier supports vector search! ✅
- Basic tier needed for semantic ranker
- Created new service: `acs118245-semantic-search`

**Issue 3: Document Upload**
- 108 documents with embeddings (7.3MB JSON)
- Embedded in Postman collection
- Successfully bulk uploaded via REST API

#### Best Practices Discovered

1. **Vector Storage Efficiency**
   - 108 documents = 1.34MB vector index
   - Vectors are compressed and optimized
   - HNSW algorithm enables fast retrieval

2. **Search Strategy Selection**
   ```
   Use Traditional: Exact matches, specific terms
   Use Vector: Concept search, similarity, discovery
   Use Hybrid: Best of both worlds
   ```

3. **Real-World Applications**
   - **E-commerce**: "running shoes" → athletic footwear, sneakers
   - **Support**: "can't login" → authentication failed, access denied
   - **Content**: Similar articles without shared keywords

#### Architecture Insights

```
Text Input → Embedding Model → 1536D Vector → Vector Index
                                                     ↓
Query Text → Embedding Model → Query Vector → Cosine Similarity → Results
```

#### Performance Metrics

| Search Type | Response Time | Quality |
|------------|---------------|---------|
| Traditional Keyword | ~50ms | Exact matches only |
| Vector Search | ~100ms | Semantic matches |
| Hybrid Search | ~120ms | Best results |

#### Key Takeaways

1. **Semantic Understanding**
   - Finds conceptually related content
   - No shared keywords required
   - Groups similar services naturally

2. **The Power of Embeddings**
   - 1536 numbers capture meaning
   - Pre-computed for efficiency
   - Language-agnostic potential

3. **Practical Applications**
   - Better search experiences
   - Content recommendation
   - Similarity detection
   - Knowledge discovery

4. **Twitter-worthy Insight**
   "Vector search is like GPS for ideas - it finds conceptually nearby content even without matching words. Searched for Kubernetes, found App Service. Magic? No, just 1536 numbers representing meaning! 🧠🔍"

---

## 🚀 Next Labs to Explore

- [x] Optimize Data Indexing with Push API
- [x] Vector Search with Azure AI Search
- [ ] Knowledge Stores in Azure Cognitive Search
- [ ] Implementing Semantic Search
- [ ] Debug and Monitor Search Solutions

---

*This document is a living record of my Azure AI learning journey. Each lab adds new insights and patterns that build upon previous experiences.*