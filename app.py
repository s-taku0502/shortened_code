# app.py
from flask import Flask, render_template, request, redirect
import secrets
import string
import json
import os
from data_rotation import save_data  # data_rotation.pyをインポート

app = Flask(__name__)

DATA_FILE = 'urls.json'

# 短縮URLを生成（ランダム6文字）
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits  # 英数字（大小文字＋数字）
    return ''.join(secrets.choice(characters) for _ in range(length))

# 短縮URLと元のURLをJSONファイルに保存
def save_url_mapping(short_url, original_url):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {}

    data[short_url] = original_url
    save_data(data)  # data_rotation.pyを使って保存時にローテーションを実行

# ホームページ（URL入力＆短縮処理）
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        short_url = generate_short_url()
        save_url_mapping(short_url, original_url)
        return render_template('index.html', short_url=short_url)

    return render_template('index.html', short_url=None)

# 短縮URLアクセス時にリダイレクト
@app.route('/<short_url>')
def redirect_to_original(short_url):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if short_url in data:
            return redirect(data[short_url])

    return "短縮URLが見つかりません", 404

if __name__ == '__main__':
    app.run(debug=True)
