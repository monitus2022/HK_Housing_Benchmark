# HK_Housing_Benchmark

Evaluate the performance of RAG text retrieval and SQL Agents.

# Components of framework:

## Documents - Estate Infos (Zh -> Zh/En)

1. Import data from S3 bucket
2. Initial local LLM (ollama)
3. Pass document to local LLM via prompt to:
- Text processing
- Handle title mismatch: reassign meaningful section titles
- Remove filler content
- Table parsing
- Score chunk relevancy (1-10)
- Select best text chunking strategy to chunk text
4. **<u>Evaluation on step 3:</u>** Pre-processing framework, using multiple model / prompt instruction (fixed chunking across vs dynamic). *--Selected estates only--*
5. Select the best preprocessing result and apply chunking
6. Perform embedding, store vectors and metadata to chromaDB
7. **<u>Evaluation on step 6:</u>** Query against embedded result, output various evaluation metrics, flagss low-quality chunks selected
8. Decide embedding approach for bilingual support: Zh embed only vs Zh/En hybrid

## SQL - Estate Infos, Market Info, Phase/Buildings Info, Transaction details

(To be added)

## Output
- Json output 