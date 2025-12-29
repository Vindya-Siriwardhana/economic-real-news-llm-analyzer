"""
Real Economic News Web Scraper
Tries multiple sources to get real economic articles
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import xml.etree.ElementTree as ET

def scrape_guardian_business():
    """
    Scrape The Guardian Business RSS feed
    Usually works well!
    """
    print("\n📰 Trying The Guardian Business RSS...")
    
    url = "https://www.theguardian.com/business/economics/rss"
    articles = []
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item')[:15]:
            title = item.find('title')
            description = item.find('description')
            link = item.find('link')
            pubDate = item.find('pubDate')
            
            if title is not None and description is not None:
                # Clean description (remove HTML tags)
                desc_text = description.text
                if desc_text:
                    soup = BeautifulSoup(desc_text, 'html.parser')
                    clean_desc = soup.get_text()
                else:
                    clean_desc = ""
                
                article = {
                    'title': title.text if title.text else '',
                    'description': clean_desc[:300],
                    'content': clean_desc,
                    'link': link.text if link is not None and link.text else '',
                    'date': pubDate.text if pubDate is not None and pubDate.text else '',
                    'source': 'The Guardian',
                    'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                articles.append(article)
                print(f"  ✓ Got: {article['title'][:60]}...")
        
        print(f"✓ Successfully scraped {len(articles)} articles from The Guardian!")
        return articles
        
    except Exception as e:
        print(f"✗ The Guardian failed: {e}")
        return []

def scrape_ft_economics():
    """
    Try Financial Times RSS
    """
    print("\n📰 Trying Financial Times RSS...")
    
    url = "https://www.ft.com/economics?format=rss"
    articles = []
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item')[:15]:
            title = item.find('title')
            description = item.find('description')
            link = item.find('link')
            pubDate = item.find('pubDate')
            
            if title is not None:
                article = {
                    'title': title.text if title.text else '',
                    'description': description.text[:300] if description is not None and description.text else '',
                    'content': description.text if description is not None and description.text else '',
                    'link': link.text if link is not None and link.text else '',
                    'date': pubDate.text if pubDate is not None and pubDate.text else '',
                    'source': 'Financial Times',
                    'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                articles.append(article)
                print(f"  ✓ Got: {article['title'][:60]}...")
        
        print(f"✓ Successfully scraped {len(articles)} articles from FT!")
        return articles
        
    except Exception as e:
        print(f"✗ Financial Times failed: {e}")
        return []

def scrape_reuters_business():
    """
    Try Reuters RSS
    """
    print("\n📰 Trying Reuters Business RSS...")
    
    url = "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best"
    articles = []
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item')[:15]:
            title = item.find('title')
            description = item.find('description')
            link = item.find('link')
            pubDate = item.find('pubDate')
            
            if title is not None:
                article = {
                    'title': title.text if title.text else '',
                    'description': description.text[:300] if description is not None and description.text else '',
                    'content': description.text if description is not None and description.text else '',
                    'link': link.text if link is not None and link.text else '',
                    'date': pubDate.text if pubDate is not None and pubDate.text else '',
                    'source': 'Reuters',
                    'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                articles.append(article)
                print(f"  ✓ Got: {article['title'][:60]}...")
        
        print(f"✓ Successfully scraped {len(articles)} articles from Reuters!")
        return articles
        
    except Exception as e:
        print(f"✗ Reuters failed: {e}")
        return []

def scrape_google_news():
    """
    Google News RSS - Economics topic
    Usually reliable!
    """
    print("\n📰 Trying Google News RSS...")
    
    url = "https://news.google.com/rss/search?q=economics+when:7d&hl=en-US&gl=US&ceid=US:en"
    articles = []
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item')[:20]:
            title = item.find('title')
            description = item.find('description')
            link = item.find('link')
            pubDate = item.find('pubDate')
            source_elem = item.find('source')
            
            if title is not None:
                article = {
                    'title': title.text if title.text else '',
                    'description': description.text[:300] if description is not None and description.text else '',
                    'content': description.text if description is not None and description.text else title.text,
                    'link': link.text if link is not None and link.text else '',
                    'date': pubDate.text if pubDate is not None and pubDate.text else '',
                    'source': source_elem.text if source_elem is not None and source_elem.text else 'Google News',
                    'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                articles.append(article)
                print(f"  ✓ Got: {article['title'][:60]}...")
        
        print(f"✓ Successfully scraped {len(articles)} articles from Google News!")
        return articles
        
    except Exception as e:
        print(f"✗ Google News failed: {e}")
        return []

def scrape_all_sources():
    """
    Try all sources and combine results
    """
    print("=" * 70)
    print("REAL ECONOMIC NEWS SCRAPER")
    print("=" * 70)
    print("\nTrying multiple sources...")
    
    all_articles = []
    
    # Try each source
    sources = [
        scrape_google_news,      # Try Google News first (most reliable)
        scrape_guardian_business, # Then Guardian
        scrape_reuters_business,  # Then Reuters
        scrape_ft_economics       # Finally FT
    ]
    
    for scraper in sources:
        articles = scraper()
        all_articles.extend(articles)
        time.sleep(2)  # Be polite - wait between requests
        
        # If we have enough articles, stop
        if len(all_articles) >= 30:
            break
    
    print("\n" + "=" * 70)
    print(f"TOTAL ARTICLES COLLECTED: {len(all_articles)}")
    print("=" * 70)
    
    if len(all_articles) == 0:
        print("\n⚠️  WARNING: No articles collected!")
        print("This might be due to:")
        print("- Network restrictions")
        print("- Website blocking")
        print("- RSS feed changes")
        print("\nFallback: Will need to use NewsAPI or sample data")
    
    return all_articles

def save_articles(articles, filename='../data/scraped_articles.csv'):
    """
    Save scraped articles to CSV
    """
    if not articles:
        print("\n❌ No articles to save!")
        return
    
    df = pd.DataFrame(articles)
    
    # Clean up and standardize
    df['id'] = ['R' + str(i+1).zfill(3) for i in range(len(df))]
    df = df[['id', 'title', 'description', 'content', 'source', 'date', 'link', 'scraped_date']]
    
    # Save
    df.to_csv(filename, index=False)
    print(f"\n✓ Saved {len(articles)} articles to: {filename}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SCRAPING SUMMARY")
    print("=" * 70)
    print(f"\nTotal articles: {len(df)}")
    print(f"\nBy source:")
    print(df['source'].value_counts())
    print("=" * 70)
    
    return df

if __name__ == "__main__":
    print("\n🚀 Starting Real News Scraper...")
    print("This will try multiple sources to get real economic articles")
    
    # Scrape articles
    articles = scrape_all_sources()
    
    # Save results
    if articles:
        df = save_articles(articles)
        print("\n✅ Scraping complete!")
        print("\nNext steps:")
        print("1. Check: data/scraped_articles.csv")
        print("2. Run LLM categorization on these real articles")
        print("3. Build dashboard to visualize results")
    else:
        print("\n⚠️  No articles collected. Try:")
        print("1. Check your internet connection")
        print("2. Try running again later")
        print("3. Consider using NewsAPI as backup")
