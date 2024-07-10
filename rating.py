import streamlit as st
import pandas as pd
from group import (load_groups_from_csv)
from player import (display_players)
def rate_player():
    """评分选手"""
    load_groups_from_csv("datas/groups_data.csv")
    load_ratings_from_csv("datas/ratings_data.csv")
    st.header("选手评分")
    player_id = st.number_input("输入选手编号", min_value=0)
    player_name = st.session_state.players.get_name(player_id)
    rater_name = st.text_input("输入打分人名字")
    rating1 = st.number_input("情感带入（0-10）", min_value=0, max_value=10)
    rating2 = st.number_input("动作符合人物（0-10）", min_value=0, max_value=10)
    rating3 = st.number_input("体态、习惯（0-10）", min_value=0, max_value=10)
    rating4 = st.number_input("沟通能力（0-10）", min_value=0, max_value=10)
    rating5 = st.number_input("个人形象（0-10）", min_value=0, max_value=10)
    rating6 = st.text_input("备注（可不填）")

    if st.button("确定"):
        # 在这里添加选手评分逻辑
        load_groups_from_csv("datas/groups_data.csv")
        load_ratings_from_csv("datas/ratings_data.csv")
        rating = (rating1 + rating2 + rating3 + rating4 + rating5) * 2
        if player_name == None:
            raise ValueError(f"找不到编号为{player_id}的选手")
        st.session_state.ratings[player_name + "+" + rater_name] = [rating, rating6]
        st.session_state.players.update_rating(player_id, st.session_state.ratings)
        save_ratings_to_csv("datas/ratings_data.csv")
        st.write(f"{rater_name} 对  {player_name} 的评分是 {rating}")
    display_players()


def delete_rating():
    """删除选手评分"""
    load_groups_from_csv("datas/groups_data.csv")
    load_ratings_from_csv("datas/ratings_data.csv")
    st.header("删除评分")
    player_id_1 = st.number_input("输入要删除评分的选手编号", min_value=0)
    player_name_1 = st.session_state.players.get_name(player_id_1)
    rater_name_1 = st.text_input("输入相应打分人名字")
    if st.button("确定", key='button1'):
        # 在这里添加删除评分逻辑
        load_groups_from_csv("datas/groups_data.csv")
        load_ratings_from_csv("datas/ratings_data.csv")
        del st.session_state.ratings[player_name_1 + "+" + rater_name_1]
        st.session_state.players.update_rating(player_id_1, st.session_state.ratings)
        save_ratings_to_csv("datas/ratings_data.csv")
        st.write(f"{rater_name_1} 对 {player_name_1} 的评分已删除")

    st.header("评分重置")
    player_id_2 = st.number_input("输入要重置评分的选手编号", min_value=0)
    player_name_2 = st.session_state.players.get_name(player_id_2)
    if st.button("确定", key='button2'):
        # 在这里添加重置评分逻辑
        load_groups_from_csv("datas/groups_data.csv")
        load_ratings_from_csv("datas/ratings_data.csv")
        rating_keys = list(st.session_state.ratings.keys())  # 将字典的键转换为列表
        for rating_key in rating_keys:
            rating_key_tuple = tuple(rating_key.split("+"))
            if rating_key_tuple[0] == player_name_2:
                del st.session_state.ratings[rating_key]
        st.session_state.players.update_rating(player_id_2, st.session_state.ratings)
        save_ratings_to_csv("datas/ratings_data.csv")
        st.write(f"选手 {player_name_2} 的评分已重置")
    display_players()

def load_ratings_from_csv(file_path):
    """从 CSV 文件加载 Ratings 数据"""
    try:
        st.session_state.ratings.clear()  # 清空现有评分数据
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            name = row['Name']
            score = row['Score']
            view = row['View']
            st.session_state.ratings[name] = [int(score), view]
        st.session_state.players.update_all_rating(st.session_state.ratings)
    except FileNotFoundError:
        st.warning("CSV 文件未找到，使用默认设置初始化。")
    except pd.errors.EmptyDataError:
        ""
    except Exception as e:
        st.error(f"加载数据时发生错误: {e}")

def save_ratings_to_csv(file_path):
    """将 Ratings 数据保存到 CSV 文件"""
    try:
        ratings_data = []
        for rating_key in st.session_state.ratings.keys():
            name = rating_key
            score = st.session_state.ratings[rating_key][0]
            view = st.session_state.ratings[rating_key][1]
            ratings_data.append({'Name': name, 'Score': score, 'View': view})
        df = pd.DataFrame(ratings_data)
        df.to_csv(file_path, index=False)
    except Exception as e:
        st.error(f"保存数据时发生错误: {e}")



