from flask import Flask

app = Flask(__name__)

@app.route('/index')
def index():
    return "Добро пожаловать"

@app.route('/about')
def about():
    return "Информация о нас"

@app.errorhandler(404)
def page_not_found(e: 404):
    links = []
    html = ''
    html += f"<p>Доступные страницы:</p>"
    for rule in app.url_map.iter_rules():
        links.append((rule.endpoint))
    for link in links:
        if link != 'static':
            html += f"<a href = {link}>{link}</a> <br>"
    return html

if __name__ == '__main__':
    app.run(debug=True)