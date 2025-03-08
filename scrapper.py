from requests import Session
import re
from database import DatabaseManager
from config import get_login_url, get_profile_url, get_wishlist_url
from lxml import html
from models import User, Comment, Item

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
}


class Scrapper:
    def __init__(self, database: DatabaseManager):
        self.session = Session()
        self.session.headers = headers
        self.session.get(url=get_login_url())
        self.db = database

    def parse_user(self, email: str, password: str):
        self.session.post(
            url=get_login_url(),
            data={
                "user_login": email,
                "password": password,
                "return_url": "index.php",
                "redirect_url": "index.php",
                "dispatch[auth.login]": "",
            },
        )
        response = self.session.get(url=get_profile_url())
        tree = html.fromstring(response.content)

        email = tree.xpath('//input[@name="user_data[email]"]')[0].value
        first_name = tree.xpath('//input[@name="user_data[s_firstname]"]')[0].value
        second_name = tree.xpath('//input[@name="user_data[s_lastname]"]')[0].value
        city = tree.xpath('//input[@name="user_data[s_city]"]')[0].value
        user = User(
            email=email,
            first_name=first_name,
            second_name=second_name,
            city=city,
        )
        user = self.db.create_or_update_user(user=user)
        return user

    def fill_items_list(self, user: User):
        response = self.session.get(url=get_wishlist_url())
        tree = html.fromstring(response.content)

        items = tree.xpath("//a[@class='abt-single-image']")
        urls = [item.get("href") for item in items]

        for url in urls:
            response = self.session.get(url=url)
            tree = html.fromstring(response.content)
            name = tree.xpath("//h1/bdi")[0].text
            price = tree.xpath(
                '//div[@class="ty-product-block__price-actual"]//span[@class="ty-price-num"]'
            )[0].text
            price = re.sub(r"\s+|&nbsp;", "", price)
            shops = tree.get_element_by_id("content_features")
            shops_n = len(shops.xpath('//div[@class="ty-product-feature"]')) - len(
                shops.xpath(
                    '//img[@src="images/addons/mws_feature_tab/zero_cross.png"]'
                )
            )
            rating_el = tree.xpath(
                '//div[@class="sticky-block"]//div[@class="ty-product-block__rating"]'
            )[0]
            rating = 5 - len(rating_el.xpath('//i[@class="ty-icon-star-empty"]'))
            comments_element = tree.xpath(
                "//div[@class='row-fluid ty-discussion-post ']"
            )

            comments_n = len(comments_element)

            if comments_n != 0:
                comments_element = comments_element[0]

            comments = []
            for comment_index in range(comments_n):
                body = comments_element.xpath(
                    "//div[@class='ty-discussion-post__message']"
                )[comment_index].text_content()
                author = comments_element.xpath(
                    "//span[@class='ty-discussion-post__author']"
                )[comment_index].text

                comment = Comment(
                    body=body,
                    name=author,
                )
                comments.append(comment)

            item = Item(
                name=name,
                price=price,
                shops_n=shops_n,
                rating=rating,
                comments=comments,
            )

            item = self.db.create_or_update_item(item)
            self.db.create_item_user_relation(user=user, item=item)
