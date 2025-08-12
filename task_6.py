""" Задача 6. Список доступных страниц
Что нужно сделать
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное. Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить список всех доступных страниц на сайте с возможностью перехода на них.

Советы и рекомендации
Flask.errorhandler также принимает на вход код ошибки: @app.errorhandler(404)
При увеличении сайта будет неудобно каждый раз дополнять наш список доступных страниц. Подумайте, не стоит ли написать декоратор для endpoint.
Список всех страниц можно получить и иначе — используя переменную app.url_map. Изучите пример реализации.
Что оценивается
Отображаются только те страницы, по которым можно перейти.
Используется декорирование endpoint’ов или app.url_map, а не заранее созданный список всех страниц.
Доступные страницы отображаются только при отсутствии запрашиваемой страницы, а не при любой другой ошибке.
 """

from flask import Flask, render_template_string, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return 'Home page'


@app.route('/about')
def about():
    return 'About the site'


@app.route('/contact')
def contact():
    return 'Contacts'


@app.errorhandler(404)
def page_not_found(e):
    """Получаем все доступные маршруты"""
    links = []
    for rule in app.url_map.iter_rules():
        """Исключаем технические endpoints и параметры (их сложнее аккуратно выводить)"""
        if (
                rule.endpoint != 'static'
                and len(rule.arguments) == 0
                and rule.methods & {'GET'}
        ):
            url = url_for(rule.endpoint)
            links.append((rule.rule, url))

    if not links:
        list_html = "<p>There are no pages available on the site yet.</p>"
    else:
        list_html = '<ul>' + ''.join(
            f'<li><a href="{url}">{rule}</a></li>' for rule, url in links
        ) + '</ul>'

    return render_template_string("""
        <h1>Page not found (404)</h1>
        <p>You can go to one of the available pages:</p>
        {{ list_html|safe }}
    """, list_html=list_html), 404


if __name__ == '__main__':
    app.run(debug=True)
