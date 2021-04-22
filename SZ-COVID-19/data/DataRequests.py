import json
from urllib.request import urlopen  # 用于获取网页
from bs4 import BeautifulSoup
import multiprocessing as mp


class Match:
    match_time = ""
    match_name = ""
    my_score = -1
    my_color = ""
    my_result = ""
    my_level = ""
    result_info = ""
    opponent_name = ""
    opponent_score = -1
    opponent_sex = ""
    opponent_country = ""
    opponent_level = ""

    def attr2dict(self):
        return vars(self)


class Player:
    player_id = -1
    name_zh = ""
    name_en = ""
    level = ""
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
    json_data = json.load(open(filename))
    return json_data[0], json_data[1]


COUNTRY_DICT = get_country_dict("country.json")[0]


def get_player_page(name, param, error_file_name):
    """
    该函数对棋手个人页面进行读取，多线程进行
    :param name: 多线程任务编号
    :param param: 多线程任务列表
    :param error_file_name: 错误文件名
    :return: 返回多线程结果列表
    """
    # 直接读取id页面
    # 读取id页面url为https://www.goratings.org/zh/players/1101.html
    # 其中1101为id，棋手id从0开始编号至2272，0为空白，共2272个选手
    # 在每个id页面，通过h1标签获得姓名，在第一个表格获取当前胜负数、生日
    # 在第二个表格获取历史对局信息，等级变化，执黑/白、胜负，对手名称、当时分数、性别国籍
    url_base_zh = "http://www.goratings.org/zh/players/"
    url_base_en = "http://www.goratings.org/en/players/"
    player_list = []
    for name in param:
        print(name)
        try:
            url_player_zh = url_base_zh + str(name) + ".html"  # url链接
            url_player_en = url_base_en + str(name) + ".html"  # url链接
            page_obj = BeautifulSoup(urlopen(url_player_zh), 'html.parser')  # 获取网页对象
            page_obj_en = BeautifulSoup(urlopen(url_player_en), 'html.parser')  # 获取网页对象
            # 创建对象，记录基本信息
            player = Player()
            if 'Dummy: ' + str(name) == page_obj.find('h1').text:
                print("第" + str(name) + "个棋手没有该人！！！姓名为Dummy: " + str(name))
                with open(error_file_name, 'a') as error_file:
                    error_file.write("error_index:  " + str(name) + "  No Player  \n")
                continue
            player.player_id = name  # 记录id
            player.name_zh = page_obj.find('h1').text  # 记录中文名
            player.name_en = page_obj_en.find('h1').text  # 记录英文名
            player.link = url_player_zh
            player_table = page_obj.find_all('table')  # 两张table，第一张

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
                with open(error_file_name, 'a') as error_file:
                    error_file.write("error_index:  " + str(name) + "  No matches  \n")
            else:
                player.score_new = int(game_list[0].find_all('td')[1].getText())
            player_list.append(player)
        except Exception as e:
            print("捕获了一个异常，编号在" + str(name) + "。  内容为", e)
            with open(error_file_name, 'a') as error_file:
                error_file.write("error_index:  " + str(name) + "  \n")
            continue
    return {name: player_list}


def add_other_data(file_name, json_name, error_file_name):
    """
    该函数为从错误列表中读取错误失败的页面编号并重新读取
    :param file_name: 错误信息的文件
    :param json_name: 重新读取数据后保存的文件
    :param error_file_name: 新的错误文件
    """
    # 读取文件中的剩下不成功的例子并添加数据
    other_data = []
    for line in open(file_name, "r"):  # 设置文件对象并读取每一行文件
        # other_data.append(line)
        ans = line.split()
        if len(ans) <= 1:
            continue
        elif len(ans) == 2:
            # 网络错误
            print(ans[1])
            other_data.append(ans[1])
        else:
            # 其他错误
            print("其他错误")
    print(len(other_data))
    num_other = len(other_data)
    other_i = num_other // 8

    # 获取dict
    # COUNTRY_DICT = get_country_dict("country.json")[0]
    pool = mp.Pool(int(mp.cpu_count()))
    param_dict = {
        'task1': list(other_data[:other_i]),
        'task2': list(other_data[other_i:other_i * 2]),
        'task3': list(other_data[other_i * 2:other_i * 3]),
        'task4': list(other_data[other_i * 3:other_i * 4]),
        'task5': list(other_data[other_i * 4:other_i * 5]),
        'task6': list(other_data[other_i * 5:other_i * 6]),
        'task7': list(other_data[other_i * 6:other_i * 7]),
        'task8': list(other_data[other_i * 7:])
    }
    results = [pool.apply_async(get_player_page, args=(name, param, error_file_name)) for name, param in
               param_dict.items()]
    results = [p.get() for p in results]
    print(results)
    data = []
    for j in results:
        for value in j.values():
            for ele in value:
                data.append(ele.attr2dict())
    with open(json_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open(error_file_name, 'a') as error_file:
        error_file.write("错误收集完了，结束！！！！\n")


def complete_sex_country(filename):
    """
    该函数为已有的json数据中的选手完善性别和国籍信息
    性别和国籍信息来源于对局信息中
    :param filename: 文件名
    """
    with open(filename, "r") as file:
        data = json.loads(file.read())
    print("棋手总共个数：", len(data))
    dic_sex = {}
    dic_country = {}
    for i in range(len(data)):
        matches = data[i]["match_list"]
        print("第" + str(i + 1) + "个棋手对局数：" + str(len(matches)))
        for j in range(len(matches)):
            people = matches[j]["opponent_name"]
            if people not in dic_country:
                dic_country[people] = matches[j]["opponent_country"]
            if people not in dic_sex:
                dic_sex[people] = matches[j]["opponent_sex"]
    # 读取完了
    print("字典中选手个数" + str(len(dic_sex)) + "  " + str(len(dic_country)))
    for i in range(len(data)):
        if data[i]["name_zh"] not in dic_sex or data[i]["name_zh"] not in dic_country:
            print("该选手" + data[i]["name_zh"] + "可能没有对局  " + str(len(data[i]["match_list"])))
            continue
        data[i]["sex"] = dic_sex[data[i]["name_zh"]]
        data[i]["country"] = dic_country[data[i]["name_zh"]]
    with open("add_attr_" + filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def generate_name_dict():
    """
    本函数用于生成中英文名的映射
    文件为add_attr_player_list.json，其中的棋手部分含有sex和country
    """
    '''
    with open("中间过程数据/add_attr_player_list.json", "r") as f:
        data = json.loads(f.read())
    zh2en = {}
    en2id = {}
    id2zh = {}
    id2sex = {}
    id2cou = {}
    for pl in data:
        zh2en[pl["name_zh"]] = pl["name_en"]
        en2id[pl["name_en"]] = pl["player_id"]
        id2zh[pl["player_id"]] = pl["name_zh"]
        if "sex" in pl.keys():
            id2sex[pl["player_id"]] = pl["sex"]
        if "country" in pl.keys():
            id2cou[pl["player_id"]] = pl["country"]
    with open("info_index.json", "w", encoding='utf-8') as f:
        json.dump({"zh2en": zh2en, "en2id": en2id, "id2zh": id2zh, "id2sex": id2sex, "id2cou": id2cou}, f,
                  ensure_ascii=False, indent=4)
    '''
    # 生成新旧名字的字典，旧名->新名
    old2new = {}
    with open("重复人名对照表.txt", "r") as f:
        temp = f.readlines()
    print(len(temp))
    for i in range(len(temp)):
        n_list = temp[i].split("--")
        name1 = n_list[0]
        name2 = n_list[2].replace("\t", "")
        if n_list[1].isdigit() and n_list[3].isdigit():
            if int(n_list[1]) > int(n_list[3]):
                old2new[name2] = name1
            elif int(n_list[1]) < int(n_list[3]):
                old2new[name1] = name2
            else:
                print("错误！两个人编号一样了！！！！！")
    print(old2new)
    print(len(old2new))
    with open("old2new.json", "w", encoding='utf-8') as f:
        json.dump({"old2new": old2new}, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    '''
    # 多线程调用时外部代码
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

    # add_other_data("error_other.txt", "player_other_list1.json", "error_other1.txt")
    # complete_sex_country("player_list.json")
    generate_name_dict()
