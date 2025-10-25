# 🔍 Information Retrieval Search Engine

This project implements a **text-based search engine** that retrieves and ranks documents according to their relevance to a user’s query.  
It performs standard **Information Retrieval (IR)** preprocessing steps and computes document similarity using **TF-IDF** weighting and **Cosine Similarity**.

---

## 🧠 Overview

The goal of this project is to design a lightweight IR system capable of:
- Extracting and preprocessing text documents
- Building an inverted index for fast lookup
- Calculating document vectors using **TF-IDF**
- Computing similarity between a user query and documents using **cosine similarity**
- Ranking and returning the most relevant results

---

## ⚙️ Preprocessing Pipeline

The system performs multiple text normalization steps before vectorization:
- **Token Extraction**
- **Text Normalization** (lowercasing, punctuation removal)
- **Stopword Removal**
- **Rooting / Lemmatization**
- **Frequency Counting**

---

## 🏗️ Architecture

1. **Index Construction:**
   - Each document is tokenized and converted into a numeric vector (TF-IDF representation).
   - A dictionary of all unique terms is built for reference.

2. **Query Processing:**
   - The query is vectorized in the same TF-IDF space as the documents.
   - For each document vector `D`, compute similarity with the query vector `Q` using **cosine similarity**.

3. **Ranking:**
   - Documents are sorted based on similarity scores in descending order.
   - The system returns the top-k most relevant documents.

---

## 📐 Mathematical Formulation

### TF-IDF
```
tfidf(t, d, D) = tf(t, d) × idf(t, D) = (1 + log(f_t,d)) × log(N / n_t)
```

### Cosine Similarity
```
similarity(a, b) = cos(θ) = (a · b) / (||a|| ||b||)
```

---

## 🧩 Features

- Indexes and searches through plain text files
- Supports **single-word** and **multi-word queries**
- Returns ranked results based on TF-IDF similarity
- Built with Python for clarity and extendability
- Modular design for easy integration with NLP pipelines

---

## 🛠️ Technologies Used

| Component | Technology |
|------------|-------------|
| Programming Language | Python |
| Libraries | NumPy, pandas, re |
| Text Processing | Custom tokenizer & stopword remover |
| Similarity Computation | Cosine Similarity |
| Ranking | TF-IDF weighting |

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/arianmotti/InformationRetrievalEngine.git
cd InformationRetrievalEngine

# Run the search engine
python main.py
```

Then enter your query and view ranked results in the console.

---

## 📚 Example Usage

```
Query:  machine learning
Top 3 relevant documents:
1. document_05.txt  →  similarity = 0.84
2. document_02.txt  →  similarity = 0.79
3. document_07.txt  →  similarity = 0.73
```

---

## 📄 License

This project was developed as part of a university course in **Information Retrieval** at **Amirkabir University of Technology**.  
© Mohammad Mottaghi, 2024
