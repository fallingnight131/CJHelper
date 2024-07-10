import random
import streamlit as st
import pandas as pd

class Script:
    def __init__(self, name, playersNum):
        self.name = name
        self.playersNum = playersNum

    def __str__(self):
        return f"{self.name}——————{self.playersNum}人剧本"


class Scripts:
    def __init__(self):
        self.scripts = []
        self.script_count = 0  # 用于跟踪已添加的剧本数量，也用作剧本ID

    def add_script(self, script):
        script.script_id = self.script_count + 1  # 在Scripts类中设置script_id
        self.scripts.append(script)
        self.script_count += 1  # 更新剧本计数器


    def remove_script(self, script_id):
        # 删除指定编号的剧本
        flag = False
        for script in self.scripts:
            if script.script_id == script_id and not flag:
                self.scripts.remove(script)
                flag = True
        if not flag:
            raise ValueError(f"找不到编号为{script_id}的剧本")
        for script in self.scripts:
            if script.script_id > script_id:
                script.script_id -= 1
        self.script_count -= 1

    def remove_all(self):
        # 删除所有剧本
        self.scripts.clear()
        self.script_count = 0

    def get_random_script(self, playerNum):
        # 过滤出玩家数小于等于给定玩家数的剧本
        compatible_scripts = [script for script in self.scripts if script.playersNum == playerNum]

        # 如果没有找到任何兼容的剧本，则抛出异常
        if not compatible_scripts:
            raise ValueError(f"没有适合{playerNum}人的剧本")

            # 如果有多个兼容的剧本，则随机选择一个
        return random.choice(compatible_scripts)

    def __str__(self):
        # 返回所有Script对象的字符串表示，每个对象占一行，并显示剧本ID
        return '\n'.join(f"{script.script_id}:{str(script)}" for script in self.scripts)

    # 示例用法

def display_scripts():
    """显示当前剧本"""
    st.header("剧本信息")
    scripts_str = str(st.session_state.scripts_container)
    st.text(scripts_str)


def add_script():
    """添加新剧本"""
    load_scripts_from_csv("datas/scripts_data.csv")
    st.header("添加剧本")
    script_name = st.text_input("输入剧本名字")
    script_player_num = st.number_input("输入剧本需要人数", min_value=1)
    if st.button("确定"):
        try:
            load_scripts_from_csv("datas/scripts_data.csv")
            script_player_num = int(script_player_num)  # 确保输入值被转换为整数
            new_script = Script(script_name, script_player_num)
            st.session_state.scripts_container.add_script(new_script)
            save_scripts_to_csv("datas/scripts_data.csv")
            st.write("剧本添加成功")
        except ValueError as e:
            st.error(f"输入无效: {e}")
    display_scripts()


def delete_script():
    """删除剧本"""
    load_scripts_from_csv("datas/scripts_data.csv")
    st.header("删除剧本")
    script_to_delete = st.number_input("输入要删除的剧本序号", min_value=0)
    if st.button("确定"):
        load_scripts_from_csv("datas/scripts_data.csv")
        st.session_state.scripts_container.remove_script(script_to_delete)
        save_scripts_to_csv("datas/scripts_data.csv")
        st.write("剧本删除成功")
    display_scripts()

def shuffle_scripts():
    """重新打乱剧本"""
    from group import (load_groups_from_csv, save_groups_to_csv, display_groups)
    load_groups_from_csv("datas/groups_data.csv")
    st.header("重新打乱所有剧本（谨慎！！！）")
    if st.button("确定", key='button1'):
        load_groups_from_csv("datas/groups_data.csv")
        load_scripts_from_csv("datas/scripts_data.csv")
        st.session_state.groups.shuffle_all(st.session_state.scripts_container)
        save_groups_to_csv("datas/groups_data.csv")
        st.write("剧本已重新打乱")

    st.header("重新打乱单个剧本")
    group_id = st.number_input("输入要重新打乱剧本的小组编号", min_value=0)
    if st.button("确定", key='button2'):
        load_groups_from_csv("datas/groups_data.csv")
        load_scripts_from_csv("datas/scripts_data.csv")
        st.session_state.groups.shuffle_group(group_id, st.session_state.scripts_container)
        save_groups_to_csv("datas/groups_data.csv")
        st.write(f"小组{group_id}的剧本已重新打乱")
    display_groups()

def load_scripts_from_csv(file_path):
    """从 CSV 文件加载 Scripts 数据"""
    try:
        st.session_state.scripts_container.remove_all()
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            script_name = row['Script_Name']
            players_num = row['Players_Num']
            script = Script(script_name, int(players_num))
            st.session_state.scripts_container.add_script(script)
    except FileNotFoundError:
        st.warning("CSV 文件未找到，使用默认设置初始化。")
    except pd.errors.EmptyDataError:
        ""
    except Exception as e:
        st.error(f"加载数据时发生错误: {e}")

def save_scripts_to_csv(file_path):
    """将 Scripts 数据保存到 CSV 文件"""
    try:
        scripts_data = []
        for script in st.session_state.scripts_container.scripts:
            script_name = script.name
            players_num = script.playersNum
            scripts_data.append({'Script_Name': script_name, 'Players_Num': players_num})
        df = pd.DataFrame(scripts_data)
        df.to_csv(file_path, index=False)
    except Exception as e:
        st.error(f"保存数据时发生错误: {e}")
