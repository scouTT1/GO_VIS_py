import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

from DataRequests import COUNTRY_DICT


def get_history_ranking():
    url_base = "https://www.goratings.org/zh/history/"
    year_list = [str(1980 + i) for i in range(42)]
    result = {}
    for year in year_list:
        url = url_base + year + "-01-01.html"
        page_obj = BeautifulSoup(urlopen(url), 'html.parser')
        player_table = page_obj.find_all('table')
        player_list = list(player_table[0])
        result[year] = []
        for i in range(1, 101):
            ans_list = player_list[i].find_all('td')
            p_rank = int(ans_list[0].getText())
            p_name = ans_list[1].getText()
            p_sex = ans_list[2].getText()
            p_cou = COUNTRY_DICT[ans_list[3].find('img').get('alt')]
            p_score = int(ans_list[4].getText())
            temp = {"rank": p_rank, "name": p_name, "sex": p_sex, "country": p_cou, "score": p_score}
            result[year].append(temp)
    with open('history_ranking.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    get_history_ranking()