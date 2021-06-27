from app.models.opinion import Opinion
import requests
import json
from bs4 import BeautifulSoup

class Product:
    def __init__(self, product_id, product_name = None, opinions = []):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions.copy()

    def extract_product(self):
        next_page = "https://www.ceneo.pl/{}#tab=reviews".format(self.product_id)
        while next_page:
            respons = requests.get(next_page)
            page_dom = BeautifulSoup(respons.text, "html.parser")
            if self.product_name == None:
                try:
                    self.product_name = page_dom.find("h1", class_="product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").text[1:]
                except AttributeError:
                    self.product_name = "empty_product_name"
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
        fp.close()

    def read_from_json(self):
        print(self.product_id)
        with open(f"app/products/{self.product_id}.json", "r", encoding="UTF-8") as fp:
            prod = json.load(fp)
        fp.close()
        self.product_name = prod['product_name']
        opinions = prod['opinions']
        for opinion in opinions:
            self.opinions.append(Opinion(**opinion))

    def save_stats_file(self):

        json_data = {}
        stats = {"name": "NaN", "opinions": 0, "cons": 0, "pros": 0, "average score": "NaN"}
        accumulated_score = 0.0

        with open(f"app/products/{self.product_id}.json", "r", encoding="UTF-8") as file:
            data = file.read()
            json_data = json.loads(data)

        stats["name"] = json_data["product_name"]
        for opinion in json_data["opinions"]:
            stats["opinions"] += 1
            stats["cons"] += len(opinion["cons"])
            stats["pros"] += len(opinion["pros"])
            accumulated_score += opinion["stars"]
            if stats["opinions"] > 0:
                stats["average score"] = round((accumulated_score / stats["opinions"]), 2)

        with open(f"app/products_stats/{self.product_id}_stats.json", "w", encoding="UTF-8") as file:
            json.dump(stats, file)