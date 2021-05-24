from app.models.opinion import Opinion
import requests
import json
from bs4 import BeautifulSoup

class Product:
    def __init__(self, product_id, product_name = None, opinions = []):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions
    
    def extract_product(self):
        next_page = "https://www.ceneo.pl/{}#tab=reviews".format(self.product_id)
        while next_page:
            respons = requests.get(next_page)
            page_dom = BeautifulSoup(respons.text, "html.parser")
            opinions = page_dom.select("div.js_product-review")
            for opinion in opinions:
                self.opinions.append(Opinion().extract_opinion(opinion).transform_opinion())
            try:
                next_page = "https://www.ceneo.pl" + \
                    page_dom.select("a.pagination__next").pop()["href"]
            except IndexError:
                next_page = None
            print(next_page)

    def __str__(self):
        return f"product_id: {self.product_id}<br>product_name: {self.product_name}<br>opinions:<br>" + "<br><br>".join(str(opinion) for opinion in self.opinions)

    def __repr__(self):
        return f"Product(product_id={self.product_id}, product_name={self.product_name}, opinions=[" + ", ".join(opinion.__repr__() for opinion in self.opinions) + "])"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions": [opinion.to_dict() for opinion in self.opinions]
        }

    def save_to_json(self):
        with open(f"app/products/{self.product_id}.json", "w", encoding="UTF-8") as fp:
            json.dump(self.to_dict(), fp, indent=4, ensure_ascii=False)
