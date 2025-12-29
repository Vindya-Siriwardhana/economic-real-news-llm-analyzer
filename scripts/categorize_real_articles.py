"""
LLM Categorization for Real Scraped Articles
Uses OpenAI API to categorize real economic news
"""

import pandas as pd
import time
from openai import OpenAI

# Economic categories
ECONOMIC_CATEGORIES = [
    'inflation',
    'monetary_policy', 
    'gdp_growth',
    'employment',
    'trade',
    'housing',
    'commodities',
    'financial_markets',
    'productivity',
    'general_economics'  # For articles that don't fit other categories
]

def setup_openai_client(api_key):
    """Initialize OpenAI client"""
    return OpenAI(api_key=api_key)

def categorize_article(client, title, description):
    """
    Use LLM to categorize a single article
    """
    
    prompt = f"""You are an economic analyst. Categorize this economic news article into ONE of these categories:

Categories:
- inflation: CPI, price changes, inflation rates
- monetary_policy: Central bank decisions, interest rates, policy changes
- gdp_growth: Economic growth, GDP reports, recession/expansion
- employment: Jobs, unemployment, labor market, wages
- trade: Imports, exports, trade balances, tariffs
- housing: Property markets, home prices, mortgages
- commodities: Oil, gold, agricultural products, raw materials
- financial_markets: Stock markets, currencies, crypto, market volatility
- productivity: Economic efficiency, tech investment, output per worker
- general_economics: Economic theory, general economic discussion, economic education

Article:
Title: {title}
Description: {description}

Respond with ONLY the category name, nothing else."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert economic analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=20
        )
        
        category = response.choices[0].message.content.strip().lower()
        
        if category in ECONOMIC_CATEGORIES:
            return category
        else:
            return 'general_economics'
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 'error'

def categorize_scraped_articles(api_key):
    """
    Categorize all scraped articles
    """
    
    print("=" * 70)
    print("LLM CATEGORIZATION - REAL ARTICLES")
    print("=" * 70)
    
    # Connect to OpenAI
    print("\n🔑 Connecting to OpenAI...")
    client = setup_openai_client(api_key)
    print("✓ Connected!")
    
    # Load scraped articles
    print("\n📂 Loading real articles...")
    df = pd.read_csv('../data/scraped_articles.csv')
    print(f"✓ Loaded {len(df)} real articles!")
    
    # Categorize
    print("\n🤖 Starting LLM categorization...\n")
    
    categories = []
    
    for idx, row in df.iterrows():
        article_id = row['id']
        title = row['title']
        description = row['description'] if pd.notna(row['description']) else title
        
        category = categorize_article(client, title, description)
        categories.append(category)
        
        print(f"[{idx+1}/{len(df)}] {article_id}: {title[:50]}... → {category}")
        
        time.sleep(0.5)  # Rate limit
    
    # Add categories
    df['llm_category'] = categories
    
    # Save
    output_path = '../data/categorized_real_articles.csv'
    df.to_csv(output_path, index=False)
    
    print("\n" + "=" * 70)
    print("✅ CATEGORIZATION COMPLETE!")
    print("=" * 70)
    print(f"\n✓ Saved to: {output_path}")
    
    # Summary
    print("\n📊 CATEGORY DISTRIBUTION:")
    print(df['llm_category'].value_counts())
    
    print("\n" + "=" * 70)
    
    return df

if __name__ == "__main__":
    print("\n🚀 Real Article LLM Categorization")
    print("=" * 70)
    
    # Get API key
    print("\n🔑 Enter your OpenAI API key:")
    api_key = input("API Key: ").strip()
    
    if not api_key.startswith('sk-'):
        print("\n❌ Invalid API key!")
        exit(1)
    
    # Run
    try:
        df = categorize_scraped_articles(api_key)
        
        print("\n✅ All done!")
        print("\nNext steps:")
        print("1. Check: data/categorized_real_articles.csv")
        print("2. Build dashboard to visualize these real results!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
