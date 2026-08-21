\# Traditional IR Baseline



\## Objective



Establish a baseline for retrieving company documents relevant to

Indian regulatory requirements.



The baseline compares two traditional information retrieval methods:



1\. TF-IDF with cosine similarity

2\. BM25



\---



\## Evaluation Dataset



The evaluation dataset contains 10 regulatory-style queries covering:



\- personal data protection

\- purpose limitation

\- data retention

\- third-party disclosure

\- security incidents

\- access control

\- third-party processors

\- marketing data usage

\- confidentiality

\- information security



Each query contains a manually defined set of relevant company documents.



\---



\## Metrics



\### Precision@5



Measures how many of the top five retrieved documents are relevant.



\### Recall@5



Measures how many of the relevant documents were retrieved in the

top five results.



\### F1@5



Harmonic mean of Precision@5 and Recall@5.



\### Mean Reciprocal Rank



Measures how early the first relevant document appears in the ranking.



\---



\## Methods



\### TF-IDF



TF-IDF represents documents using term importance and compares query

and document vectors using cosine similarity.



\### BM25



BM25 is a probabilistic lexical retrieval method that considers:



\- term frequency

\- inverse document frequency

\- document length

\- term frequency saturation



\---



\## Baseline Results



The exact numerical results are stored in:



`baseline\_results.json`



The benchmark will be used as the comparison point for future retrieval

methods.



\---



\## Expected Limitation



Traditional lexical retrieval depends heavily on vocabulary overlap.



For example:



"personal data"



and



"customer information"



may refer to similar concepts but do not share the same exact terms.



Likewise:



"technical and organizational measures"



and



"administrative and technological safeguards"



may have similar meaning despite different vocabulary.



This motivates the introduction of semantic retrieval in the next phase.



\---



\## Experimental Progression



The project will compare:



TF-IDF

&#x20;   ↓

BM25

&#x20;   ↓

Semantic Retrieval

&#x20;   ↓

Hybrid Retrieval



The final system will combine retrieval with LLM-based interpretation

rather than using the LLM as the primary search engine.

