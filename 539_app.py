import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

st.title("今彩539均質預測")

def fetch_lottery_data():
    url = 'https://www.taiwanlottery.com.tw/lotto/dailycash/history.aspx'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    result = []

    for td in soup.find_all('td'):
        if '開出順序' in td.text:
            for num in td.find_next_siblings('td'):
                span = num.find('span')
                if span is not None:
                    result.append(int(span.text))

    result = [sorted(result[i:i+5]) for i in range(0, len(result), 5)]

    return result

result = fetch_lottery_data()

st.subheader("最近10組今彩539號碼:")
st.table(pd.DataFrame(result, columns=["1st", "2nd", "3rd", "4th", "5th"]))

def calculate_centroids(data):
    unique_numbers = sorted(set(sum(data, [])))
    ranges = [(1, 8), (9, 16), (17, 24), (25, 32), (33, 39)]
    centroid_1 = []
    for start, end in ranges:
        numbers_in_range = [num for num in unique_numbers if start <= num <= end]
        if numbers_in_range:
            centroid_1.append(round(sum(numbers_in_range) / len(numbers_in_range)))

    sorted_data = [sorted(sub_list) for sub_list in data]
    centroid_2 = []
    for i in range(len(sorted_data[0])):
        avg = round(sum(sub_list[i] for sub_list in sorted_data) / len(sorted_data))
        centroid_2.append(avg)
    centroid_2.sort()

    combined_centroids = centroid_1 + centroid_2
    centroid_3 = []
    for start, end in ranges:
        numbers_in_range = [num for num in combined_centroids if start <= num <= end]
        if numbers_in_range:
            centroid_3.append(round(sum(numbers_in_range) / len(numbers_in_range)))

    return centroid_3

st.subheader("均質預測號碼與今彩539號碼:")
comparison_data = []
latest_prediction = calculate_centroids(result[:3])
comparison_data.append({"Predicted": latest_prediction, "Actual": None})

for i in range(len(result) - 2):
    data = result[i:i + 3]
    centroid_3 = calculate_centroids(data)
    comparison_data.append({"Predicted": centroid_3, "Actual": result[i]})

comparison_df = pd.DataFrame(comparison_data)
st.table(comparison_df)
