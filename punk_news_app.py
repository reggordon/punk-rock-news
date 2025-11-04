import streamlit as st
import feedparser
from datetime import datetime
import urllib.parse

def fetch_google_news_rss(query):
    """Fetch articles from Google News RSS feed"""
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(rss_url)
    return feed.entries

def main():
    st.set_page_config(
        page_title="Punk Rock News", 
        page_icon="🎸", 
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for minimal, crisp design
    st.markdown("""
        <style>
        /* Main title styling */
        h1 {
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem !important;
        }
        
        /* Remove extra padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Article title links */
        h3 a {
            text-decoration: none;
            color: #1f1f1f;
            transition: color 0.2s;
        }
        
        h3 a:hover {
            color: #666;
        }
        
        /* Hide sidebar by default */
        [data-testid="stSidebar"] {
            display: none;
        }
        
        /* Minimal dividers */
        hr {
            margin: 2rem 0;
            border: none;
            border-top: 1px solid #e0e0e0;
        }
        
        /* Clean captions */
        .stCaption {
            color: #666;
            font-size: 0.875rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🎸 Punk Rock News")
    
    # Minimal search bar
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("Search", value="punk rock", label_visibility="collapsed", placeholder="Search for news...")
    with col2:
        max_articles = st.number_input("Max", min_value=5, max_value=50, value=15, label_visibility="collapsed")
    
    st.markdown("")
    
    # Fetch and display articles
    try:
        articles = fetch_google_news_rss(query)
        
        if not articles:
            st.info("No articles found. Try a different search query.")
            return
        
        # Display articles with minimal styling
        for i, article in enumerate(articles[:max_articles]):
            # Article title
            st.markdown(f"### [{article.title}]({article.link})")
            
            # Meta info in one line
            meta_parts = []
            if hasattr(article, 'source'):
                meta_parts.append(article.source.get('title', 'Unknown'))
            if hasattr(article, 'published'):
                meta_parts.append(article.published)
            
            if meta_parts:
                st.caption(" • ".join(meta_parts))
            
            st.markdown("---")
                
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")

if __name__ == "__main__":
    main()
