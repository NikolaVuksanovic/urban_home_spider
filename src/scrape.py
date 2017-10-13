import requests
import json

from bs4 import BeautifulSoup

class Ad(object):
    def __init__(self):
        self.model = {
            "GetSetBuiltAt": 0,
            "additionalFeatures": {
                "characteristics": {
                    "has_wheelchair_access": False,
                    "managerie": False,
                    "new_building": False,
                    "pets": False,
                    "share": False
                },
                "energy": {
                    "eClass": "",
                    "eConsumption": ""
                },
                "equipment": {
                    "airConditioning": False,
                    "barbecue": False,
                    "cableTv": False,
                    "ceramicHob": False,
                    "dishwasher": False,
                    "isdn": False,
                    "steamOven": False,
                    "tumbleDryer": False,
                    "washingMachine": False
                },
                "exterior": {
                    "balcony": False,
                    "barbecue": False,
                    "childFriendly": False,
                    "lift": False,
                    "parkingSpace": False,
                    "playground": False,
                    "pool": False,
                    "privateGarage": False},
                "heating": {
                    "electrical": False,
                    "fuel": False,
                    "gas": False,
                    "pump": False,
                    "solar": False,
                    "wood": False
                },
                "interior": {
                    "attic": False,
                    "cellar": False,
                    "fireplace": False,
                    "hobbyRoom": False,
                    "parquet": False,
                    "pool": False,
                    "sauna": False,
                    "storageRoom": False,
                    "view": False,
                    "wineCellar": False
                }
            },
            "address": {
                "city": "",
                "street": "",
                "zipCode": 0,
            },
            "countryCode": "CH",
            "details": {
                "availableAt": 0,
                "builtAt": 0,
                "description": "",
                "keywords": "",
                "renovatedAt": ""
            },
            "distances": {
                "busStation": 0,
                "highway": 0,
                "kindergarden": 0,
                "playground": 0,
                "primarySchool": 0,
                "proximity": {
                    "lake": False,
                    "mountains": False,
                    "sea": False
                },
                "secondarySchool": 0,
                "shopping": 0,
                "trainStation": 0,
                "university": 0
            },
            "isRent": False,
            "isSale": False,
            "lat": 0,
            "lon": 0,
            "mainFeatures": {
                "baths": 0,
                "floor": 0,
                "floorSpace": 0,
                "floors": 0,
                "garages": 0,
                "livingSpace": 0,
                "lotSize": 0,
                "parkings": 0,
                "roomHeight": 0,
                "rooms": 0,
                "showers": 0,
                "toilets": 0,
                "volume": 0
            },
            "media": {
                "gallery": [],
            },
            "name": "",
            "price": {
                "currency": "CHF",
                "expenses": 0,
                "rentNetPrice": 0,
                "rentPrice": 0,
                "rentUnit": 0,
                "salePrice": 0
            },
            "timeStampAdded": "",
            "categories": [],
            "isSpider": True,
            "spiderName": "urban home",
            "origSource": "source url goe shere"
        }

class UrbanHomeSpider(object):
    def __init__(self):
        self.search_request = {
            "settings": {
                "MainTypeGroup": 1,
                "Category": 1,
                "AdvancedSearchOpen": False,
                "MailID": "",
                "PayType": 1,
                "Type": 1,
                "RoomsMin": 0,
                "RoomsMax": 0,
                "PriceMin": 0,
                "PriceMax": 0,
                "Regions": [
                    "188542"
                ],
                "SubTypes": [
                    0
                ],
                "SizeMin": 0,
                "SizeMax": 0,
                "Available": "",
                "NoAgreement": False,
                "FloorRange": 0,
                "RentalPeriod": 0,
                "equipmentgroups": [],
                "Email": "",
                "Interval": 0,
                "SubscriptionType1": True,
                "SubscriptionType2": True,
                "SubscriptionType4": True,
                "SubscriptionType8": True,
                "SubscriptionType128": True,
                "SubscriptionType512": True,
                "Sort": 0
            },
            "manual": False,
            "skip": 0,
            "reset": True,
            "position": 16,
            "iframe": 0,
            "defaultTitle": True,
            "saveSettings": True
        }
        self.objects = []

    def scrape(self):

        self.search_request['position'] = 0
        self.search_request['skip'] = 0

        while (True):

            headers = {
                'Content-type': 'application/json; charset=utf-8;',
                'X-Requested-With': 'XMLHttpRequest'
            }
            response = requests.post(
                url="http://www.urbanhome.ch/Search/DoSearch",
                data=json.dumps(self.search_request),
                headers=headers
            )
            res_dict = json.loads(response.content)

            # following block fixes problem with encoding of response
            rows = res_dict['Rows'][1:-1].replace('\\r\\n', '').replace('\\', '')
            soup = BeautifulSoup(rows, 'html.parser')
            s = soup.prettify()
            clear_soup = BeautifulSoup(s, 'html.parser')

            # list of html elements containing the data to be scraped
            items_list = clear_soup.find_all("li")
            # stop if no elements were received from request
            if len(items_list) <= 0:
                break
            # for each element from this request parse the data and append the object to "objects" field
            for item in items_list:
                item_soup = BeautifulSoup(str(item), 'html.parser')
                self.parse_data_and_append_object(item_soup)

            if self.search_request['skip'] == 0:
                self.search_request['skip'] = 25
                self.search_request['position'] = 16
            else:
                self.search_request['position'] += 16
                self.search_request['skip'] += 16

        print(len(self.objects))

        with open('data.json', 'w') as fp:
            json.dump(self.objects, fp, indent=4)

    def parse_data_and_append_object(self, item_soup):
        #create object
        record = Ad()

        # scrape data from html element
        record.model['name'] = item_soup.find_all('div')[1].find('h2').find('a').text[5:-4]
        record.model['origSource'] = item_soup.find_all('a', href=True)[0].get('href')[7:]
        record.model['price']['currency'] = item_soup.find_all('div')[1].find_all('h2')[1].find('span').text[5:-4]
        record.model['price']['rentPrice'] = item_soup.find_all('div')[1].find_all('h2')[1].find('span').next_sibling[4:-3]
        # pay_each = item_soup.find_all('div')[1].find_all('div')[0].find('p', {'class': 'fr pt15'}).text[7:-6]
        record.model['details']['availableAt'] = \
            item_soup.find_all('div')[1].find_all('div')[0].find_all('div')[0].find_all('p')[1].text[7:-6]
        floor = item_soup.find_all('div')[1].find_all('div')[0].find_all('div')[0].find_all('p')[2].text[7:-6]
        if 'EG' in floor:
            record.model['mainFeatures']['floor'] = 0
        else:
            try:
                record.model['mainFeatures']['floorSpace'] = int(
                    item_soup.find_all('div')[1].find_all('div')[0].find_all('div')[0].find_all('p')[3].text[7:-9])
                record.model['mainFeatures']['floor'] = int(floor[0])
            except:
                pass
        record.model['address']['street'] = \
            item_soup.find_all('div')[1].find_all('div')[0].find_all('div')[3].find_all('p')[0].text[6:-5]
        record.model['address']['zipCode'] = \
            item_soup.find_all('div')[1].find_all('div')[0].find_all('div')[3].find_all('p')[1].text[6:-5][0:4]
        record.model['address']['city'] = \
            item_soup.find_all('div')[1].find_all('div')[0].find_all('div')[3].find_all('p')[1].text[6:-5][5:-3]


        # scrape additional features
        features_html = item_soup.find_all('span', {'class': 'fl pr6'})
        features = []
        for feature in features_html:
            features.append(feature.find('span').next_sibling[5:-4])
        # add appropriate values in model if present
        if 'Glaskeramik' in features:
            record.model['additionalFeatures']['equipment']['ceramicHob'] = True
        if 'Garage' in features:
            record.model['additionalFeatures']['exterior']['privateGarage'] = True
        if 'Parkplatz' in features:
            record.model['additionalFeatures']['exterior']['parkingSpace'] = True
        if 'Geschirrspüler' in features:
            record.model['additionalFeatures']['equipment']['dishwasher'] = True
        if 'Haustiere ok' in features:
            record.model['additionalFeatures']['characteristics']['pets'] = True
        if 'Tiefgarage' in features:
            record.model['additionalFeatures']['exterior']['privateGarage'] = True
        if 'WG erlaubt' in features:
            record.model['additionalFeatures']['characteristics']['share'] = True
        if 'ISDN' in features:
            record.model['additionalFeatures']['equipment']['isdn'] = True
        if 'Kabel TV' in features:
            record.model['additionalFeatures']['equipment']['cableTv'] = True
        if 'Rollstuhlgängig' in features:
            record.model['additionalFeatures']['characteristics']['has_wheelchair_access'] = True
        if 'Lift' in features:
            record.model['additionalFeatures']['exterior']['lift'] = True
        if 'Balkon' in features:
            record.model['additionalFeatures']['exterior']['balcony'] = True

        gallery_list = []
        # get the gallery
        res = requests.get('http://' + record.model['origSource'])
        page_soup = BeautifulSoup( res.content ,'html.parser' )
        clear_page_soup = BeautifulSoup( page_soup.prettify(), 'html.parser' )
        l = clear_page_soup.find('div', {'id' : 'th'})
        if (l is None):
            pass
        else:
            img_list = l.find_all("li")

            if (len(img_list) <= 0):
                pass
            else:
                for itm in img_list:
                    item_soupie = BeautifulSoup(str(itm), 'html.parser')
                    link = item_soupie.find_all('a', href=True)[0].get('href')
                    gallery_list.append('http://www.urbanhome.ch' + link)

        record.model['media']['gallery'] = gallery_list

        self.objects.append(record.model)


if __name__ == '__main__':
    spider = UrbanHomeSpider()
    spider.scrape()
