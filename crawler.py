import time
import json
import urllib3

"""
{
	"category": {
		"alias": "hotdogs",
		"title": "Fast Food",
		"parent_aliases": [
			"restaurants"
		],
		"country_whitelist": [],
		"country_blacklist": []
	}
}
"""
def crawl_categories():
  http = urllib3.PoolManager()
  r = http.request(
    'GET',
    'https://api.yelp.com/v3/categories',
      headers={
            "Authorization": "Bearer pHbUQBGRHB3mi8NG14AQx9jhLCpMOpw6xh8oIwpRhQCcOfjvZeMlBTpfwbb9KSNgRT1u-FAAep2mupH-w5TMxo60uDxuemrK33ngn-wxfq-ez7O2VeBNnSVwMARzYnYx"
      }
    )
  data = json.loads(r.data)
  with open('categories.json', 'w') as file:
    file.write(json.dumps(data))

def get_categories():
  with open('categories.json', 'r') as file:
    categories = json.loads(file.read())

  # print( categories['categories']) 
  output = []
  for category in categories['categories']:
    if 'restaurants' in category['parent_aliases']:
      output.append(category['alias'])
  
  with open('categories_label.csv', 'w') as file:
    for data in output:
      file.write(data + ' 0\n')
  return output

def get_categories_labeled():
  with open('categories_label.csv', 'r') as file:
    data = [line.split() for line in file.readlines()]
  return data
      
# https://api.yelp.com/v3/businesses/{id}  
def process_data():
  http = urllib3.PoolManager()
  categories = get_categories_labeled()
  for cuisine, label in categories:
    for i in range(0, 1000, 50):
      r = http.request(
        'GET',
        f'https://api.yelp.com/v3/businesses/search?location=Manhattan&categories={cuisine}&offset={i}&limit=50',
        headers={
          "Authorization": "Bearer ZthhwvCoYQiMyZWXAGcJx9jk5ASsYWhWhtIA6hUDIkc-lHsp2o--1lpihbz9BHdnJ_YFlZEw3N6JHi_YvKPQM1t-Cd4XzUbYM7zS010kp4O_54ZnhFJw79FFw5USYnYx"
        })
      
      data = []
      rid = set()
      businesses = json.loads(r.data)['businesses']
      for record in businesses:
        if record['id'] in rid:
          continue
        rid.add(record['id'])
        try:
          data.append({
          'rid': record['id'],
          'name': record['name'],
          'address': ' '.join(record['location']['display_address']),
          'review_count': record['review_count'],
          'rating': record['rating'],
          'price': record['price'],
          'zip_code': record['location']['zip_code'],
          'image_url': record['image_url'],
          'categories' : record['categories'],
          'label' : label,
        }) 
        except Exception as e: print(e)

      with open('output.jsonl', 'a') as outfile:
        for entry in data:
          json.dump(entry, outfile)
          outfile.write('\n')

process_data()