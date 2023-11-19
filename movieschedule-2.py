import csv
from datetime import datetime
from itertools import combinations

# CSVファイルのパス
csv_file_path = "C:/Users/凌/Desktop/python/schedule.csv"

# 映画スケジュールのデータを保持するリスト
schedule_data = []

# CSVファイルの読み込み
with open(csv_file_path, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # ヘッダ行をスキップ
    for row in reader:
        movie_number = int(row[0])
        title = row[1]
        start_time = datetime.strptime(row[2], "%H:%M")
        end_time = datetime.strptime(row[3], "%H:%M")
        schedule_data.append({"movie_number": movie_number, "title": title, "start_time": start_time, "end_time": end_time})

# ユーザーにmovie_numberを3つ選択させる
print("以下のリストの中から3つの映画を選んでください:")
movie_numbers = []
for movie in schedule_data:
    if movie["movie_number"] not in movie_numbers:
        print(f"{movie['movie_number']}: {movie['title']}")
        movie_numbers.append(movie["movie_number"])

selected_movie_numbers = input("映画No.(例:1,2,3): ").split(",")
selected_movie_numbers = [int(number.strip()) for number in selected_movie_numbers]

print("---------------------------------------")
selected_movies = [movie for movie in schedule_data if movie["movie_number"] in selected_movie_numbers]

if len(selected_movies) < 3:
    print("映画を3つ以上選んでください")
else:
    all_combinations = list(combinations(selected_movies, 3))
    valid_combinations = []

    for combination in all_combinations:
        combination_movies = list(combination)
        combination_movies.sort(key=lambda x: x["start_time"])

        duplicate = False
        for i in range(2):
            if combination_movies[i]['end_time'] >= combination_movies[i + 1]['start_time']:
                duplicate = True
                break

        if not duplicate:
            valid_combinations.append(combination_movies)

    filtered_combinations = []
    for combination in valid_combinations:
        titles = {movie['title'] for movie in combination}
        if len(titles) == 3:
            filtered_combinations.append(combination)

    if not filtered_combinations:
        print("選択された映画の上映スケジュールが見つかりませんでした。")
    else:
        for i, combination_movies in enumerate(filtered_combinations, start=1):
            print(f"組み合わせ{i}:")
            for movie in combination_movies:
                print("映画:")
                print(f"タイトル: {movie['title']}")
                print(f"上映開始時刻: {movie['start_time'].strftime('%H:%M')}")
                print(f"上映終了時刻: {movie['end_time'].strftime('%H:%M')}")
            print("---------------------------------------")
