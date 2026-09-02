import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="E-Commerce Recommendation Engine", layout="wide")


@st.cache_data
def load_data():
    train_df = pd.read_csv("artifacts/train_df.csv")
    popularity_df = pd.read_csv("artifacts/popularity_df.csv")
    product_catalog = pd.read_csv("artifacts/product_catalog.csv")
    comparison_df = pd.read_csv("artifacts/comparison_df.csv")
    with open("artifacts/user_item_matrix.pkl", "rb") as f:
        user_item_matrix = pickle.load(f)
    with open("artifacts/item_similarity_df.pkl", "rb") as f:
        item_similarity_df = pickle.load(f)
    return train_df, popularity_df, product_catalog, comparison_df, user_item_matrix, item_similarity_df


train_df, popularity_df, product_catalog, comparison_df, user_item_matrix, item_similarity_df = load_data()


def recommend_collaborative(user_id, n=10):
    if user_id not in user_item_matrix.index:
        return pd.DataFrame(columns=["StockCode", "Description", "Score"])
    user_row = user_item_matrix.loc[user_id]
    user_products = user_row[user_row > 0].index.tolist()
    if len(user_products) == 0:
        return pd.DataFrame(columns=["StockCode", "Description", "Score"])
    scores = pd.Series(dtype=float)
    for product in user_products:
        scores = scores.add(item_similarity_df[product] * user_row[product], fill_value=0)
    scores = scores.drop(labels=user_products, errors="ignore")
    top_n = scores.sort_values(ascending=False).head(n)
    result = pd.DataFrame({"StockCode": top_n.index, "Score": top_n.values})
    result = result.merge(train_df[["StockCode", "Description"]].drop_duplicates(), on="StockCode", how="left")
    return result[["StockCode", "Description", "Score"]].reset_index(drop=True)


st.title("Personalized E-Commerce Recommendation Engine")

st.sidebar.header("KPIs")
st.sidebar.metric("Total Users", train_df["CustomerID"].nunique())
st.sidebar.metric("Total Products", train_df["StockCode"].nunique())
st.sidebar.metric("Total Interactions", len(train_df))
best_row = comparison_df.loc[comparison_df["NDCG@10"].idxmax()]
st.sidebar.metric("Best Model Precision@10", f'{best_row["Precision@10"]:.3f}')
st.sidebar.metric("Best Model Recall@10", f'{best_row["Recall@10"]:.3f}')
st.sidebar.metric("Best Model NDCG@10", f'{best_row["NDCG@10"]:.3f}')

user_ids = sorted(user_item_matrix.index.tolist())
selected_user = st.selectbox("Select Customer", user_ids)

user_data = train_df[train_df["CustomerID"] == selected_user]

col1, col2 = st.columns(2)
with col1:
    st.subheader("Customer Profile")
    st.write(f"User ID: {selected_user}")
    st.write(f"Number of previous interactions: {len(user_data)}")
    st.write(f"Distinct products purchased: {user_data['StockCode'].nunique()}")

with col2:
    st.subheader("Previously Interacted Products")
    st.dataframe(
        user_data[["StockCode", "Description", "InteractionScore_capped"]]
        .sort_values("InteractionScore_capped", ascending=False)
        .head(10)
    )

st.subheader("Recommended Products")
recs = recommend_collaborative(selected_user, n=10)
recs["Method"] = "Collaborative Filtering"
st.dataframe(recs)

st.subheader("Model Comparison")
st.dataframe(comparison_df)

st.subheader("Top Popular Products")
st.bar_chart(popularity_df.head(10).set_index("Description")["PopularityScore"])
