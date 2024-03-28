from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import re
import time
from selenium.webdriver.chrome.options import Options
import argparse


def download_data(
    id: str,
    pw: str,
    start_year_int: int = 2000,
    start_month: str = "01",
    end_year_int: int = 2001,
    end_month: str = "12",
    location_keyword: str = "모슬포",
    final_year: int = 2023,
) -> None:
    """
    This function is to batch download data from the website of Ministry of Oceans and Fisheries (MOF) of Korea automatically made by selenium.

    Args:
        id: str, your id to login the website
        pw: str, your password to login the website
        start_year_int: int, the start year of the data you wanna download
        start_month: str, the start month of the data you wanna download (note, it should be '01' instead of '1')
        end_year_int: int, the end year of the data you wanna download in one batch. Because the website limits users to download data within 2 years. so the end data - start data should be less than 2 years
        end_month: str, the end month of the data you wanna download in one batch. Ditto.
        location_keyword: str, the location keyword of the data you wanna download (in our current task, it is "모슬포", a port in Jeju island)
        final_year: int, the final year of the data you wanna download
    """

    # Set Chrome options to keep the browser window open
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(
        "http://www.khoa.go.kr/oceangrid/gis/category/reference/distribution.do#none"
    )

    # click 로그인
    login_button = browser.find_element(By.XPATH, "//a[text()='로그인']")
    login_button.click()
 
    id_box = browser.find_element(By.ID, "user_id")
    pw_box = browser.find_element(By.ID, "user_passwd")
    # input the id into the id cell
    id_box.send_keys(id)
    time.sleep(2)
    pw_box.send_keys(pw)
    time.sleep(2)
    login_button_at_login_page = browser.find_element(By.ID, "btn_login")
    login_button_at_login_page.click()
    time.sleep(2)

    # input the location keyword. In our current task, it is "모슬포"
    keyword_box = browser.find_element(By.ID, "searchKey")
    keyword_box.send_keys(location_keyword)

    # click to select the item you wanna download, in our current task, it is the "수온" item
    item_button = browser.find_element(By.ID, "chkCodeTemp")
    item_button.click()
    # select the time interval

    while start_year_int < final_year + 1:
        start_year_button = browser.find_element(By.ID, "searchPreYear1")
        start_month_button = browser.find_element(By.ID, "searchPreMonth1")
        end_year_button = browser.find_element(By.ID, "searchPreYear2")
        end_month_button = browser.find_element(By.ID, "searchPreMonth2")
        # the timeframe gap between start and end should be less than 2 years
        start_year = str(start_year_int)
        end_year = str(end_year_int)
        Select(start_year_button).select_by_value(start_year)
        Select(start_month_button).select_by_value(start_month)
        Select(end_year_button).select_by_value(end_year)
        Select(end_month_button).select_by_value(end_month)

        # click the 검색 button to show the result
        search_button = browser.find_element(
            By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/p/a/img'
        )
        search_button.click()

        start_year_int, end_year_int = start_year_int + 2, end_year_int + 2

        time.sleep(2)
        try:
            popup_button = browser.find_element(By.CLASS_NAME, "ui-dialog-buttonset")
            popup_button.click()
        except:
            pass

        # get the page's html
        html = browser.page_source
        pattern = r'a href="javascript:goPage(.*?);">.*?</a>'
        matches = re.findall(pattern, html)

        # len(matches) - 3 = amount of pages in current search result
        # len(matches) - 4 = how many times we should click the next page button
        next_page_button_click_times = len(matches) - 4

        # click the 번호 button to select all items in the current page
        beonho_button = browser.find_element(By.ID, "checkboxAll")
        beonho_button.click()

        # click the 다운로드 button to download the data
        download_button = browser.find_element(By.NAME, "zipdown")
        download_button.click()
        time.sleep(2)

        for i in range(next_page_button_click_times):
            # click the next page button
            next_page_button = browser.find_element(
                By.CSS_SELECTOR, 'img[alt="다음페이지"]'
            )
            next_page_button.click()
            time.sleep(5)

            beonho_button = browser.find_element(By.ID, "checkboxAll")
            beonho_button.click()

            # click the 다운로드 button to download the data
            download_button = browser.find_element(By.NAME, "zipdown")
            download_button.click()
            time.sleep(2)
            try:
                popup_button = browser.find_element(
                    By.CLASS_NAME, "ui-dialog-buttonset"
                )
                popup_button.click()
            except:
                pass
        time.sleep(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument("--id", type=str, default="your_id")
    parser.add_argument("--pw", type=str, default="your_pw")
    parser.add_argument("--start_year_int", type=int, default=2000)
    parser.add_argument("--start_month", type=str, default="01")
    parser.add_argument("--end_year_int", type=int, default=2001)
    parser.add_argument("--end_month", type=str, default="12")
    parser.add_argument("--location_keyword", type=str, default="모슬포")
    parser.add_argument("--final_year", type=int, default=2024)
    args = parser.parse_args()

    download_data(
        start_year_int=args.start_year_int,
        start_month=args.start_month,
        end_year_int=args.end_year_int,
        end_month=args.end_month,
        location_keyword=args.location_keyword,
        final_year=args.final_year,
    )