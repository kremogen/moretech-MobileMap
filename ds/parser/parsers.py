import time
from dataclasses import asdict

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from helpers import ParserHelper
from storage import Review, Info


class Parser:
    def __init__(self, driver):
        self.driver = driver

    def __scroll_to_bottom(self, elem, driver) -> None:
        """
        Скроллим список до последнего отзыва
        :param elem: Последний отзыв в списке
        :param driver: Драйвер undetected_chromedriver
        :return: None
        """
        driver.execute_script(
            "arguments[0].scrollIntoView();",
            elem
        )
        time.sleep(1)
        new_elem = driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")[-1]
        if elem == new_elem:
            return
        self.__scroll_to_bottom(new_elem, driver)

    def __get_data_item(self, elem):
        """
        Спарсить данные по отзыву
        :param elem: Отзыв из списка
        :return: Словарь
        {
            name: str
            icon_href: Union[str, None]
            date: float
            text: str
            stars: float
        }
        """
        try:
            name = elem.find_element(By.XPATH, ".//span[@itemprop='name']").text
        except NoSuchElementException:
            name = None

        try:
            icon_href = elem.find_element(By.XPATH, ".//div[@class='user-icon-view__icon']").get_attribute('style')
            icon_href = icon_href.split('"')[1]
        except NoSuchElementException:
            icon_href = None

        try:
            date = elem.find_element(By.XPATH, ".//meta[@itemprop='datePublished']").get_attribute('content')
        except NoSuchElementException:
            date = None

        try:
            text = elem.find_element(By.XPATH, ".//span[@class='business-review-view__body-text']").text
        except NoSuchElementException:
            text = None
        try:
            stars = elem.find_elements(By.XPATH, ".//div[@class='business-rating-badge-view__stars']/span")
            stars = ParserHelper.get_count_star(stars)
        except NoSuchElementException:
            stars = 0

        item = Review(
            name=name,
            icon_href=icon_href,
            date=ParserHelper.form_date(date),
            text=text,
            stars=stars
        )
        return asdict(item)

    def __get_data_campaign(self) -> dict:
        """
        Получаем данные по компании.
        :return: Словарь данных
        {
            name: str
            rating: float
            count_rating: int
            stars: float
        }
        """
        try:
            xpath_name = ".//h1[@class='orgpage-header-view__header']"
            name = self.driver.find_element(By.XPATH, xpath_name).text
        except NoSuchElementException:
            name = None
        try:
            xpath_rating_block = ".//div[@class='business-summary-rating-badge-view__rating-and-stars']"
            rating_block = self.driver.find_element(By.XPATH, xpath_rating_block)
            xpath_rating = ".//div[@class='business-summary-rating-badge-view__rating']/span[contains(@class, 'business-summary-rating-badge-view__rating-text')]"
            rating = rating_block.find_elements(By.XPATH, xpath_rating)
            rating = ParserHelper.format_rating(rating)
            xpath_count_rating = ".//div[@class='business-summary-rating-badge-view__rating-count']/span[@class='business-rating-amount-view _summary']"
            count_rating_list = rating_block.find_element(By.XPATH, xpath_count_rating).text
            count_rating = ParserHelper.list_to_num(count_rating_list)
            xpath_stars = ".//div[@class='business-rating-badge-view__stars']/span"
            stars = ParserHelper.get_count_star(rating_block.find_elements(By.XPATH, xpath_stars))
        except NoSuchElementException:
            rating = 0
            count_rating = 0
            stars = 0

        item = Info(
            name=name,
            rating=rating,
            count_rating=count_rating,
            stars=stars
        )
        return asdict(item)

    def __get_data_reviews(self) -> list:
        reviews = []
        # print(self.driver.current_url)
        elements = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")
        # print(elements)
        if len(elements) > 1:
            self.__scroll_to_bottom(elements[-1], self.driver)
            elements = self.driver.find_elements(By.CLASS_NAME, "business-reviews-card-view__review")
            for elem in elements:
                reviews.append(self.__get_data_item(elem))
        return reviews

    def __isinstance_page(self):
        return True
        try:
            xpath_name = ".//h1[@class='orgpage-header-view__header']"
            # xpath_name = "/html/body/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[5]/div/div[2]/div/div[1]/div[2]/div/div[3]/div[2]/div/div/div[3]/span[2]/div/span/span"
            # xpath_name = "/html/body/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/div[5]/div/div[2]/div/div[1]/div[2]"
            print(xpath_name)
            name = self.driver.find_element(By.XPATH, xpath_name).text
            print(name)
            return True
        except NoSuchElementException:
            return False

    def parse_all_data(self) -> dict:
        """
        Начинаем парсить данные.
        :return: Словарь данных
        {
             company_info:{
                    name: str
                    rating: float
                    count_rating: int
                    stars: float
            },
            company_reviews:[
                {
                  name: str
                  icon_href: str
                  date: timestamp
                  text: str
                  stars: float
                }
            ]
        }
        """
        if not self.__isinstance_page():
            print("heelioo")
            return {'error': 'Страница не найдена'}
        return {'company_info': self.__get_data_campaign(), 'company_reviews': self.__get_data_reviews()}

    def parse_reviews(self, company_id) -> dict:
        """
        Начинаем парсить данные только отзывы.
        :return: Массив отзывов
        {
            company_reviews:[
                {
                  name: str
                  icon_href: str
                  date: timestamp
                  text: str
                  stars: float
                }
            ]
        }

        """
        if not self.__isinstance_page():
            print('error')
            return {'error': 'Страница не найдена'}

        # dataframe[company_id] = self.__get_data_reviews()
        # return dataframe
        return self.__get_data_reviews()
        # return {company_id: self.__get_data_reviews()}

    def parse_company_info(self) -> dict:
        """
        Начинаем парсить данные только данные о компании.
        :return: Объект компании
        {
            company_info:
                {
                    name: str
                    rating: float
                    count_rating: int
                    stars: float
                }
        }
        """
        if not self.__isinstance_page():
            return {'error': 'Страница не найдена'}
        return {'company_info': self.__get_data_campaign()}
