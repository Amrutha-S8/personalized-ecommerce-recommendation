# Personalized E-Commerce Recommendation & Ranking Engine

## Overview
An end-to-end recommendation system that suggests relevant products to individual
customers based on their purchase history and product content, built on real
UK online-retailer transaction data.

## Problem Statement
E-commerce platforms lose engagement and revenue when customers can't easily
discover products relevant to them. This project builds a recommendation
pipeline that combines collaborative filtering, content-based filtering, and
a hybrid ranking approach to solve this.

## Business Motivation
Personalized recommendations drive cross-selling, repeat purchases, and
improved product discovery — directly impacting revenue per customer.

## Dataset
[UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)
— ~540K real transactions from a UK-based online gift retailer (Dec 2010–Dec 2011).
See `data/README.md` for download instructions. Raw data is not committed to this repo.

## Features
- End-to-end data cleaning pipeline for real, messy transactional data
- Implicit feedback modeling (no explicit ratings available in this dataset)
- Time-aware train/test split to avoid data leakage
- Popularity, Collaborative Filtering, Content-Based, and Hybrid recommenders
- Cold-start handling for new users and new products
- Full evaluation suite: Precision@K, Recall@K, NDCG@K
- Interactive Streamlit dashboard

## Technologies
Python, Pandas, NumPy, Scikit-learn, NLTK, Matplotlib/Seaborn, Streamlit

## Architecture
Data Ingestion → Cleaning → EDA → Interaction Table → Time-Aware Split →
[Popularity | Collaborative | Content-Based] → Hybrid Scoring →
Cold-Start Routing → Evaluation → Dashboard

## EDA Highlights
- User-item matrix sparsity: `[FILL IN FROM YOUR NOTEBOOK STEP 8a OUTPUT]`
- Long-tail product distribution observed (see `images/eda.png` once exported)
- Seasonal transaction trend observed (see notebook EDA section)

## Recommendation Methods
- **Popularity Baseline**: reach + volume weighted scoring
- **Collaborative Filtering**: item-based cosine similarity on implicit interactions
- **Content-Based Filtering**: TF-IDF (1–2 grams) on product descriptions
- **Hybrid**: weighted combination (0.6 collaborative / 0.4 content, tunable)

## Evaluation Metrics
Precision@K, Recall@K, and NDCG@K were used instead of accuracy, since
recommendation is a ranking problem, not a classification problem.

## Results
See `results/model_comparison.csv` — **this file must be replaced with your own
notebook's actual output**. No fabricated numbers are included in this template.

## Dashboard
Interactive Streamlit app (`dashboard/app.py`) — customer selection, profile,
purchase history, live recommendations, and model KPIs.

## Installation
```bash
git clone <this-repo-url>
cd personalized-ecommerce-recommendation
pip install -r requirements.txt
```

## Usage
1. Download the dataset per `data/README.md`
2. Run the notebook in `notebooks/` end-to-end to generate `artifacts/` used by the dashboard
3. Launch the dashboard: `streamlit run dashboard/app.py`

## Project Structure
```
personalized-ecommerce-recommendation/
├── notebooks/
├── data/
├── src/
├── dashboard/
├── results/
├── images/
├── requirements.txt
├── README.md
└── .gitignore
```

## Limitations
- No explicit ratings — implicit feedback introduces noise (a purchase isn't always "liked")
- Content-based filtering relies on product titles only (no category/brand/description fields available in the source dataset)
- Dataset is UK-dominated, limiting geographic generalization
- Item-item similarity matrix is dense and may not scale to catalogs with millions of products without a sparse/ANN-based approach

## Future Improvements
- Matrix factorization (ALS/SVD) for collaborative filtering
- Learned hybrid weights instead of fixed weights
- Approximate nearest neighbor search (FAISS) for scalability
- A/B testing framework to validate offline metrics against real engagement

## Author
`[Your Name]` — Independent Data Science Project
