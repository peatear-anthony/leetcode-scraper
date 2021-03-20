import csv
import time
from selenium import webdriver


USER_NAME = 'peatear-anthony'
MAX_WAIT = 2
PAGE_LIMIT = 3  # Check only the first PAGE_LIMIT pages

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


def get_problem_base_urls():
    easy_problems_url = "https://leetcode.com/problemset/algorithms/?difficulty=Easy"
    driver.get(easy_problems_url)
    sort = driver.find_element_by_xpath('//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span[1]/select')
    sort.click()
    select_all_button = driver.find_element_by_xpath('//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span[1]/select/option[4]')
    select_all_button.click()
    problems = driver.find_elements_by_xpath("//a[contains(@href,'/problems/')]")
     # Skip the first url as it's random.
    return [prob.get_attribute('href') for prob in problems][1:]

def get_page_numbers(url):
    discuss_python_tag = '/discuss/?currentPage=1&orderBy=hot&query=&tag=python'
    driver.get(url + discuss_python_tag)
    # Get all page numbers
    start_time = time.time()
    while True:
        try:
            pagination_element = driver.find_elements_by_xpath(
            "//li[contains(@class, 'ant-pagination-item')]"
            )
            page_numbers = []
            try:
                for page in pagination_element:
                    page_numbers.append(int(page.text))
            except:
                print(page.text)
            assert len(page_numbers) > 0
            return page_numbers
        except AssertionError as e:
            if time.time() - start_time >= MAX_WAIT :
                return 'skip'
            time.sleep(0.5)


def get_post_from_url(url):
    print(f'Current URL: {url}')
    page_numbers = get_page_numbers(url)
    if page_numbers == 'skip':
        return None
    for page in page_numbers[:PAGE_LIMIT]:
        if USER_NAME in driver.page_source:
            link_element = driver.find_element_by_xpath(
                "//*[contains(text(),'peatear-anthony')]/../../../..//*[contains(@class,'title-link__1ay5')]"
                )
            post_link = link_element.get_attribute('href')
            like_element = driver.find_element_by_xpath(
                "//*[contains(text(),'peatear-anthony')]/../../../../..//*[contains(@class, 'no__1erK')]"
                )
            num_of_likes = int(like_element.text)
            return({'link': post_link,
                'number_of_likes': num_of_likes})
        url_suffix = f'/discuss/?currentPage={str(page)}&orderBy=hot&query=&tag=python'
        tmp_url = url + url_suffix
        driver.get(tmp_url)   

def get_post_dic(problem_urls):
    leetcode_posts = []
    try:
        for index, url in enumerate(problem_urls): 
            print(f'{index + 1} / {len(problem_urls)}')
            post  = get_post_from_url(url)
            if post:
                leetcode_posts.append(post)
    except Exception as e:
        raise e
    finally:
        return leetcode_posts


if __name__ == "__main__":
    problem_urls = get_problem_base_urls()
    try:
        leetcode_posts = get_post_dic(problem_urls)
    except Exception as e:
        raise e
    finally:
        csv_columns = ['link', 'number_of_likes']
        file_name = 'leetcode_post_data.csv'
        with open(file_name, 'w+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for row in leetcode_posts:
                writer.writerow(row)