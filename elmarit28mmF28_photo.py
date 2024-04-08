import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ページ設定を"wide mode"に設定
st.set_page_config(layout="wide")

# Flickr APIの設定
API_KEY = st.secrets["flickr_api_key"]
API_URL = 'https://www.flickr.com/services/rest/'

def fetch_images(text, per_page=300):
    """Flickrから画像を検索してURLリストを取得"""
    params = {
        'method': 'flickr.photos.search',
        'api_key': API_KEY,
        'text': text,
        'safe_search': 1,
        'content_type': 1,
        'media': 'photos',
        'per_page': per_page,
        'sort': 'random',  # 投稿順をランダムに設定
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
    st.title('Elmarit 28mm f2.8 example photo')

    # レンズバージョンの選択セレクトボックス
    lens_version = st.selectbox("Please select lens version :", ['','1st', '2nd', '3rd', 'ASPH'])

    # SEARCH_TEXTの動的な設定
    if lens_version == '1st':
        SEARCH_TEXT = 'Elmarit 28mm f2.8 1st OR Elmarit 28mm f2.8 first'
    elif lens_version == '2nd':
        SEARCH_TEXT = 'Elmarit 28mm f2.8 2nd OR Elmarit 28mm f2.8 second'
    elif lens_version == '3rd':
        SEARCH_TEXT = 'Elmarit 28mm f2.8 3rd OR Elmarit 28mm f2.8 third'
    elif lens_version == 'ASPH':
        SEARCH_TEXT = 'Elmarit 28mm f2.8 ASPH OR Elmarit 28mm f2.8 Aspherical'

    # セレクトボックスの選択をトリガーとして検索を実行
    if lens_version:
        urls = fetch_images(SEARCH_TEXT)
        if urls:
            display_images(urls)
        else:
            st.write('画像が見つかりませんでした。')

if __name__ == '__main__':
    main()
