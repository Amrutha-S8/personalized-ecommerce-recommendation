# Dashboard Screenshots Guide

## Overview

This guide walks through capturing 4 key screenshots of the Streamlit dashboard to include in your portfolio and README. These screenshots showcase the interactive features and demonstrate the recommendation engine in action.

---

## Prerequisites

1. Ensure all artifacts are generated (should already be done):
   ```bash
   python run_notebook.py
   ```

2. Start the dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

3. Dashboard opens at: `http://localhost:8501`

4. Use a screenshot tool:
   - **macOS:** Command + Shift + 4 (built-in)
   - **Windows:** Windows + Shift + S (built-in Snip & Sketch)
   - **Linux:** PrtScn or Screenshot tool
   - **Web:** F12 → Device Tools → Capture screenshot

---

## Screenshot 1: Overview Page (KPIs & Top Products)

**Path in dashboard:** Click "🏠 Overview" in the left sidebar

**What to capture:**
- The KPI cards at the top (5 metrics: Customers, Transactions, Products, Models, Best Score)
- The title "Personalized Recommendation Engine"
- The system explanation text
- Both charts: "Top-selling products" and "Transactions over time"

**Why it's important:**
- Shows the scale of the project (4K+ customers, 3.6K+ products)
- Demonstrates the best-performing model (Collaborative, NDCG@10: 0.112)
- Visual proof that real data was processed

**File name:** `overview_kpis.png`

**Dimensions:** ~1400 × 900px (full-width capture)

**Crop tips:**
- Include the Streamlit header and sidebar
- Make sure all KPI cards are fully visible
- Show both charts side-by-side

**Caption for README:**
```markdown
![Dashboard Overview - KPIs and Top Products](images/overview_kpis.png)
*Overview page showing key project metrics (4,338 customers, 3,662 products) and top-selling products chart.*
```

---

## Screenshot 2: Customer Explorer (Profile & Purchase History)

**Path in dashboard:**
1. Click "👤 Customer Explorer" in the left sidebar
2. Select a customer from the dropdown (any customer with visible history is fine)
3. Scroll down to show both the profile section and purchase history table

**What to capture:**
- The "Customer Profile" section with:
  - Customer ID
  - Country
  - Number of purchases
  - Unique products purchased
  - Total spending (in £)
  - Last purchase date
- The "Purchase History" table showing recent transactions (StockCode, Description, Quantity, UnitPrice, etc.)

**Why it's important:**
- Demonstrates the customer explorer functionality
- Shows real data from actual UK retail customers
- Illustrates how purchase history is used for personalization
- Proves the dataset contains all necessary fields

**File name:** `customer_profile.png`

**Dimensions:** ~1400 × 1000px (needs to show both sections)

**Crop tips:**
- Select a customer with 10+ purchases for a complete profile
- Include at least 5-10 rows of purchase history
- Make sure country and spending totals are visible
- Show the full metrics in KPI-style cards

**Caption for README:**
```markdown
![Customer Explorer - Purchase History](images/customer_profile.png)
*Customer profile showing purchase history, spending totals, and individual transaction details.*
```

---

## Screenshot 3: Recommendations (Personalized Picks with Explanations)

**Path in dashboard:**
1. Click "🛍️ Recommendations" in the left sidebar
2. Select a customer from the dropdown
3. Set slider to 5 recommendations
4. Wait for "Generating recommendations..." to complete
5. Scroll to show all 5 recommendation cards

**What to capture:**
- The slider for "Number of recommendations"
- The recommendation cards showing:
  - Rank icons (🥇 🥈 🥉 #4 #5)
  - Product description
  - Plain-language explanation (e.g., "Customers with similar purchase behavior also bought this")
  - Score badge (e.g., "Score: 0.485")
  - Method badge (e.g., "Hybrid")

**Why it's important:**
- **Most impressive visual** for portfolio
- Shows the personalization in action
- Demonstrates human-readable explanations (not just scores)
- Proves the hybrid recommendation approach works
- Shows the multi-modal ranking (Collaborative + Content signals)

**File name:** `recommendations_card.png`

**Dimensions:** ~1400 × 1200px (needs to show 5 cards)

**Crop tips:**
- Include the page title and slider at the top
- Make sure all 5 recommendation cards are visible
- Cards should show the medal icons, descriptions, and explanations clearly
- Try to capture a mix of personalized and popular recommendations for variety

**Caption for README:**
```markdown
![Recommendations - Personalized Products with Explanations](images/recommendations_card.png)
*Personalized product recommendations with human-readable explanations of why each product was suggested (60% collaborative filtering + 40% content-based).*
```

---

## Screenshot 4: Model Performance (Comparison Table & Chart)

**Path in dashboard:**
1. Click "📊 Model Performance" in the left sidebar
2. The table should display automatically
3. Scroll to see the comparison table fully (4 models × metrics)
4. Make sure all columns are visible: Model, Precision@5, Recall@5, NDCG@5, Precision@10, Recall@10, NDCG@10, Precision@20, Recall@20, NDCG@20

**What to capture:**
- The title "Model Performance"
- The subtitle "Best performing model (by NDCG@10): 🏆 Collaborative"
- The full comparison table highlighting the best model in green
- The bar chart below comparing models on a specific metric (should default to NDCG@10)

**Why it's important:**
- Shows rigorous evaluation methodology (Precision, Recall, NDCG metrics)
- Provides transparency on model performance trade-offs
- Proves that Collaborative Filtering outperforms baselines
- Demonstrates knowledge of ranking metrics (not classification accuracy)
- Shows all four models: Popularity, Collaborative, Content-Based, Hybrid

**File name:** `model_comparison.png`

**Dimensions:** ~1400 × 900px

**Crop tips:**
- Include the "Best performing model" highlight text
- Show the full table with all rows and key columns visible
- Include the metric selector dropdown
- Show the bar chart below the table
- Make sure the Collaborative model is highlighted in green

**Caption for README:**
```markdown
![Model Performance - Metric Comparison](images/model_comparison.png)
*Model comparison showing Collaborative Filtering as the best performer (NDCG@10: 0.112, Precision@10: 0.083) across all four approaches.*
```

---

## Optional Screenshot 5: Customer Insights (Distribution & Geography)

**Path in dashboard:**
1. Click "📈 Customer Insights" in the left sidebar
2. Two charts should display:
   - Left: "Purchases per customer (distribution)" - histogram
   - Right: "Top countries by transaction volume" - bar chart

**What to capture:**
- Both charts showing distribution and geographic data
- Demonstrates data diversity and international reach

**File name:** `customer_insights.png` (optional)

**Dimensions:** ~1400 × 600px

**Caption for README:**
```markdown
![Customer Insights - Distribution & Geography](images/customer_insights.png)
*Customer purchase distribution and top countries by transaction volume, demonstrating data diversity.*
```

---

## How to Save Screenshots

### Option 1: Direct Save (Fastest)
1. Use your OS screenshot tool (Cmd+Shift+4, Win+Shift+S, etc.)
2. Save directly to `images/` folder with the filenames above
3. Format: PNG (transparent bg, good compression)

### Option 2: Streamlit Export
1. Click the ⋮ menu in the top-right of Streamlit
2. Select "Settings" → look for screenshot/export options
3. Or use browser DevTools (F12 → Screenshot)

### Option 3: Browser Screenshot Extension
- Chrome: "Full Page Screen Capture" extension
- Firefox: Native screenshot (right-click → Take Screenshot)

---

## File Structure After Capturing

```
personalized-ecommerce-recommendation/
├── images/
│   ├── overview_kpis.png              # Required ✓
│   ├── customer_profile.png           # Required ✓
│   ├── recommendations_card.png       # Required ✓
│   ├── model_comparison.png           # Required ✓
│   └── customer_insights.png          # Optional
├── notebooks/
├── dashboard/
├── artifacts/
└── README.md
```

---

## Updating README with Screenshots

After capturing screenshots, add them to the README.md in the Dashboard section:

```markdown
## 🖥️ Dashboard

The Streamlit dashboard (`dashboard/app.py`) includes:

- **Overview** — KPIs (customers, products, transactions, model scores) and top products chart
- **Customer Explorer** — profile and purchase history for any customer, with spending totals and last purchase date
- **Recommendations** — personalized top-N picks as cards, each with a plain-language explanation of why it was recommended
- **Model Performance** — side-by-side comparison of all four models with Precision@K, Recall@K, NDCG@K metrics
- **Customer Insights** — purchase distribution, country breakdown, popularity scatter plot
- **About** — project overview and author info

### Screenshots

**Overview Page - KPIs & Product Trends**
![Dashboard Overview - KPIs and Top Products](images/overview_kpis.png)
*Project scale (4,338 customers, 3,662 products, 294K interactions) and top-selling products over time.*

**Customer Explorer - Purchase History & Profile**
![Customer Explorer - Purchase History](images/customer_profile.png)
*Individual customer profile with complete purchase history, spending totals, and transaction details.*

**Recommendations - Personalized with Explanations**
![Recommendations - Personalized Products with Explanations](images/recommendations_card.png)
*Personalized product recommendations with human-readable explanations: 60% collaborative + 40% content-based.*

**Model Performance - Metric Comparison**
![Model Performance - Metric Comparison](images/model_comparison.png)
*Rigorous evaluation: Collaborative Filtering outperforms baselines (NDCG@10: 0.112, Precision@10: 0.083).*
```

---

## Tips for Professional-Looking Screenshots

1. **Clean state:** Refresh the dashboard before taking screenshots
2. **Consistent theme:** All screenshots use Streamlit's default light theme (no dark mode)
3. **Full width:** Expand browser to ~1400px width for good readability
4. **Hide URL bar:** Use full-screen mode (F11 on most browsers)
5. **No clutter:** Close unnecessary tabs/windows
6. **Resolution:** At least 1400×900px for clarity
7. **Consistency:** Use same browser and zoom level for all screenshots

---

## Image Optimization

For GitHub/portfolio:

1. **Format:** PNG (lossless, clear, good for code/UI)
2. **Size:** Aim for <500KB per image
3. **Compression:** Use online tools like TinyPNG if needed
4. **Dimensions:** Keep aspect ratio, ~1400×900px is ideal

Command-line compression (if available):
```bash
pngquant --speed 1 --quality 85-95 image.png
# or
optipng -o2 image.png
```

---

## Checklist Before Pushing to GitHub

- [ ] All 4 required screenshots captured
- [ ] Screenshots saved in `images/` with correct filenames
- [ ] README.md updated with screenshot references
- [ ] Image files committed to git (`git add images/`)
- [ ] All links in README point to correct paths
- [ ] Images display correctly when viewing README on GitHub
- [ ] Optional: Customer Insights screenshot captured (bonus)

---

## Portfolio Talking Points

When presenting this project with screenshots:

1. **Overview:** "Built on 541K real transactions from a UK retailer, cleaned to 396K usable interactions"
2. **Scale:** "Handles 4,338 customers and 3,662 products with 98.53% sparse user-item matrix"
3. **Recommendations:** "Combined collaborative (similar customers) + content-based (similar products) filtering for robustness"
4. **Results:** "Collaborative Filtering outperformed all baselines with NDCG@10 of 0.112 in time-aware evaluation"
5. **Cold-start:** "Intelligent routing to popularity baseline for 30.7% of test customers (new users)"
6. **Explainability:** "Every recommendation includes human-readable explanation, not just a score"
7. **Production-ready:** "Graceful error handling, consistent naming, comprehensive evaluation metrics"

---

## Next Steps After Screenshots

1. Commit images to git:
   ```bash
   git add images/*.png
   git commit -m "Add dashboard screenshots for portfolio"
   ```

2. Update README with references

3. Push to GitHub:
   ```bash
   git push origin main
   ```

4. Share link with:
   - Portfolio websites
   - LinkedIn
   - GitHub profile
   - Job applications
   - Recruiters

---

## Questions?

If screenshots don't look right:
- Check that all artifacts are present in `artifacts/`
- Verify the dashboard starts without errors: `streamlit run dashboard/app.py`
- Ensure you're on a representative customer for recommendations (one with 5+ purchases)
- Try different customers if one has incomplete data

**Good luck with your portfolio! 🚀**
