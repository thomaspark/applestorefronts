import csv
from urllib.parse import urlencode
from flask import Flask, render_template, request
from google.appengine.api import wrap_wsgi_app

app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app)


def capitalize(word):
    word = word.replace("_", " ").lower()

    if (word.__len__() <= 3):
        return word.upper()
    else:
        return word.title()


def makeLinks(id, country, city, rnum):
    width = '1440'
    height = '806'
    
    prefix = ''
    suffix = 'hero_large.jpg'

    if country == 'UK':
        prefix = prefix + 'uk/'
    elif country == 'Australia':
        prefix = prefix + 'au/'
    elif country == 'Austria':
        prefix = prefix + 'at/'
    elif country == 'Belgium':
        prefix = prefix + 'befr/'
    elif country == 'Brazil':
        prefix = prefix + 'br/'
    elif country == 'Canada':
        prefix = prefix + 'ca/'
    elif country == 'China':
        if city == 'Hong Kong':
            prefix = prefix + 'hk/'
        elif city == 'Macao':
            prefix = prefix + 'mo/'
        else:
            prefix = prefix + 'cn/'
    elif country == 'France':
        prefix = prefix + 'fr/'
    elif country == 'Germany':
        prefix = prefix + 'de/'
    elif country == 'India':
        prefix = prefix + 'in/'
    elif country == 'Italy':
        prefix = prefix + 'it/'
    elif country == 'Japan':
        prefix = prefix + 'jp/'
    elif country == 'Korea':
        prefix = prefix + 'kr/'
    elif country == 'Malaysia':
        prefix = prefix + 'my/'
        return ['https://apple.com/' + prefix + id + '/', 'https://rtlimages.apple.com/cmc/dieter/store/16_9/R' + rnum + '.png?resize=' + width + ':' + height + '&output-format=jpg&output-quality=85&interpolation=progressive-bicubic']
    elif country == 'Mexico':
        prefix = prefix + 'mx/'
    elif country == 'Netherlands':
        prefix = prefix + 'nl/'
    elif country == 'Singapore':
        prefix = prefix + 'sg/'
    elif country == 'Spain':
        prefix = prefix + 'es/'
    elif country == 'Sweden':
        prefix = prefix + 'se/'
    elif country == 'Switzerland':
        prefix = prefix + 'chde/'
    elif country == 'Taiwan':
        prefix = prefix + 'tw/'
    elif country == 'Thailand':
        prefix = prefix + 'th/'
    elif country == 'Turkey':
        prefix = prefix + 'tr/'
    elif country == 'United Arab Emirates':
        prefix = prefix + 'ae/'

    return ['https://apple.com/' + prefix + 'retail/' + id + '/', 'https://rtlimages.apple.com/cmc/dieter/store/16_9/R' + rnum + '.png?resize=' + width + ':' + height + '&output-format=jpg&output-quality=85&interpolation=progressive-bicubic']

reader = csv.reader(open("stores.csv"))

stores_oldest = []

for idx, row in enumerate(reader):
    row.insert(0, idx+1)
    stores_oldest.append(row)

for store in stores_oldest:
    store.extend(makeLinks(store[1], store[5], store[3], store[8]))

stores_newest = stores_oldest[::-1]



@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()
    
    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, urlencode(args))


@app.route("/")
def front():
    filter = request.args.get("filter")
    size = request.args.get("size")
    sort = request.args.get("sort")

    if sort == 'old':
        stores = stores_oldest
    else:
        stores = stores_newest

    if "filter" in request.args:
        filter = request.args.get("filter")

        if (filter == 'gallery'):
            stores = [item for item in stores if item[9] == filter]
        else:
            filter = capitalize(filter)
            stores = [item for item in stores if (item[5] == filter) or (item[4].lower() == filter.lower()) or (item[7] == filter)]


    return render_template("index.html", stores=stores, size = size, sort = sort)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
