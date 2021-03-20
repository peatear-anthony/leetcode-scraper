import csv
import time
from selenium import webdriver

USER_NAME = 'peatear-anthony'
MAX_WAIT = 5

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

# Get all the problem urls
easy_problems_url = "https://leetcode.com/problemset/algorithms/?difficulty=Easy"
driver.get(easy_problems_url)
sort = driver.find_element_by_xpath('//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span[1]/select')
sort.click()
all = driver.find_element_by_xpath('//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span[1]/select/option[4]')
all.click()
problems = driver.find_elements_by_xpath("//a[contains(@href,'/problems/')]")

# Check the comments of each
discuss_python_tag = '/discuss/?currentPage=1&orderBy=hot&query=&tag=python'

problem_urls = [prob.get_attribute('href')
                for prob in problems]

# check out first website
url = problem_urls[1]
driver.get(url + discuss_python_tag)

# Get all page numbers
start_time = time.time()
while True:
    try:
        pagination_element = driver.find_elements_by_xpath(
        "//li[contains(@class, 'ant-pagination-item')]"
        )
        page_numbers = [int(page.text) for page in pagination_element]
        assert len(page_numbers) > 0
        break
    except AssertionError as e:
        if time.time() - start_time >= MAX_WAIT :
            raise e
        time.sleep(0.5)

for page in page_numbers[1:]:
    print('sleep')
    time.sleep(2)
    if USER_NAME in driver.page_source:
        tmp1 = driver.find_element_by_xpath(
            "//*[contains(text(),'peatear-anthony')]/../../../..//*[contains(@class,'title-link__1ay5')]"
            )
        post_link = tmp1.get_attribute('href')
        tmp2 = driver.find_element_by_xpath(
            "//*[contains(text(),'peatear-anthony')]/../../../../..//*[contains(@class, 'no__1erK')]"
            )
        num_of_likes = int(tmp2.text)
        break

    url_suffix = f'/discuss/?currentPage={str(page)}&orderBy=hot&query=&tag=python'
    tmp_url = url + url_suffix
    print('sleep')
    time.sleep(1)
    driver.get(tmp_url)
    time.sleep(1)

print(post_link)
print(num_of_likes)


'''
[{'link':, number_of_likes: },
 {'link':, number_of_likes: }
]
csv_columns = ['link', 'number_of_likes']
file_name = 'leetcode_post_data.csv'
with open(file_name, 'w+') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader
    for row in leetcode_posts:
        writer.writerow(row)
'''