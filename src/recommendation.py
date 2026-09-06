"""
recommendation.py

Core recommendation pipeline for the Personalized E-Commerce Recommendation &
Ranking Engine project. Consolidates the popularity, collaborative, content-based,
and hybrid recommenders, plus cold-start routing and evaluation metrics.

This module assumes it will be imported AFTER the following objects have been
built (typically inside the project notebook, then optionally pickled for reuse):

    train_df               : cleaned, time-split training interactions
    test_df                : held-out future interactions
    user_item_matrix        : pandas DataFrame, rows=CustomerID, cols=StockCode
    item_similarity_df      : pandas DataFrame, item-item cosine similarity
    content_similarity      : numpy array, product-product TF-IDF cosine similarity
    product_catalog         : DataFrame with unique StockCode/Description rows
    product_index_map       : Series mapping StockCode -> row index in product_catalog
    popularity_df            : DataFrame with precomputed popularity scores

See the project notebook (notebooks/) for how each of these is built step by step.
"""

import math
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# STAGE 7 — Popularity baseline
# ---------------------------------------------------------------------------

def recommend_popular_products(popularity_df, n=10):
    """Return the top-N most popular products overall (non-personalized)."""
    return popularity_df.head(n)[['StockCode', 'Description', 'PopularityScore']].reset_index(drop=True)


# ---------------------------------------------------------------------------
# STAGE 8 — Collaborative filtering
# ---------------------------------------------------------------------------

def recommend_collaborative(user_id, user_item_matrix, item_similarity_df, train_df, n=10):
    """Item-based collaborative filtering recommendation for a known user."""
    if user_id not in user_item_matrix.index:
        return pd.DataFrame(columns=['StockCode', 'Description', 'Score'])

    user_row = user_item_matrix.loc[user_id]
    user_products = user_row[user_row > 0].index.tolist()
    if len(user_products) == 0:
        return pd.DataFrame(columns=['StockCode', 'Description', 'Score'])

    scores = pd.Series(dtype=float)
    for product in user_products:
        user_strength = user_row[product]
        similar_products = item_similarity_df[product] * user_strength
        scores = scores.add(similar_products, fill_value=0)

    scores = scores.drop(labels=user_products, errors='ignore')
    top_n = scores.sort_values(ascending=False).head(n)

    result = pd.DataFrame({'StockCode': top_n.index, 'Score': top_n.values})
    result = result.merge(
        train_df[['StockCode', 'Description']].drop_duplicates(),
        on='StockCode', how='left'
    )
    return result[['StockCode', 'Description', 'Score']].reset_index(drop=True)


# ---------------------------------------------------------------------------
# STAGE 9 — Content-based filtering
# ---------------------------------------------------------------------------

def recommend_content_based(product_id, product_catalog, product_index_map, content_similarity, n=10):
    """Return products textually similar to the given product via TF-IDF cosine similarity."""
    if product_id not in product_index_map.index:
        return pd.DataFrame(columns=['StockCode', 'Description', 'Score'])

    idx = product_index_map[product_id]
    if isinstance(idx, pd.Series):
        idx = idx.iloc[0]

    sim_scores = list(enumerate(content_similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] != idx][:n]

    result_indices = [s[0] for s in sim_scores]
    result_scores = [s[1] for s in sim_scores]

    result = product_catalog.iloc[result_indices][['StockCode', 'Description']].copy()
    result['Score'] = result_scores
    return result.reset_index(drop=True)


def get_content_scores(user_id, user_item_matrix, product_index_map, product_catalog, content_similarity):
    """Average content-similarity score across all products a user has interacted with."""
    if user_id not in user_item_matrix.index:
        return pd.Series(dtype=float)

    user_row = user_item_matrix.loc[user_id]
    user_products = user_row[user_row > 0].index.tolist()
    user_products = [p for p in user_products if p in product_index_map.index]
    if len(user_products) == 0:
        return pd.Series(dtype=float)

    all_scores = []
    for product in user_products:
        idx = product_index_map[product]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]
        sim_row = pd.Series(content_similarity[idx], index=product_catalog['StockCode'])
        all_scores.append(sim_row)

    combined = pd.concat(all_scores, axis=1).mean(axis=1)
    combined = combined.drop(labels=user_products, errors='ignore')
    return combined


def get_collaborative_scores(user_id, user_item_matrix, item_similarity_df):
    """Full collaborative score vector (all products) for a user, used by the hybrid model."""
    if user_id not in user_item_matrix.index:
        return pd.Series(dtype=float)

    user_row = user_item_matrix.loc[user_id]
    user_products = user_row[user_row > 0].index.tolist()
    if len(user_products) == 0:
        return pd.Series(dtype=float)

    scores = pd.Series(0.0, index=user_item_matrix.columns)
    for product in user_products:
        user_strength = user_row[product]
        scores = scores.add(item_similarity_df[product] * user_strength, fill_value=0)

    scores = scores.drop(labels=user_products, errors='ignore')
    return scores


# ---------------------------------------------------------------------------
# STAGE 10 — Hybrid recommender
# ---------------------------------------------------------------------------

def _normalize(s):
    if s.max() == s.min():
        return s * 0
    return (s - s.min()) / (s.max() - s.min())


def recommend_hybrid(user_id, user_item_matrix, item_similarity_df, product_index_map,
                      product_catalog, content_similarity, train_df,
                      n=10, collab_weight=0.6, content_weight=0.4):
    """Weighted combination of collaborative and content-based scores."""
    collab_scores = get_collaborative_scores(user_id, user_item_matrix, item_similarity_df)
    content_scores = get_content_scores(user_id, user_item_matrix, product_index_map,
                                         product_catalog, content_similarity)

    if collab_scores.empty and content_scores.empty:
        return pd.DataFrame(columns=['StockCode', 'Description', 'HybridScore'])

    all_products = collab_scores.index.union(content_scores.index)
    collab_scores = collab_scores.reindex(all_products, fill_value=0)
    content_scores = content_scores.reindex(all_products, fill_value=0)

    collab_norm = _normalize(collab_scores)
    content_norm = _normalize(content_scores)

    hybrid_scores = (collab_weight * collab_norm) + (content_weight * content_norm)
    hybrid_scores = hybrid_scores.sort_values(ascending=False).head(n)

    result = pd.DataFrame({'StockCode': hybrid_scores.index, 'HybridScore': hybrid_scores.values})
    result = result.merge(
        train_df[['StockCode', 'Description']].drop_duplicates(),
        on='StockCode', how='left'
    )
    return result[['StockCode', 'Description', 'HybridScore']].reset_index(drop=True)


# ---------------------------------------------------------------------------
# STAGE 11 — Cold-start routing
# ---------------------------------------------------------------------------

def recommend_for_user(user_id, user_item_matrix, item_similarity_df, product_index_map,
                        product_catalog, content_similarity, train_df, popularity_df, n=10):
    """Routes to hybrid (known users) or popularity fallback (cold-start users)."""
    is_known_user = user_id in user_item_matrix.index
    has_history = False
    if is_known_user:
        has_history = (user_item_matrix.loc[user_id] > 0).sum() > 0

    if has_history:
        recs = recommend_hybrid(user_id, user_item_matrix, item_similarity_df, product_index_map,
                                 product_catalog, content_similarity, train_df, n=n)
        recs['Method'] = 'Hybrid (Personalized)'
        return recs

    recs = recommend_popular_products(popularity_df, n=n)
    recs = recs.rename(columns={'PopularityScore': 'HybridScore'})
    recs['Method'] = 'Popularity (Cold-Start)'
    return recs


# ---------------------------------------------------------------------------
# STAGE 12 — Evaluation metrics
# ---------------------------------------------------------------------------

def precision_at_k(recommended, relevant, k):
    if k == 0:
        return 0.0
    recommended_k = recommended[:k]
    hits = len(set(recommended_k) & set(relevant))
    return hits / k


def recall_at_k(recommended, relevant, k):
    if len(relevant) == 0:
        return 0.0
    recommended_k = recommended[:k]
    hits = len(set(recommended_k) & set(relevant))
    return hits / len(relevant)


def ndcg_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]
    dcg = 0.0
    for i, item in enumerate(recommended_k):
        if item in relevant:
            dcg += 1 / math.log2(i + 2)
    ideal_hits = min(len(relevant), k)
    idcg = sum(1 / math.log2(i + 2) for i in range(ideal_hits))
    return dcg / idcg if idcg > 0 else 0.0


# ---------------------------------------------------------------------------
# Recommendation explanations (used by the dashboard to make results legible
# to a non-technical viewer, instead of showing raw scores with no context)
# ---------------------------------------------------------------------------

def explain_recommendation(method, collab_weight=0.6, content_weight=0.4):
    """
    Returns a short, human-readable reason for a recommendation, based on
    which method produced it. Used purely for UI presentation — it does not
    change any scoring logic.
    """
    method = (method or "").lower()

    if "hybrid" in method:
        return (f"Hybrid pick: {int(collab_weight * 100)}% based on customers with similar "
                f"purchase patterns, {int(content_weight * 100)}% based on product similarity.")
    if "collaborative" in method:
        return "Customers with similar purchase behavior also bought this."
    if "content" in method:
        return "Similar to products you've previously purchased, based on product description."
    if "popular" in method or "cold" in method:
        return "One of the most popular products overall — shown because we don't have enough purchase history for this customer yet."
    return "Recommended based on your purchase history."
