try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO
from lxml import etree;
from lxml.html.soupparser import fromstring;
from multiprocessing import Pool, freeze_support
import itertools;
i = 0
def u(str):
	return str.encode('utf-8').strip();

def downloadurl(url):
	try:
		response = urllib2.urlopen(url);
		tree = fromstring(response.read());
	except Exception as e:
		print(e)
		print (url)
		tree = fromstring("");
	return tree;

# Map from state names to its two letter codes
def twoletterstates():
	twolettercode = {}
	with open("states.txt") as f:
		str = f.readlines();
		for aline in str:
			twolettercode[aline.split("\t")[0].strip()] = aline.split("\t")[1].strip()
		return twolettercode

def moststates():
	cities = []
	states = []
	twolettercode = twoletterstates();
	with open("most.csv") as f:
		str = f.readlines();
		for aline in str:
			city = aline.strip().split("\t")[0].split("[")[0];
			state = aline.strip().split("\t")[1];
			if state in twolettercode:
				cities.append(city)
				states.append(twolettercode[state])
	return (cities,states)

def crawlmanualpage(query,state,city,pageno):
	url = "http://www.yelp.com/search?find_desc={0}&find_loc={1}+{2}&start={3}&attrs=ActiveDeal".format("+".join(query.split()),"+".join(city.split()),state,(pageno-1)*10);
	tree = downloadurl(url);

	pagedump = [];

	blocks = tree.xpath("//div[@class='biz-listing-large']");
	for block in blocks:
		dump = {}
		dump["brand"] = "";
		dump["offer"] = "";
		dump["url"] = ""

		for a in block.xpath("div[@class='main-attributes']"):
			for element in a.xpath("div//h3[@class='search-result-title']//a"):
				dump["brand"] = element.text_content();

			for element in a.xpath("div/div[@class='media-story']/ul[@class='search-result_tags']/li/small/text()"):
				dump["offer"] = element.strip()
			
			for element in a.xpath("div/div/div/a/img/@src"):
				dump["url"] = element

		# 	for element in a.xpath("div/div//img[@class='offscreen']/@alt"):
		# 		dump["rating"] = element;
		#	for a in block.xpath("div[@class='secondary-attributes']"):
		# 	for sa in a.xpath("address"):
		# 		dump["streetaddress"] = sa.text_content().strip();
		# 	dump["telephone"] = a.xpath("span[@class='biz-phone']")[0].text_content().strip() 
		pagedump.append(dump)
	writefile = open("./result/offers-{1}-{2}.csv".format(state,city,pageno),"wt");
	templ = "";
	for adump in pagedump:
		#temp = "{1},{2},{3},{4},{5}\n".format(str(i),(adump["brand"]),(adump["streetaddress"]),(adump["telephone"]),(adump["pricerange"]), (adump['rating']));
		temp = "{1},{2},{3}\n".format(str(i),(adump["brand"]),adump["offer"],adump['url']);
		templ = templ + temp;
	try:
		writefile.write(templ);
	except:
		pass
	writefile.close();


def cmpstar(query_state_city_pageno):
	crawlmanualpage(*query_state_city_pageno);

if __name__ == '__main__':
	freeze_support();	#http://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
	pc = 10;
	pagec = 50;
	pool = Pool(pc);

	querylist = []
	pagenolist = []
	citylist = []
	statelist = []

	(cities,states) = moststates();
	index = 0
	for city in cities:
		citylist.extend([city]*pagec)
		statelist.extend([states[index]]*pagec)
		# Add category here
		querylist.extend(["restaurants"]*pagec)
		pagenolist.extend(range(1,pagec+1))
		index = index + 1
	pool.map(cmpstar, zip(querylist,statelist,citylist,pagenolist));
