import streamlit as st
from group import (load_groups_from_csv)
from rating import (load_ratings_from_csv)
import io
import pandas as pd

def display_rank():
    """显示选手排名"""
    load_groups_from_csv("datas/groups_data.csv")  # 从 CSV 文件加载数据
    load_ratings_from_csv("datas/ratings_data.csv")

    st.header("排名")
    players = st.session_state.players.players

    # 排序选手，根据评分从高到低排序
    players.sort(key=lambda x: x.score, reverse=True)

    # 记录当前排名和上一个选手的评分
    current_rank = 0
    last_score = None
    rank_count = 0

    # 生成排名并保存数据
    ranking_data = []
    for player in players:
        rank_count += 1
        if last_score is None or player.score != last_score:
            current_rank = rank_count
            last_score = player.score

        ranking_data.append({"排名": current_rank, "姓名": player.name, "平均得分": player.score, "备注": player.view})
        st.text(f"{current_rank}. {player}")

    return ranking_data

def data_rank():
    """显示选手排名"""
    load_groups_from_csv("datas/groups_data.csv")  # 从 CSV 文件加载数据
    load_ratings_from_csv("datas/ratings_data.csv")

    st.header("排名")
    players = st.session_state.players.players

    # 排序选手，根据评分从高到低排序
    players.sort(key=lambda x: x.score, reverse=True)

    # 记录当前排名和上一个选手的评分
    current_rank = 0
    last_score = None
    rank_count = 0

    # 生成排名并保存数据
    ranking_data = []
    for player in players:
        rank_count += 1
        if last_score is None or player.score != last_score:
            current_rank = rank_count
            last_score = player.score

        ranking_data.append({"排名": current_rank, "姓名": player.name, "平均得分": player.score, "备注": player.view})

    return ranking_data

def download_rankings():
    """下载排名数据为 CSV 文件"""
    ranking_data = data_rank()
    df = pd.DataFrame(ranking_data)

    # Convert DataFrame to CSV format
    csv = df.to_csv(index=False)

    # Create a BytesIO object
    buffer = io.BytesIO()
    buffer.write(csv.encode())
    buffer.seek(0)

    st.download_button(
        label="下载排名结果为 CSV 文件",
        data=buffer,
        file_name='rankings.csv',
        mime='text/csv'
    )

