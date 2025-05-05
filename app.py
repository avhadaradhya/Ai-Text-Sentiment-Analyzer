import streamlit as st
from textblob import TextBlob
import re

# Set page config
st.set_page_config(
    page_title="AI Text Sentiment Analyzer",
    page_icon="😊",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .sentiment-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .positive {
        background-color: #e6ffe6;
        border-left: 5px solid #4CAF50;
    }
    .negative {
        background-color: #ffe6e6;
        border-left: 5px solid #f44336;
    }
    .neutral {
        background-color: #f0f0f0;
        border-left: 5px solid #9e9e9e;
    }
    </style>
    """, unsafe_allow_html=True)

# Header with emoji
st.markdown("# 📝 AI Text Sentiment Analyzer")
st.markdown("### Discover the emotional tone of your text")

# Description
st.markdown("""
    This app analyzes the sentiment of any text you enter. 
    It will tell you whether the text is positive, negative, or neutral.
    """)

# Text input with custom styling
st.markdown("### Enter your text below:")
user_input = st.text_area("", height=150, placeholder="Type or paste your text here...")

# Analyze button with custom styling
if st.button("🔍 Analyze Sentiment", use_container_width=True):
    if user_input:
        # Create TextBlob object
        blob = TextBlob(user_input)
        
        # Get sentiment polarity (-1 to 1)
        sentiment = blob.sentiment.polarity
        
        # Count negative words
        negative_words = ['sad', 'unhappy', 'depressed', 'miserable', 'terrible', 
                         'horrible', 'awful', 'bad', 'worst', 'pain', 'hurt',
                         'cry', 'tears', 'broken', 'heartbroken', 'disappointed',
                         'angry', 'frustrated', 'annoyed', 'upset', 'regret']
        
        # Count occurrences of negative words
        negative_count = sum(1 for word in negative_words 
                           if re.search(r'\b' + word + r'\b', user_input.lower()))
        
        # Adjust sentiment based on negative word count
        adjusted_sentiment = sentiment - (negative_count * 0.1)
        
        # Determine sentiment label and emoji
        if adjusted_sentiment > 0.1:  # Increased threshold for positive
            sentiment_label = "Positive"
            emoji = "😊"
            color = "#4CAF50"
            sentiment_class = "positive"
        elif adjusted_sentiment < -0.1:  # Increased threshold for negative
            sentiment_label = "Negative"
            emoji = "😢"
            color = "#f44336"
            sentiment_class = "negative"
        else:
            sentiment_label = "Neutral"
            emoji = "😐"
            color = "#9e9e9e"
            sentiment_class = "neutral"
        
        # Display results in a styled box
        st.markdown(f"""
            <div class="sentiment-box {sentiment_class}">
                <h2 style="color: {color}; margin: 0;">{sentiment_label} {emoji}</h2>
                <p style="margin: 5px 0;">Sentiment Score: {adjusted_sentiment:.2f}</p>
                <p style="margin: 5px 0;">Negative Words Detected: {negative_count}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional information
        st.markdown("### 📊 Analysis Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Polarity", f"{sentiment:.2f}")
        with col2:
            st.metric("Adjusted Polarity", f"{adjusted_sentiment:.2f}")
        with col3:
            st.metric("Subjectivity", f"{blob.sentiment.subjectivity:.2f}")
            
    else:
        st.warning("⚠️ Please enter some text to analyze.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and TextBlob") 