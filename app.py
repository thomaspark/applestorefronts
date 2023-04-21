from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
import csv


def capitalize(word):
    word = word.replace("_", " ").lower()

    if (word.__len__() <= 3):
        return word.upper()
    else:
        return word.title()


class MainPage(webapp.RequestHandler):

    def get(self, filter=None, sort=None, size=None):

        stores = stores_newest

        if (size == None):
            size = ''

        if (sort == None):
            sort = ''

        if (filter == None) or (filter.lower() == 'all'):
            filter = 'All'
            if sort == 'old':
                stores = stores_oldest
        elif (filter == 'gallery') and (sort == 'old'):
            stores = [item for item in stores_oldest if item[9] == filter]
            filter = capitalize(filter)
        elif (filter == 'gallery'):
            stores = [item for item in stores_newest if item[9] == filter]
            filter = capitalize(filter)
        elif sort == 'old':
            filter = capitalize(filter)
            stores = [item for item in stores_oldest if (item[5] == filter) or (item[4].lower() == filter.lower()) or (item[7] == filter)]
        else:
            filter = capitalize(filter)
            stores = [item for item in stores_newest if (item[5] == filter) or (item[4].lower() == filter.lower()) or (item[7] == filter)]

        template_values = {
            'stores': stores,
            'filter': filter,
            'sort': sort,
            'size': size
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/([^/]+)?/([^/]+)?/([^/]+)?/?', MainPage),
                                     ('/([^/]+)?/([^/]+)?/?', MainPage),
                                     ('/([^/]+)?/?', MainPage),
                                     ('/', MainPage)],
                                     debug=True)


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

    if rnum == '469':
        return ['https://www.apple.com/' + prefix + 'retail/' + id + '/', 'https://rtlimages.apple.com/cmc/dieter/store/16_9/R' + rnum + '.png?output-format=jpg&output-quality=85&interpolation=progressive-bicubic']
    else:
        return ['https://www.apple.com/' + prefix + 'retail/' + id + '/', 'https://rtlimages.apple.com/cmc/dieter/store/16_9/R' + rnum + '.png?resize=' + width + ':' + height + '&output-format=jpg&output-quality=85&interpolation=progressive-bicubic']

reader = csv.reader(open("stores.csv", "U"))

stores_oldest = []

for idx, row in enumerate(reader):
    row.insert(0, idx+1)
    stores_oldest.append(row)

for store in stores_oldest:
    store.extend(makeLinks(store[1], store[5], store[3], store[8]))

stores_newest = stores_oldest[::-1]


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
