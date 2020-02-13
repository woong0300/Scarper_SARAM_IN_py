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

#구직 목록에서 정보를 뽑아내는 함수
def get_datas(html):
    job_title = html.find("div", {"class": "area_job"}).find("a")["title"]
    corp_name = html.find("strong", {"class": "corp_name"}).find("a")["title"] 
    
    # def get_job_location(html):
    big_location = html.find("div", {"class": "job_condition"}).find("a").string
    small_location =html.find("div", {"class": "job_condition"}).find("a").find_next("a").string
    adrress = big_location + " " + small_location;
    
    return {'title':job_title, 'corp_name': corp_name, 'location': adrress}


  
def get_job_condition(html):
    conditions = html.find("div", {"class": "job_condition"}).find("span").find("a").parent.find_next_siblings()
    
    for condition in conditions[0:2]:  
        print(condition)
        # if condition.find_next("span") is not None:
        #     tmp = condition.find_next("span")
        #     first = first + ", " + tmp
        # else:
        #     continue
        # print(first)
    
    

#각 페이지에서 구직 목록을 뽑아내는 함수
def extract_jobs(last_page):
    jobs = []
    # for page in range(last_page):
    # result = requests.get(f"{SARAM_IN_URL}&recruitPageCount={PAGE_JOB_COUNT}&recruitPage={page}")
    result = requests.get(f"{SARAM_IN_URL}&recruitPageCount={PAGE_JOB_COUNT}&recruitPage=1")
    soup = BeautifulSoup(result.text, "html.parser")
    recruit_lists = soup.find_all("div", {"class": "item_recruit"})
    for recruit_list in recruit_lists:
        # job = get_job_condition(recruit_list)
        
        # 잠시 테스트를 위해서 주석
        job = get_datas(recruit_list)
        jobs.append(job)
        
        
        # if item_recruit.find("div", {"class": "area_job"}).find("a")["title"] is None:
        #     continue
        # else:
        #     print(item_recruit.find("div", {"class": "area_job"}).find("a")["title"])

        
    return jobs