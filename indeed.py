import requests #library text형태의 html
from bs4 import BeautifulSoup #텍스트형태의 데이터에서 원하는 html 태그 추출

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&amp;limit={LIMIT}&start=0" #f-string formatting


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    titles = html.find("span", title=True).string
    companys = html.find("span", {"class": "companyName"})
    company_anchor = companys.find("a")
    if companys.find("a") is not None:
        companys = str(company_anchor.string)
    else:
        companys = None
    location = html.find("div", {"class": "companyLocation"}).string
    job_id = html["data-jk"]
    return {
        'title': titles,
        'company': companys,
        'location': location,
        "link": f"https://kr.indeed.com/python%EC%A7%81-%EC%B7%A8%EC%97%85?vjk={job_id}"
    }  # 둘 사이의 차이는 없으나 관습적으로 중요한 문자열은 작은 따옴표, 의미가 없다면 큰 따옴표


def extract_page(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a", {"class": "resultWithShelf"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs


def get_jobs():
  last_page = get_last_page()
  jobs = extract_page(last_page)
  return jobs
