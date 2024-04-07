import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ページ設定を"wide mode"に設定
st.set_page_config(layout="wide")

# Flickr APIの設定
API_KEY = st.secrets["flickr_api_key"]
API_URL = 'https://www.flickr.com/services/rest/'
SEARCH_TEXT = 'Elmarit 28mm f2.8 2nd'

def fetch_images(text, per_page=100):
    """Flickrから画像を検索してURLリストを取得"""
    params = {
        'method': 'flickr.photos.search',
        'api_key': API_KEY,
        'text': text,
        'safe_search': 1,
        'content_type': 1,
        'media': 'photos',
        'per_page': per_page,
        'sort': 'date-posted-desc',  # 検索結果を最新のものに限定
        'format': 'json',
        'nojsoncallback': 1
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    urls = []
    for photo in data['photos']['photo']:
        url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_b.jpg"
        urls.append(url)
    return urls

def display_images(urls):
    """画像URLのリストを受け取り、Streamlitで表示"""
    for url in urls:
        image = Image.open(BytesIO(requests.get(url).content))
        st.image(image, use_column_width=True)

def main():
    st.title('Elmarit 28mm f2.8 2nd example photo')
    urls = fetch_images(SEARCH_TEXT)
    if urls:
        display_images(urls)
    else:
        st.write('画像が見つかりませんでした。')

if __name__ == '__main__':
    main()
