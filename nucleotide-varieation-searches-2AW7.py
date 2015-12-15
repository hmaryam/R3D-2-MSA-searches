import time
import requests
from pprint import pprint
import csv

FINISHED = set(['succeeded', 'failed'])

def a(ntd_number):
	headers = {'Accept': 'application/json'}
	# Access variations for one nucleotide
	response = fetch("http://rna.bgsu.edu/r3d-2-msa",
	                 params={'units': '2AW7|1|A|A|%s'%ntd_number, 'aid':'1'}, headers=headers)
	data = response.json()
	return ntd_number, data
	

def fetch(*args, **kwargs):
    response = requests.get(*args, **kwargs)
    response.raise_for_status()
    data = response.json()
    while data['status'] not in FINISHED:
        time.sleep(3)
        response = requests.get(*args, **kwargs)
        data = response.json()
    return response

def get_data(ntd_number,data):
	dic={}
	summary=[]
	base_occurance=[]
	all_counts=[]
	for x in data['summ']:
		summary.append(x) 
	for y in range(len(summary)):
		base_occurance.append([value for value in summary[y].itervalues()])
	dic.update({'ntd_number': ntd_number})
	for x in base_occurance:
		x[0]=str(x[0])
		dic.update({x[0]:x[1]})
		all_counts.append(x[1])
	tot_count= sum(all_counts)
	dic.update({'tot_count':tot_count})
	return dic

def final_result(list_of_ntd):
	frequency_data=[]
	for ntd in list_of_ntd:
		data = a(ntd)[1]
		ntd_number= a(ntd)[0]
		frequency_data.append(get_data(ntd_number,data))
	return frequency_data


test_array = final_result(list_of_ntd)
test_file = open('test111.csv','wb')
csvwriter = csv.DictWriter(test_file, delimiter=',', 
	fieldnames=['ntd_number','A','B','C', 'U', 'W', 'G', '-', 'N','tot_count'])
csvwriter.writerow(dict((fn,fn) for fn in ['ntd_number','A','B','C', 'U', 'W', 'G', '-', 'N','tot_count']))
for row in test_array:
    csvwriter.writerow(row)
test_file.close()
