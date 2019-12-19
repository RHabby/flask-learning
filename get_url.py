import pprint

from app import create_app
from app.collection.url_extractor import url_extractor

app = create_app()
with app.app_context():
    pp = pprint.PrettyPrinter(indent=1)
    print(url_extractor.find_base_url("https://bootstrap-4.ru/docs/4.3.1/components/navbar/"))
    pp.pprint(url_extractor.extract_open_graph(
        "https://bootstrap-4.ru/docs/4.3.1/components/navbar/"))
