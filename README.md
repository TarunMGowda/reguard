\# Reguard



\## Regulatory Compliance \& Contract Risk Auditor



Reguard is a lightweight, explainable compliance auditing system that helps organizations identify contracts and internal policies that may require review when new regulations are introduced.



The system combines:



\- Traditional Information Retrieval

\- Semantic Search

\- Hybrid Relevance Ranking

\- Local LLM-based Risk Interpretation



\## Problem



Organizations may have thousands of contracts and internal documents that need to be reviewed when new regulations or regulatory requirements are introduced.



Manually identifying affected documents can be time-consuming and error-prone.



\## Planned Solution



Reguard will:



1\. Accept a new regulatory document.

2\. Accept company contracts and internal policies.

3\. Extract regulatory requirements.

4\. Retrieve relevant clauses using traditional and semantic search.

5\. Combine retrieval signals using hybrid ranking.

6\. Use a local LLM to interpret potential compliance risks.

7\. Flag documents that may require compliance review.

8\. Present the findings through a simple user interface.



\## Project Status



Phase 1 - Project foundation and development environment.



\## Retrieval Approach



Reguard uses a staged retrieval architecture.



\### Phase 1 — Traditional Retrieval



The initial retrieval layer uses:



\- TF-IDF

\- BM25

\- cosine similarity

\- document-level relevance aggregation



\### Phase 2 — Semantic Retrieval



A lightweight locally hosted embedding model will be used to identify

semantically related regulatory requirements and company clauses even

when terminology differs.



\### Phase 3 — Hybrid Retrieval



Lexical and semantic scores will be combined to produce a final relevance

ranking.



\### Phase 4 — LLM Risk Interpretation



The LLM will not replace the retrieval system.



Instead, it will interpret the highest-ranked regulatory/document pairs

and produce:



\- relevance explanation

\- potentially affected clause

\- risk category

\- reasoning

\- recommended review priority



This separation keeps the system explainable and computationally lightweight.

