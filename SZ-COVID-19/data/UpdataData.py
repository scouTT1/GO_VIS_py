import time
import json
import operator
from urllib.request import urlopen  # 用于获取网页
from bs4 import BeautifulSoup
import multiprocessing as mp
from DataRequests import get_country_dict, Match


def sort_by_id(f_name):
    """
    本函数读取文件中的数据，并将列表按id排序
    :return: 棋手列表
    """
    with open(f_name, "r") as file:
        data = json.loads(file.read())
        for i in range(len(data)):
           if type(data[i]["player_id"]) != int:
               data[i]["player_id"] = int(data[i]["player_id"])
        json_data = sorted(data, key=operator.itemgetter('player_id'))
    return json_data


DATA = sort_by_id("./add_attr_player_list.json")


# DATA = sort_by_id("add_attr_player_list.json")


def loads_info():
    with open("info_index.json", "r") as file:
        temp = json.loads(file.read())
    return temp["zh2en"], temp["en2id"], temp["id2zh"], temp["id2sex"], temp["id2country"]


# ZH2EN, EN2ID, ID2ZH, ID2SEX, ID2COU = loads_info()


def get_matches_dict(m_list: list):
    """
    本函数用于获取从日期到比赛所属index的字典
    :param m_list: 比赛列表
    :return: 字典
    """
    m_dic = {}
    for m in range(len(m_list)):
        m_dic[m_list[m]["match_time"]] = m
    return m_dic


def get_color_info(bl: str, wh: str, res: str, name: str):
    """
    本函数针对对局情况返回胜负数据
    :param bl: 黑方姓名和段位
    :param wh: 白方姓名和段位
    :param res: 结果字符串，以+分割
    :param name: 己方棋手姓名
    :return: 返回己方姓名、段位、颜色，对方姓名、段位、颜色，己方胜负、目数
    """
    r2 = res.split("+")[-1]
    if name in bl:
        # 棋手执黑
        if "B" in res:
            # 胜
            return bl[:-3], bl[-2:], "执黑", wh[:-3], wh[-2:], "执白", "胜", r2
        else:
            # 负
            return bl[:-3], bl[-2:], "执黑", wh[:-3], wh[-2:], "执白", "负", r2
    else:
        # 棋手执白
        if "W" in res:
            # 胜
            return wh[:-3], wh[-2:], "执白", bl[:-3], bl[-2:], "执黑", "胜", r2
        else:
            # 负
            return wh[:-3], wh[-2:], "执白", bl[:-3], bl[-2:], "执黑", "负", r2


def get_page_from_go4go(name, param, error_file_name):
    """
    多线程内部函数，访问页面并且记录信息，决定更改或者新增比赛信息
    :param name: 多线程任务号
    :param param: 多线程任务对应要访问的页面编号
    :param error_file_name: 错误信息记录的文件名
    :return: 返回多线程任务的结果
    """
    pre_url = "http://www.go4go.net/go/games/byplayer/"
    id2index = {}
    for p_ind in range(len(DATA)):
        id2index[DATA[p_ind]["player_id"]] = p_ind
    player_list = []
    for name in param:
        # 对每一个选手循环
        print(name)
        if name in id2index.keys():
            player_new = DATA[id2index[name]]
        else:
            print("第" + str(name) + "个棋手没有该人，疑为AI")
            with open(error_file_name, 'a') as file:
                file.write("error_index: " + str(name) + "  maybe ai\n")
            continue
        try:
            matches_list = player_new["match_list"]
            # matches_list 为原有对局列表，现有的可能>原有，先建立原有列表中时间->index的字典
            match_dict = get_matches_dict(matches_list)
            # 页面
            url_link = pre_url + str(name)
            page_obj = BeautifulSoup(urlopen(url_link), 'html.parser')  # 获取网页对象
            # 找到对应名字的标签，获取对弈局数
            player_p = page_obj.find("p", attrs={"align": "center"})
            if player_p is None:
                print("第" + str(name) + "个棋手没有比赛")
                player_list.append(player_new)
                continue
            player_info_list = player_p.find_all("b")
            if len(player_info_list) == 5:
                print("该棋手两个名，分别为", player_info_list[0].getText(), player_info_list[1].getText())
                if player_new["name_en"] in player_info_list[0].getText():
                    player_name = player_info_list[0].getText()
                else:
                    player_name = player_info_list[1].getText()
                num_match = int(player_info_list[2].getText())
                num_win = int(player_info_list[3].getText())
            else:
                player_name = player_info_list[0].getText()
                num_match = int(player_info_list[1].getText())
                num_win = int(player_info_list[2].getText())
            num_lose = num_match - num_win
            # 通过对弈局数更改原有的局数
            player_new["num_total"] = num_match
            player_new["num_wins"] = num_win
            player_new["num_losses"] = num_lose
            if num_match % 30 == 0:
                match_page_ind = num_match // 30
            else:
                match_page_ind = num_match // 30 + 1
            print("第" + str(name) + "个棋手对局数：" + str(num_match) + "  页面数：" + str(match_page_ind))
            for page_ind in range(match_page_ind):
                next_link = url_link + "/" + str(page_ind * 30)
                print("\t第" + str(name) + "个棋手第" + str(page_ind) + "个页面", next_link)
                page_obj_match = BeautifulSoup(urlopen(next_link), 'html.parser')
                table_list = page_obj_match.find("table").find_all("tr")
                if "Game Date and Game Description" in table_list[0].getText():
                    table_list.pop(0)
                    print("\t第一个表头去掉了")
                if "Download" in table_list[0].getText():
                    table_list.pop(0)
                    print("\t第二个表头去掉了")
                print("\t该页面剩余行数：", len(table_list))
                for ind in range(0, len(table_list), 2):
                    # 第ind行代表比赛信息，第ind+1行代表对局胜负
                    match_info_list = table_list[ind].getText().split()
                    match_date = match_info_list[0].replace("[", "").replace("]", "")
                    match_info_list.pop(0)
                    match_info = " ".join(match_info_list)  # 获得比赛名称
                    match_people_list = table_list[ind + 1].find_all("td")
                    # 黑方 白方 胜负列表（胜负信息，如B+R）
                    black = match_people_list[0].getText()
                    white = match_people_list[1].getText()
                    result = match_people_list[2].getText()
                    assert player_name in black or white, "警告：棋手名字不对，序号第" + str(name) + "!!!!"
                    match_ans = get_color_info(black, white, result, player_name)
                    if match_date not in match_dict.keys():
                        # 添加原来没有的对局
                        match = Match()
                        match.match_time = match_date
                        match.match_name = match_info
                        match.my_score = -1
                        match.my_color = match_ans[2]
                        match.my_result = match_ans[6]
                        match.my_level = match_ans[1]
                        match.result_info = match_ans[7]
                        match.opponent_name = match_ans[3]
                        match.opponent_score = -1
                        match.opponent_sex = ""
                        match.opponent_country = ""
                        match.opponent_level = match_ans[4]
                        matches_list.append(match.attr2dict())
                    else:
                        # 修改原来的对局
                        # 原对局没有段位、比赛名、结果详细信息，新增
                        matches_list[match_dict[match_date]]["match_name"] = match_info
                        matches_list[match_dict[match_date]]["my_level"] = match_ans[1]
                        matches_list[match_dict[match_date]]["opponent_level"] = match_ans[4]
                        matches_list[match_dict[match_date]]["result_info"] = match_ans[7]
            player_new["match_list"] = matches_list
            player_list.append(player_new)
        except Exception as e:
            player_list.append(player_new)
            print("捕获了一个异常，编号在" + str(name) + "。  内容为", e)
            with open(error_file_name, 'a') as error:
                error.write("error_index:  " + str(name) + "  \n")
            continue
    return {name: player_list}


def complete_basic_info():
    with open("player_list1.json", "r") as file:
        data = json.loads(file.read())
    id2sex = {}
    id2country = {}
    for peo in data:
        if peo["player_id"] not in id2sex.keys():
            id2sex[peo["player_id"]] = peo["sex"]
        if peo["player_id"] not in id2country.keys():
            id2country[peo["player_id"]] = peo["country"]
    with open("sex_index.json", "w") as f:
        json.dump({"id2sex": id2sex, "id2cou": id2country}, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    '''
    #如果补充之前错误的数据就先导入错误的index
    with open("error_go4go.txt", "r") as f:
        temp = f.read()
    error_data = []
    for er in temp.split():
        if er.isdigit():
            error_data.append(int(er))
    '''

    # 多线程调用时外部代码
    time_start = time.time()
    error_file = "error_go4go1.txt"

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
    results = [pool.apply_async(get_page_from_go4go, args=(name, param, error_file)) for name, param in
               param_dict.items()]
    results = [p.get() for p in results]
    #print(results)
    data = []
    for j in results:
        for value in j.values():
            for ele in value:
                data.append(ele)
    with open('player_list2.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open(error_file, 'a') as error_file:
        error_file.write("错误收集完了，结束！！！！\n")
    time_end = time.time()
    print("totally cost", time_end - time_start)

    # 完善数据，完善对局中的性别、国籍，并将英文名替换成中文名
    # complete_basic_info()
