import time

import undetected_chromedriver
from parsers import Parser


class YandexParser:
    def __init__(self, id_yandex: int):
        """
        @param id_yandex: ID Яндекс компании
        """
        self.id_yandex = id_yandex

    def __open_page(self):
        # print(123)
        url: str = 'https://yandex.ru/maps/org/{}/reviews/'.format(str(self.id_yandex))
        opts = undetected_chromedriver.ChromeOptions()
        opts.add_argument('headless')
        opts.add_argument('--disable-gpu')
        driver = undetected_chromedriver.Chrome(options=opts)
        parser = Parser(driver)
        driver.get(url)
        print(driver.current_url)
        return parser

    def parse(self, company_id, type_parse: str = 'reviews') -> dict:
        """
        Функция получения данных в виде
        @param type_parse: Тип данных, принимает значения:
            default - получает все данные по аккаунту
            company - получает данные по компании
            reviews - получает данные по отчетам
        @return: Данные по запрошенному типу
        """
        result:dict = {}
        # page = self.__open_page()
        # time.sleep(1)
        try:
            page = self.__open_page()
            time.sleep(1)
            if type_parse == 'default':
                result = page.parse_all_data()
            if type_parse == 'company':
                result = page.parse_company_info()
            if type_parse == 'reviews':
                result = page.parse_reviews(company_id)
        except Exception as e:
            print(e)
            return result
        finally:
            page.driver.close()
            page.driver.quit()
            return result
