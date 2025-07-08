# 📰 Predicting Stock Market Movements from Financial News Headlines

**Final Project for CS1090A at Harvard University**

This project investigates how the sentiment of Yahoo Finance news headlines impacts daily fluctuations in the S&P 500 index, and how well various machine learning models can predict these changes. By aligning sentiment analysis results with stock market data, we explore patterns and correlations that can inform predictive modeling.

---

## 📌 Problem Statement

**Research Question:**  
*How does the sentiment of Yahoo financial news headlines influence fluctuations in the S&P 500 index, and to what extent can machine learning models like Linear Regression and Random Forest accurately predict these changes?*

We aim to:

- Collect and align financial news and S&P 500 index data
- Analyze the sentiment of headlines
- Train and evaluate predictive models based on this sentiment and historical market data
- Compare results across different market sectors to identify industry-specific effects

---

## 🔍 Approach

1. **Data Collection**
   - Scraped financial news headlines from Yahoo Finance
   - Retrieved corresponding S&P 500 index data
   - Aligned dates to ensure consistency

2. **Sentiment Analysis**
   - Applied NLP techniques to extract sentiment scores from headlines
   - Used pre-trained sentiment models and custom scoring

3. **Modeling**
   - Tried multiple models: Linear Regression, Random Forest, and others
   - Compared performance across models and features
   - Final model achieves **66%+ accuracy** in predicting market direction

4. **Exploration Beyond S&P 500**
   - Included analysis on industry-specific indexes
   - Investigated if certain sectors are more sentiment-sensitive

---

## 🧠 Tools & Technologies

- **Python**, **Pandas**, **NumPy**
- **NLTK**, **TextBlob**, **VADER** (for sentiment analysis)
- **Scikit-learn** (modeling)
- **Matplotlib**, **Seaborn** (visualization)

---

## 🧪 Results

- Random Forest and ensemble models performed best overall
- Clear correlations observed between sentiment scores and market changes
- Sectors like tech and energy showed greater sensitivity to sentiment shifts

---

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/SG-36/my-projects.git
   cd my-projects/yahoo_fin_news_sp500
2. Open the notebook in jupyter lab or google collab
3. Make sure you install the dependent libraries
4. Run the notebook
