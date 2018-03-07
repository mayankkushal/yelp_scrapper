import requests
import csv

filename = 'offers/offer-Seattle-complete-3.csv'
req = list()
api_key = 'vi8dzMbFN07N1v8IS_FN22uWPb_eu7pq0nhNYZtYIXUrvEPLjB51tkn0KKoxpQAlvpsg96PrGrZ9RULiLIFt-RozLrF0-64A8Pe3vcXjkPCWtuBvtAkNjU6LwjGYWnYx'


with open(filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            if row[1] == 'Has a Check-In Offer':
                req.append(row[0])
        except:
            pass
req = list(set(req))
new = list()
for x in req[:1]:
    print(x.replace("'",""))
    print(x)
    new.append(x)

req = ["-".join(i.lower().split())+"-seattle" for i in req]

row_list = [['name', 'image_url', 'rating', 'hours', 'latitude', 
            'longitude', 'location']]
for b_id in req:
    url = 'https://api.yelp.com/v3/businesses/{}'.format(b_id)
    headers = {
            'Authorization': 'Bearer %s' % api_key,
        }
    url_params = None
    
    r = requests.request('GET', url, headers=headers, params=url_params)
    data = r.json()
    try:
        new_row = [data['name'], data['image_url'], data['rating'], 
                   data['hours'], data['coordinates']['latitude'], 
            data['coordinates']['longitude'], data['location']]
    except Exception as e:
        print(b_id)
        print(e)
        continue
    row_list.append(new_row)

with open('seattle_detail.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in row_list:
        writer.writerow(row)

