import streamlit as st
import pandas as pd
from player import (Player)
from script import (Script)
from script import (load_scripts_from_csv)
from rating import (remove_ratings_by_name, load_ratings_from_csv, save_ratings_to_csv)
import io
import re


class Group:
    def __init__(self, names):
        self.players = names.split(' ')  # 明确指定空格作为分割符
        self.playersNum = len(self.players)
        self.script = Script("", 0)

    def shuffle(self, scripts):
        # 打乱剧本
        if scripts.script_count == 0:
            raise ValueError("没有剧本可供选择")
        self.script = scripts.get_random_script(self.playersNum)

    def get_script(self, script):
        # 获取剧本
        self.script = script

    def __str__(self):
        # 返回一个包含所有玩家名字的字符串，名字之间用逗号加空格分隔
        return f"选手: {', '.join(self.players)}      剧本: {self.script}"


class Groups:
    def __init__(self):
        self.groups = []  # 存储Group对象
        self.group_count = 0  # 用于跟踪已添加的组数

    def add_group(self, group):
        # 为新组分配编号，并添加到列表中
        group.group_id = self.group_count + 1  # 编号从1开始
        self.groups.append(group)
        self.group_count += 1  # 更新组计数器

    def remove_group(self, group_id):
        # 删除指定编号的组
        flag = False
        for group in self.groups:
            if group.group_id == group_id and not flag:
                self.groups.remove(group)
                flag = True
        if not flag:
            raise ValueError(f"找不到编号为{group_id}的组")
        for group in self.groups:
            if group.group_id > group_id:
                group.group_id -= 1
        self.group_count -= 1

    def remove_all(self):
        # 删除所有组
        self.groups.clear()
        self.group_count = 0

    def shuffle_all(self, scripts):
        # 打乱所有组的剧本
        for group in self.groups:
            group.shuffle(scripts)

    def shuffle_group(self, group_id, scripts):
        # 打乱指定组的剧本
        for group in self.groups:
            if group.group_id == group_id:
                group.shuffle(scripts)
                return
        raise ValueError(f"找不到编号为{group_id}的组")

    def __str__(self):
        # 返回一个包含所有组信息的字符串，每个组的信息占一行，并包含组编号
        return '\n\n'.join(f"组{group.group_id}: {group}" for group in self.groups)


def normalize_spaces(input_string):
    # 去掉首尾的空格
    trimmed_string = input_string.strip()
    # 用正则表达式将连续的空格替换成一个空格
    normalized_string = re.sub(r'\s+', ' ', trimmed_string)
    return normalized_string


def display_groups():
    """显示当前小组"""
    st.header("小组信息")
    groups_str = str(st.session_state.groups)
    st.text(groups_str)


def data_groups():
    """显示当前小组"""
    st.header("小组信息")
    groups = st.session_state.groups.groups
    groups_data = []
    group_count = 0
    for group in groups:
        group_count += 1
        groups_data.append({"序号": group_count, "选手": ', '.join(group.players), "剧本": group.script.name})
    return groups_data


def add_group():
    """添加新小组"""
    load_groups_from_csv("datas/groups_data.csv")
    st.header("添加小组")
    player_names = st.text_input("输入小组中选手名字，用空格分隔")
    if st.button("确定"):
        load_groups_from_csv("datas/groups_data.csv")
        load_scripts_from_csv("datas/scripts_data.csv")
        player_names = normalize_spaces(player_names)
        group = Group(player_names)
        group.shuffle(st.session_state.scripts_container)
        st.session_state.groups.add_group(group)
        players = player_names.split(' ')
        for player in players:
            st.session_state.players.add_player(Player(player))
        save_groups_to_csv("datas/groups_data.csv")
        st.write("小组添加成功")
    display_groups()


def delete_group():
    """删除小组"""
    load_groups_from_csv("datas/groups_data.csv")
    st.header("删除小组")
    group_to_delete = st.number_input("输入要删除小组的序号", min_value=0)
    if st.button("确定"):
        load_groups_from_csv("datas/groups_data.csv")
        load_ratings_from_csv("datas/ratings_data.csv")
        names = st.session_state.groups.groups[group_to_delete - 1].players
        for name in names:
            st.session_state.players.remove_by_name(name)
            remove_ratings_by_name(name)
        st.session_state.groups.remove_group(group_to_delete)
        save_groups_to_csv("datas/groups_data.csv")
        save_ratings_to_csv("datas/ratings_data.csv")
        st.write("小组删除成功")
    display_groups()


def load_groups_from_csv(file_path):
    """从 CSV 文件加载 Groups 数据"""
    try:
        st.session_state.players.remove_all()
        st.session_state.groups.remove_all()
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            players_str = row['Players']
            players = players_str.split(' ')
            script_name = row['Script']
            for player in players:
                st.session_state.players.add_player(Player(player))
            group = Group(players_str)
            group.get_script(Script(script_name, len(players)))
            st.session_state.groups.add_group(group)
    except FileNotFoundError:
        st.warning("CSV 文件未找到，使用默认设置初始化。")
    except pd.errors.EmptyDataError:
        ""
    except Exception as e:
        st.error(f"加载数据时发生错误: {e}")


def save_groups_to_csv(file_path):
    """将 Groups 数据保存到 CSV 文件"""
    try:
        groups_data = []
        for group in st.session_state.groups.groups:
            players = ' '.join(group.players)
            script = group.script.name if group.script else ''
            groups_data.append({'Players': players, 'Script': script})

        df = pd.DataFrame(groups_data)
        df.to_csv(file_path, index=False)
    except Exception as e:
        st.error(f"保存数据时发生错误: {e}")


def download_groups():
    """下载 Groups 数据为 CSV 文件"""
    groups_data = data_groups()
    df = pd.DataFrame(groups_data)

    # Convert DataFrame to CSV format
    csv = df.to_csv(index=False)

    # Create a BytesIO object
    buffer = io.BytesIO()
    buffer.write(csv.encode())
    buffer.seek(0)

    st.download_button(
        label="下载小组信息为 CSV 文件",
        data=buffer,
        file_name='groups.csv',
        mime='text/csv'
    )
