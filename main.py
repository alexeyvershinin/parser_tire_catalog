import requests
import fake_useragent
import json

ua = fake_useragent.UserAgent()

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Is-Ajax-Request": "X-Is-Ajax-Request",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": ua.random
}


def get_data():
    url = "https://roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&arCatalogFilter_463=668736523&PAGEN_1=1"
    r = requests.get(url=url, headers=headers)

    # сохраним полученные данные в json
    with open('r.json', 'w', encoding='utf-8') as file:
        json.dump(r.json(), file, indent=4, ensure_ascii=False)

    # получим количество доступных страниц
    pages_count = r.json()["pagesCount"]

    # в цикле получим данные с каждой страницы
    for page in range(1, pages_count + 1):
        url = f"https://roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&arCatalogFilter_463=668736523&PAGEN_1={page}"

        r = requests.get(url=url, headers=headers)
        data = r.json()
        items = data["items"]

        # возможные склады, информация по ним была в разметке одной из страниц
        possible_stores = ["discountStores", "fortochkiStores", "commonStores"]

        # получаем данные из ключа items
        for item in items:
            total_amount = 0
            item_name = item["name"]
            item_price = item["price"]
            item_img = f'https://roscarservis.ru{item["imgSrc"]}'
            item_url = f'https://roscarservis.ru{item["url"]}'

            # список складов, которые достанем из ключа items
            stores = []

            for ps in possible_stores:
                if ps in item:
                    if item[ps] is None or len(item[ps]) < 1:
                        continue
                    else:
                        for store in item[ps]:
                            # название склада
                            store_name = store["STORE_NAME"]
                            # прайс
                            store_price = store["PRICE"]
                            #  количество шин на складе
                            store_amount = store["AMOUNT"]
                            # общее количество шин
                            total_amount += int(store["AMOUNT"])

                            stores.append(
                                {
                                    "store_name": store_name,
                                    "store_price": store_price,
                                    "store_amount": store_amount
                                }
                            )
            print(stores)


def main():
    get_data()


if __name__ == '__main__':
    main()
