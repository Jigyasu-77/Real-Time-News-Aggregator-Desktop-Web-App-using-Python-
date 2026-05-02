
import streamlit as st
import requests
import xml.etree.ElementTree as ET
import re

st.set_page_config(page_title="Top Real 20 News", layout="wide")

st.title("This is real top 20 news")

url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
response = requests.get(url)
root = ET.fromstring(response.content)

articles = []

for item in root.findall('.//item')[:20]:
    title = item.find('title').text
    desc = item.find('description').text or ""
    clean_desc = re.sub('<.*?>', '', desc)

    articles.append({
        "title": title,
        "description": clean_desc,
        "url": item.find('link').text
    })

for i, article in enumerate(articles):
    st.subheader(f"{i+1}. {article['title']}")
    st.write(article["description"])
    st.markdown(f"[Read More]({article['url']})")
    st.divider()