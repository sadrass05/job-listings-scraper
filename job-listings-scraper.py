import csv
import requests
from bs4 import BeautifulSoup

headers ={
    'referer': 'https://www.joblistings.com',
    'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
}

url = 'https://realpython.github.io/fake-jobs/'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

def safe_get_text(tag, default=""):
    return tag.get_text(strip=True) if tag else default

def safe_get_attr(tag, attr, default=""):
    return tag.get(attr, default) if tag else default

jobs = []
head = ['job_title','company_name','loaction','job_detail_page_url']
for card in soup.select('div.card'):
    job = {
        "job_title" : safe_get_text(card.select_one('h2.title.is-5')),
        "company_name" : safe_get_text(card.select_one('h3.subtitle.is-6.company')),
        "loaction" : safe_get_text(card.select_one('p.location')),
        "job_detail_page_url" : safe_get_attr(card.select_one('a[href*="/jobs/"]'),'href')
    }
    jobs.append(job)
print(f"get total jobs:{len(jobs)}")
print('-'*50)
print(jobs[0])
print('-'*50)

with open('job-listings.csv','w',newline='',encoding='utf8') as f:
    writer = csv.DictWriter(f,fieldnames=head)
    writer.writeheader()
    writer.writerows(jobs)
    print(f"job listings saved to csv")