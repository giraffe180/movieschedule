import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://www.smt-cinema.com/site/utsunomiya/"

# Seleniumの設定
options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.get(URL)

all_sections = driver.find_elements(By.CSS_SELECTOR, "section")  # すべてのセクションを取得

movie_data = []  # 映画データを格納するリスト
movie_number = 1  # 映画番号の初期値

for section in all_sections:
    class_name = section.get_attribute("class")
    if "T0" in class_name or "A0" in class_name:  # "T0"と"A0"を含むセクションのみ処理する
        movie_title = section.find_element(By.TAG_NAME, "h2").text
        schedule_items = section.find_elements(By.CSS_SELECTOR, ".inner.ok, .block.ng")  # 上映スケジュールの要素を指定
        schedule_times = []
        for item in schedule_items:
            time_element = item.find_element(By.CSS_SELECTOR, "p.time")
            time_text = time_element.text.strip()
            time_text = time_text.replace("\n", ",")  # 改行をコンマに変更
            time_parts = time_text.split(",")  # コンマで区切って時刻を分割
            for i in range(0, len(time_parts), 2):
                start_time = time_parts[i].strip("～")
                end_time = time_parts[i + 1].strip("～")
                schedule_times.append({"start_time": start_time, "end_time": end_time})

        movie_data.append({"movie_number": movie_number, "movie_title": movie_title, "schedule_times": schedule_times})  # 映画データを追加
        movie_number += 1  # 映画番号をインクリメント

driver.quit()

#CSVファイルにデータを保存
CSV_FILE = "schedule.csv"
with open(CSV_FILE, mode='w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Movie Number', 'Movie Title', 'Start Time', 'End Time'])  # ヘッダー行を書き込み
    for movie in movie_data:
        movie_number = movie["movie_number"]
        movie_title = movie["movie_title"]
        schedule_times = movie["schedule_times"]
        for time in schedule_times:
            writer.writerow([movie_number, movie_title, time["start_time"], time["end_time"]])  # 映画番号、映画タイトル、上映開始時刻、上映終了時刻を書き込み

print("映画の上映情報をCSVファイルに保存しました。")
print("---------------------------------------")

