# data_rotation.py
import json
import os
import shutil

DATA_FILE = 'urls.json'

def rotate_data():
    # データファイルが1000件以上のデータを持っている場合
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # データが1000件以上ならローテーション
        if len(data) >= 1000:
            archive_file = f'urls_{len(data)}.json'
            shutil.move(DATA_FILE, archive_file)
            print(f"データがローテーションされました。{archive_file}として保存されました。")

def save_data(data):
    rotate_data()  # ローテーション確認
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
