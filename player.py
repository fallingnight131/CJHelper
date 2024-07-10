import streamlit as st
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.view = ""

    def update_rating(self, ratings):
        self.score = 0
        self.view = ""
        rater_num = 0
        for rating_key in ratings.keys():
            rating_key_tuple = tuple(rating_key.split("+"))
            if rating_key_tuple[0] == self.name:
                rater_num += 1
                self.score += ratings[rating_key][0]
                if ratings[rating_key][1] != "":
                    if self.view == "":
                        self.view = self.view + str(ratings[rating_key][1]) + "(by " + str(rating_key_tuple[1]) + ") "
                    else:
                        self.view = self.view + "/ " + str(ratings[rating_key][1]) + "(by " + str(rating_key_tuple[1]) + ") "
        if rater_num != 0:
            self.score = self.score / rater_num
            self.score = round(self.score, 3)

    def __str__(self):
        # 返回一个包含所有玩家名字的字符串，名字之间用逗号加空格分隔
        if self.view == "":
            return f"{self.name}      评分:{self.score}      备注: 无"
        else:
            return f"{self.name}      得分:{self.score}      备注:{self.view}"


class Players:
    def __init__(self):
        self.players = []  # 存储player对象
        self.player_count = 0  # 用于跟踪已添加的组数

    def add_player(self, player):
        # 为新选手分配编号，并添加到列表中
        player.player_id = self.player_count + 1  # 编号从1开始
        self.players.append(player)
        self.player_count += 1  # 更新组计数器

    def remove_player(self, player_id):
        # 删除指定编号的组
        flag = False
        for player in self.players:
            if player.player_id == player_id and not flag:
                self.players.remove(player)
                flag = True
        if not flag:
            raise ValueError(f"找不到编号为{player_id}的选手")
        for player in self.players:
            if player.player_id > player_id:
                player.player_id -= 1
        self.player_count -= 1

    def remove_all(self):
        # 删除所有组
        self.players.clear()
        self.player_count = 0

    def remove_by_name(self, name):
        # 删除指定名字的选手
        flag = False
        for player in self.players:
            if player.name == name and not flag:
                self.players.remove(player)
                flag = True
        if not flag:
            raise ValueError(f"找不到名字为{name}的选手")
        for player in self.players:
            if player.player_id > player.player_id:
                player.player_id -= 1
        self.player_count -= 1

    def get_name(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                return player.name

    def update_rating(self, player_id, ratings):
        for player in self.players:
            if player.player_id == player_id:
                player.update_rating(ratings)
                return

    def update_all_rating(self, ratings):
        for player in self.players:
            player.update_rating(ratings)

    def __str__(self):
        # 返回一个包含所有组信息的字符串，每个组的信息占一行，并包含组编号
        return '\n\n'.join(f"{player.player_id}: {player}" for player in self.players)


def display_players():
    """显示当前选手"""
    st.header("选手信息")
    players_str = str(st.session_state.players)
    st.text(players_str)
