import pandas as pd
import time
import requests as re
import json
from urllib.request import urlopen  # 用于获取网页
from bs4 import BeautifulSoup
import multiprocessing as mp


class Match:
    match_time = ""
    my_score = -1
    my_color = ""
    my_result = ""
    opponent_name = ""
    opponent_score = -1
    opponent_sex = ""
    opponent_country = ""

    def attr2dict(self):
        return vars(self)


class Player:
    player_id = -1
    name_zh = ""
    name_en = ""
    score_new = -1
    link = ""
    sex = ""
    ranking_new = -1
    country = ""
    birthday = ""
    num_wins = -1
    num_losses = -1
    num_total = -1
    match_list = []

    def attr2dict(self):
        return vars(self)


def get_country_dict(filename: str):
    json_data = json.load(open("country.json"))
    return json_data[0], json_data[1]


def get_info(string_info: str):
    score = string_info[-4:]
    string_info = string_info[:-4]
    sex = string_info[-1]
    string_info = string_info[:-1]
    str_list = list(string_info)
    rank = ""
    name = ""
    ind = -1
    for s in range(len(str_list)):
        if str_list[s].isdigit():
            rank += str_list[s]
        else:
            ind = s
            break
    name = string_info[ind:]
    print(int(rank), name, sex, int(score))
    return int(rank), name, sex, int(score)


def get_ranking_page():
    url_ranking = "https://www.goratings.org/zh/"
    ans = re.get(url_ranking)
    bsObj = BeautifulSoup(urlopen('https://www.goratings.org/zh/'), 'html.parser')
    result_table = bsObj.find_all('table')  # 两张table，用第二张
    player_table_list = result_table[1].text.split("\n")
    player_country_list = result_table[1].find_all('img')
    temp_set = set()
    for i in player_country_list:
        temp_set.add(i.get('alt'))
    print(temp_set)
    player_dict = {}  # 记录id和姓名之间的关系
    temp_id_list = result_table[1].find_all("a")
    for temp_id in temp_id_list:
        temp_href = temp_id.get("href").split("/")[-1].split(".")[0]
        temp_name = temp_id.text
        assert temp_name not in player_dict, "警告：有重名的人！！！！！！！！"
        player_dict[temp_name] = temp_href
    if "排名棋手姓名♂♀国籍Elo等级分" in player_table_list[0]:
        player_table_list[0] = player_table_list[0].replace("排名棋手姓名♂♀国籍Elo等级分", "")
        print("多余的表头去掉了")
    if player_table_list[-1] is "":
        player_table_list.pop(-1)
        print("多余的表尾去掉了")
    print(player_table_list)
    player_list = []
    for player_info_ind in range(len(player_table_list)):
        player_info = player_table_list[player_info_ind]
        # print(player_info)
        temp_info = get_info(player_info)
        player = Player()
        player.player_id = player_dict[temp_info[1]]
        player.name_zh = temp_info[1]
        player.link = "http://www.goratings.org/zh/players/" + player_dict[temp_info[1]] + ".html"
        player.__setattr__("sex", temp_info[2])
        player.__setattr__("ranking_new", temp_info[0])
        player.__setattr__("score_new", temp_info[3])
        assert player_country_list[player_info_ind].get('alt') in COUNTRY_DICT, "错误：" + player_country_list[
            player_info_ind].get('alt') + "国家没查到！！！！"
        player.__setattr__("country", COUNTRY_DICT[player_country_list[player_info_ind].get('alt')])
        player_list.append(player.attr2dict())
    print(len(player_list))
    with open('player_ranking_list.json', 'w', encoding='utf-8') as f:
        json.dump(player_list, f, ensure_ascii=False, indent=4)


def get_player_page(name, param):
    # 直接读取id页面
    # 读取id页面url为https://www.goratings.org/zh/players/1101.html
    # 其中1101为id，棋手id从0开始编号至2272，0为空白，共2272个选手
    # 在每个id页面，通过h1标签获得姓名，在第一个表格获取当前胜负数、生日
    # 在第二个表格获取历史对局信息，等级变化，执黑/白、胜负，对手名称、当时分数、性别国籍
    url_base_zh = "http://www.goratings.org/zh/players/"
    url_base_en = "http://www.goratings.org/en/players/"
    # 个人页面无法记录自己的性别、国籍，用dict记录，用id做key
    # sex_dict = {}
    # country_dict = {}
    player_list = []
    for name in param:
        print(name)
        try:
            url_player_zh = url_base_zh + str(name) + ".html"  # url链接
            url_player_en = url_base_en + str(name) + ".html"  # url链接
            page_Obj = BeautifulSoup(urlopen(url_player_zh), 'html.parser')  # 获取网页对象
            page_Obj_en = BeautifulSoup(urlopen(url_player_en), 'html.parser')  # 获取网页对象
            # 创建对象，记录基本信息
            player = Player()
            if 'Dummy: ' + str(name) == page_Obj.find('h1').text:
                print("第" + str(name) + "个棋手没有该人！！！姓名为Dummy: " + str(name))
                with open('error.txt', 'a') as error_file:
                    error_file.write("error_index:  " + str(name) + "  No Player  \n")
                continue
            player.player_id = name  # 记录id
            player.name_zh = page_Obj.find('h1').text  # 记录中文名
            player.name_en = page_Obj_en.find('h1').text  # 记录英文名
            player.link = url_player_zh
            player_table = page_Obj.find_all('table')  # 两张table，第一张

            data_list = list(player_table[0])  # 数据汇总表格，前三行胜负总，最后一行生日
            player.num_wins = int(data_list[0].find('td').getText())  # 记录胜场
            player.num_losses = int(data_list[1].find('td').getText())  # 记录负场
            player.num_total = int(data_list[2].find('td').getText())  # 记录总场
            player.birthday = data_list[-1].find('td').getText()  # 记录生日

            game_list = list(player_table[1])  # 对局汇总表格，第一个为表头，最后一个为换行
            if "日期等级分黑白对局结果对手棋谱" in game_list[0].getText():
                game_list.pop(0)
                print("第一个表头去掉了")
            # 棋手的对局列表容易出错，单独重新设置
            player_match_list = []
            for game_ind in range(len(game_list)):
                game = game_list[game_ind]
                if game == "\n":
                    continue
                if "执" in game.getText():
                    # 对局信息：时间、己方等级分、黑白、结果、对手名、对手分、对手性别、对手国籍
                    match = Match()  # 创建对局对象
                    match_info = game.find_all('td')  # 获取对局信息
                    match.match_time = match_info[0].getText()  # 记录对局时间
                    match.my_score = int(match_info[1].getText())  # 记录己方分数
                    match.my_color = match_info[2].getText()  # 记录己方颜色
                    match.my_result = match_info[3].getText()  # 记录己方胜负
                    match.opponent_name = match_info[4].getText()  # 记录对手名
                    match.opponent_score = int(match_info[5].getText())  # 记录对手分数
                    match.opponent_sex = match_info[6].getText()  # 记录对手性别
                    assert match_info[7].find('img').get('alt') in COUNTRY_DICT, "警告：没有国家" + match_info[7].find(
                        'img').get('alt')
                    match.opponent_country = COUNTRY_DICT[match_info[7].find('img').get('alt')]  # 记录对手国籍
                    # 用对手名的超链接的id记录所有棋手的性别、国籍
                    # opp_id = int(match_info[4].find('a').get('href').split('.')[0])
                    # sex_dict[opp_id] = match_info[6].getText()
                    # country_dict[opp_id] = COUNTRY_DICT[match_info[7].find('img').get('alt')]
                    # 加到棋手的对局列表中
                    player_match_list.append(match.attr2dict())
            player.match_list = player_match_list
            # 去掉表头后第一行的分数为棋手最新分数
            if len(game_list) == 0:
                print("第" + str(name) + "个棋手没有对局！！！")
                with open('error.txt', 'a') as error_file:
                    error_file.write("error_index:  " + str(name) + "  No matches  \n")
            else:
                player.score_new = int(game_list[0].find_all('td')[1].getText())
            player_list.append(player)
        except Exception as e:
            print("捕获了一个异常，编号在" + str(name) + "。  内容为", e)
            with open('error.txt', 'a') as error_file:
                error_file.write("error_index:  " + str(name) + "  \n")
            continue
    return {name: player_list}


if __name__ == '__main__':
    time_start = time.time()
    # 获取dict
    COUNTRY_DICT = get_country_dict("country.json")[0]
    pool = mp.Pool(int(mp.cpu_count()))
    param_dict = {
        'task1': list(range(1, 121)),
        'task2': list(range(121, 261)),
        'task3': list(range(261, 481)),
        'task4': list(range(481, 721)),
        'task5': list(range(721, 1001)),
        'task6': list(range(1001, 1301)),
        'task7': list(range(1301, 1701)),
        'task8': list(range(1701, 2273))
    }
    results = [pool.apply_async(get_player_page, args=(name, param)) for name, param in param_dict.items()]
    results = [p.get() for p in results]
    print(results)
    data = []
    for j in results:
        for value in j.values():
            for ele in value:
                data.append(ele.attr2dict())
    with open('player_list.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open('error.txt', 'a') as error_file:
        error_file.write("错误收集完了，结束！！！！\n")
    time_end = time.time()
    print("totally cost", time_end - time_start)
    '''
    # 补充所有棋手的性别和国籍
    for ind in range(len(player_list)):
        player_list[ind].sex = sex_dict[player_list[ind].player_id]
        player_list[ind].country = country_dict[player_list[ind].player_id]
    data = [vars(p) for p in player_list]
    with open('player_list.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    '''
