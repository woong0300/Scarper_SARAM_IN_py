import requests
from bs4 import BeautifulSoup

SEARCH_WORD = "파이썬"
PAGE_JOB_COUNT = 50
SARAM_IN_URL = f"http://www.saramin.co.kr/zf_user/search/recruit?searchType=search&&searchword={SEARCH_WORD}&panel_type=&search_optional_item=y&search_done=y&panel_count=y&recruitSort=relation"

def extract_saram_in_pages():
    html_result = requests.get(SARAM_IN_URL)
    
    # 웹페이지를 가져와서 soup로 만들어줬다.
    html_soup = BeautifulSoup(html_result.text, "html.parser")
    
    # div태그의 pagination class를 갖고 page목록을 움직일 목록을 가져왔다.
    pagination = html_soup.find("div", {"class": "pagination"})
    page_links = pagination.find_all('a')

    # div태그의 a태그를 찾고 보니 안에 내용은 숫자 밖에 없어서 바로 추출
    # TODO:마지막 페이지까지 돌고 나면 다음을 눌러서 다시 11페이지 이상을 
    # 추출할 수 있도록 해보자
    pages = []
    for page_link in page_links[:-1]:
        pages.append(int(page_link.text))

    max_page = pages[-1]        #목록에 있을 마지막 페이지

    return max_page


#각 페이지에서 구직 목록을 뽑아내는 함수
def extract_jobs(last_page):
    jobs = []
    # for page in range(last_page):
    # result = requests.get(f"{SARAM_IN_URL}&recruitPageCount={PAGE_JOB_COUNT}&recruitPage={page}")
    result = requests.get(f"{SARAM_IN_URL}&recruitPageCount={PAGE_JOB_COUNT}&recruitPage=1")
    soup = BeautifulSoup(result.text, "html.parser")
    item_recruits = soup.find_all("div", {"class": "item_recruit"})
    for item_recruit in item_recruits:
         
        if item_recruit.find("div", {"class": "area_job"}).find("a")["title"] is None:
            continue
        else:
            print(item_recruit.find("div", {"class": "area_job"}).find("a")["title"])

        
    return jobs