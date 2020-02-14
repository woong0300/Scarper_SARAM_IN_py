from saram_in import extract_saram_in_pages, extract_jobs
from save import save_to_file

SEARCH_WORD = input("검색어를 입력하세요:")
PAGE_JOB_COUNT = 50
SARAM_IN_URL = f"http://www.saramin.co.kr/zf_user/search/recruit?searchType=search&&searchword={SEARCH_WORD}&panel_type=&search_optional_item=y&search_done=y&panel_count=y&recruitSort=relation"

max_num = extract_saram_in_pages(SARAM_IN_URL)

jobs = extract_jobs(max_num, SARAM_IN_URL, PAGE_JOB_COUNT)

save_to_file(jobs)