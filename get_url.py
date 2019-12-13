from app import create_app
from app.collection.url_extractor import url_extractor

app = create_app()
with app.app_context():
    print(url_extractor.find_base_url("https://habr.com/en/post/349860/"))
    print(url_extractor.extract_open_graph("https://habr.com/en/post/349860/"))
    