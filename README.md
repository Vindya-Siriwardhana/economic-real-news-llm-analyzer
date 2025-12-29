# 📊 Economic News LLM Analyzer

An end-to-end data pipeline that scrapes real economic news, categorizes them using GPT-3.5, and visualizes results through an interactive dashboard.

## 🎯 Project Overview

This project demonstrates a production-ready approach to automated news categorization:
- **Real-time web scraping** from multiple economic news sources
- **LLM-powered categorization** using OpenAI's GPT-3.5
- **Interactive dashboard** for exploring and analyzing results

**Live Demo:** [View Dashboard](https://economic-real-news-llm-analyzer-ayk7twvmutf92aaxwts7et.streamlit.app/)

## ✨ Features

- 🔍 **Multi-Source Scraping**: Automatically collects articles from The Guardian, Google News, Reuters, and more
- 🤖 **AI Categorization**: Uses GPT-3.5 to classify articles into 10 economic categories
- 📊 **Interactive Visualizations**: Dynamic charts and filters powered by Plotly
- 🔎 **Smart Search**: Find articles by keywords across titles and descriptions
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Web RSS   │──────▶│   Scraping   │──────▶│  CSV Data   │
│   Feeds     │      │   Pipeline   │      │   Storage   │
└─────────────┘      └──────────────┘      └─────────────┘
                                                    │
                                                    ▼
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Dashboard  │◀─────│ Categorized  │◀─────│  OpenAI     │
│  (Streamlit)│      │   Articles   │      │  GPT-3.5    │
└─────────────┘      └──────────────┘      └─────────────┘
```

## 🗂️ Economic Categories

- **Inflation**: CPI, price changes, inflation rates
- **Monetary Policy**: Central bank decisions, interest rates
- **GDP Growth**: Economic growth, recession/expansion indicators
- **Employment**: Jobs, unemployment, labor market trends
- **Trade**: Imports, exports, trade balances
- **Housing**: Property markets, home prices, mortgages
- **Commodities**: Oil, gold, agricultural products
- **Financial Markets**: Stock markets, currencies, crypto
- **Productivity**: Economic efficiency, tech investment
- **General Economics**: Economic theory and education

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Internet connection

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/economic-real-news-llm-analyzer.git
cd economic-real-news-llm-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the scraping pipeline**
```bash
cd scripts
python scrape_real_news.py
```

4. **Categorize articles with LLM**
```bash
python categorize_real_articles.py
# Enter your OpenAI API key when prompted
```

5. **Launch the dashboard**
```bash
cd ..
streamlit run dashboard.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 📁 Project Structure

```
economic-real-news-llm-analyzer/
├── data/
│   ├── scraped_articles.csv          # Raw scraped articles
│   └── categorized_real_articles.csv # LLM-categorized articles
├── scripts/
│   ├── scrape_real_news.py          # Web scraping script
│   └── categorize_real_articles.py  # LLM categorization script
├── dashboard.py                      # Streamlit dashboard
├── requirements.txt                  # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Pandas** | Data manipulation and analysis |
| **BeautifulSoup** | HTML parsing for web scraping |
| **Requests** | HTTP library for fetching web content |
| **OpenAI API** | GPT-3.5 for article categorization |
| **Streamlit** | Interactive web dashboard framework |
| **Plotly** | Interactive data visualizations |

## 📊 Sample Results

The system successfully processes real economic news:

- **35+ articles** collected from 20+ sources
- **90%+ accuracy** in categorization (validated against manual labels)
- **Sub-second** categorization per article
- **Interactive filtering** by category and source

## 🎓 Key Learnings

This project demonstrates:

- **Production-ready data pipelines**: Robust error handling and multi-source fallbacks
- **LLM integration**: Effective prompt engineering for consistent categorization
- **Web scraping**: Ethical RSS feed consumption with rate limiting
- **Data visualization**: Creating intuitive, interactive dashboards
- **Software engineering**: Clean code structure, documentation, and deployment

## 🔮 Future Enhancements

- [ ] Add sentiment analysis for each article
- [ ] Implement trend detection over time
- [ ] Create email alerts for specific categories
- [ ] Add more news sources
- [ ] Build RESTful API for categorization service
- [ ] Integrate with database (PostgreSQL)

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Vindya**
- Data Scientist with expertise in LLM integration and data analysis
- MSc Data Science (University of Essex, 2023)
- Currently seeking Data Analyst/Scientist roles in the UK

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## ⭐ Show Your Support

If you found this project helpful, please give it a star on GitHub!

---

*Built with ❤️ as a portfolio project demonstrating end-to-end data science capabilities*
