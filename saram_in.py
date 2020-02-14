import requests
from bs4 import BeautifulSoup


def extract_saram_in_pages(html):
    html_result = requests.get(html)
    
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
    
    # def get_job_condition(html):
    conditions = html.find("div", {"class": "job_condition"}).find("span").find("a").parent.find_next_siblings()
    details = []
    for condition in conditions:
        details.append(condition.string)
    " ,".join(details)

    # def get_link(html):
    corp_link = html.find("strong", {"class": "corp_name"}).find("a")["href"]
    front_link = "http://www.saramin.co.kr"
    return {
        'title':job_title, 
        'corp_name': corp_name, 
        'location': adrress, 
        'condition details': details, 
        'recruit link': front_link + corp_link}


  
# def get_job_condition(html):
#     conditions = html.find("div", {"class": "job_condition"}).find("span").find("a").parent.find_next_siblings()
#     details = []
#     for condition in conditions:
#         details.append(condition.string)
#         # count = 0
#         # if count is 0:
#         #     detail += condition.string
#         # else:
#         #     count += 1
#         #     detail += '-'
#         #     detail += condition.string
#         # print(detail)
#     " ,".join(details)
#     print(details)
#     print(" ################  ")
    
    # if condition.find_next("span") is not None:
        #     tmp = condition.find_next("span")
        #     first = first + ", " + tmp
        # else:
        #     continue
        # print(first)
    

# def get_link(html):
#     corp_link = html.find("strong", {"class": "corp_name"}).find("a")["href"]
#     print(corp_link)
#각 페이지에서 구직 목록을 뽑아내는 함수

def extract_jobs(last_page, url, count_number):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{url}&recruitPageCount={count_number}&recruitPage={page}")
        print(f"Scrapping page {page}")
        soup = BeautifulSoup(result.text, "html.parser")
        recruit_lists = soup.find_all("div", {"class": "item_recruit"})
        for recruit_list in recruit_lists:
            job = get_datas(recruit_list)
            jobs.append(job)
           
        
        # if item_recruit.find("div", {"class": "area_job"}).find("a")["title"] is None:
        #     continue
        # else:
        #     print(item_recruit.find("div", {"class": "area_job"}).find("a")["title"])

        
    return jobs