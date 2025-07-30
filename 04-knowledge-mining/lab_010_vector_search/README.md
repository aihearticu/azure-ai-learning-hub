# Lab 010: Vector Search with Azure AI Search

## Metadata
- **Date Completed**: 2025-07-22
- **Category**: Search
- **Difficulty**: Advanced
- **Time Taken**: 3 hours
- **Prerequisites**: 
  - Azure Cognitive Search basics
  - Understanding of embeddings/vectors
  - REST API knowledge

## Azure Services Used
- **Primary**: Azure Cognitive Search (Basic tier)
- **Supporting**: Postman, REST APIs
- **Cost Estimate**: $75/month (Basic tier) or Free tier compatible

## Business Scenario
### Problem Statement
Traditional keyword search misses semantically related content. Users searching for "running shoes" won't find "athletic footwear" or "jogging sneakers."

### Use Cases
- E-commerce product discovery
- Customer support ticket routing
- Content recommendation systems
- Knowledge base semantic search

## Implementation Summary

### Key Results
- Created vector search index with 108 Azure service documents
- Each document has 1536-dimensional embeddings
- Implemented pure vector, filtered, hybrid, and cross-field search

### Performance Achieved
```
Search Type         | Response Time | Quality
--------------------|---------------|------------------
Traditional Keyword | ~50ms         | Exact matches only
Vector Search       | ~100ms        | Semantic matches
Hybrid Search       | ~120ms        | Best results
```

## Key Code Pattern
```json
{
  "vectorQueries": [{
    "vector": [0.00366, -0.0292, ...],
    "fields": "titleVector",
    "k": 5
  }],
  "filter": "category eq 'Compute'",
  "select": "id,title,category"
}
```

## Major Learning
When searching for services similar to "Azure Kubernetes Service", vector search found:
- Azure App Service (89.78% similar)
- Azure Service Fabric (89.71% similar)

These are conceptually related (container/app hosting) without sharing keywords!

## Files
- [Full Results](../../mslearn-knowledge-mining/Labfiles/10-vector-search/vector-search-results.md)
- [Demo Scripts](../../mslearn-knowledge-mining/Labfiles/10-vector-search/vector-search-demo.sh)
- [Code Examples](../../mslearn-knowledge-mining/Labfiles/10-vector-search/vector-search-code-examples.md)

## Twitter Summary
"Vector search is GPS for ideas - finds conceptually nearby content without matching words. Searched for Kubernetes, found App Service. Magic? No, just 1536 numbers! 🧠🔍"

---
*Part of Azure AI Engineer Learning Journey*