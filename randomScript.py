#created by: 落夜织寒
#created on: 2024/7/7
#latest update: 2024/7/11
import streamlit as st
import pandas as pd
import io
from script import (Scripts,add_script, delete_script)
from group import (Groups,add_group, delete_group, download_groups)
from player import (Players)
from rank import (display_rank, download_rankings)
from rating import (rate_player, delete_rating)
from script import (load_scripts_from_csv, shuffle_scripts)
from group import (load_groups_from_csv)

def initialize_state():
    """初始化 Streamlit 会话状态变量"""
    if 'scripts_container' not in st.session_state:
        st.session_state.scripts_container = Scripts()
        load_scripts_from_csv("datas/scripts_data.csv")

    if 'groups' not in st.session_state and 'players' not in st.session_state:
        st.session_state.groups = Groups()
        st.session_state.players = Players()
        load_groups_from_csv("datas/groups_data.csv")  # 从 CSV 文件加载数据

    if 'ratings' not in st.session_state:
        st.session_state.ratings = {}


def main():
    """主函数运行 Streamlit 应用"""
    initialize_state()

    st.title("CJ团招新辅助工具")
    st.sidebar.title("导航")
    option = st.sidebar.selectbox("请选择一个操作",
                                  ("添加小组", "删除小组",
                                   "添加剧本", "删除剧本",
                                   "选手评分", "删除评分",
                                   "重新打乱剧本", "显示排名",
                                   "下载结果"))
    if option == "添加小组":
        add_group()
    elif option == "删除小组":
        delete_group()
    elif option == "添加剧本":
        add_script()
    elif option == "删除剧本":
        delete_script()
    elif option == "选手评分":
        rate_player()
    elif option == "删除评分":
        delete_rating()
    elif option == "重新打乱剧本":
        shuffle_scripts()
    elif option == "显示排名":
        display_rank()
    elif option == "下载结果":
        download_rankings()
        download_groups()


if __name__ == "__main__":
    main()
