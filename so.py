import requests 
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://stackoverflow.com/questions/tagged/python?tab=newest&page=i"
HEADER = {"User-Agent" : "Chrome/95.0.4638.54"}


def get_last_page():
  result = requests.get(URL, HEADER)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class" : "s-pagination"}).find_all("a")
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    #print(f"let's go ! {page + 1}")
    result = requests.get(f"{URL}&pg={page+1}")
    #print(result.status_code)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"question-summary"})
    for result in results:
      print(result["question-summary"])

  
def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return []
