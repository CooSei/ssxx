import requests
import json, time, re
from bs4 import BeautifulSoup
import Levenshtein
def get_log(my_name):
	try:
		q_a = json.load(open(my_name+'q_a.txt', 'r',encoding='utf-8'))
		scores = json.load(open(my_name+'score.txt', 'r'))     #记录每次提交分数
	except:
		scores = []
		q_a = {}
		f = open(my_name+'score.txt','w')
		f.close()
		f = open(my_name+'q_a.txt', 'w')
		f.close()
	return q_a, scores
def decrypt(op):
	soup = BeautifulSoup(op, 'lxml')
	soup_text = soup.text
	p = re.compile((r'display: ?none;(text-decoration:none;)?">(.*?)<'))
	for i in p.findall(op):
		if i:
			soup_text = soup_text.replace(i[1], '')
	return soup_text
def get_content(url,my_name,my_index):
	this_time = str(int(time.time()))
	headers = {
	'Host':'ssxx.univs.cn',
	'Connection': 'keep-alive',
	'Accept': 'application/json, text/plain, */*',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
	'Sec-Fetch-Site': 'same-origin',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Dest': 'empty',
	'Referer': 'https://ssxx.univs.cn/clientLogin?redirect=%2Fclient%2Fdetail%2F5f71e934bcdbf3a8c3ba5061',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Cookie': "_ga=GA1.2.406742327.1606105391; tgw_l7_route=be2f17e6fbcb3e6c5202ac57e388ad5a; _gid=GA1.2.25532619.1608623537; _gat=1",
	}
	response = requests.get(url, headers=headers)
	ll = json.loads(response.text)
	token = ll['token']
	url2 = 'https://ssxx.univs.cn/cgi-bin/race/beginning/?t='+this_time+'&activity_id=5f71e934bcdbf3a8c3ba5061&mode_id='+my_index+'&way=1'
	headers['Authorization'] = 'Bearer '+token
	response = requests.get(url2,headers=headers)
	question = json.loads(response.text)
	question_id = question['question_ids']
	race_code = question['race_code']
	headers['Referer'] = 'https://ssxx.univs.cn/client/exam/5f71e934bcdbf3a8c3ba5061/1/1/'+my_index
	every_score = 20
	for l in question_id:
		url3 = 'https://ssxx.univs.cn/cgi-bin/race/question/?t='+this_time+'&activity_id=5f71e934bcdbf3a8c3ba5061&question_id='+l+'&mode_id='+my_index+'&way=1'
		a = requests.get(url3, headers)
		all_data = json.loads(a.text)
		title = decrypt(all_data['data']['title'])
		opsWordId = {}
		opsIdWord = {}
		for i in range(len(all_data['data']['options'])):
			opsWordId[decrypt(all_data['data']['options'][i]['title'])] = all_data['data']['options'][i]['id']
			opsIdWord[all_data['data']['options'][i]['id']] = decrypt(all_data['data']['options'][i]['title'])
		url4 = 'https://ssxx.univs.cn/cgi-bin/race/answer/'
		post_answer = []
		if q_a.get(title, 0) != 0:
			opswordlist = list(opsWordId.keys())
			for sub_answer in q_a[title]:
				try:
					post_answer.append(opsWordId[sub_answer])
				except:
					ops_distance = [Levenshtein.distance(sub_answer, ole) for ole in opswordlist]
					post_answer.append(opsWordId[opswordlist[ops_distance.index(min(ops_distance))]])
		else:
			post_answer = [all_data['data']['options'][i]['id']]
		data = {"activity_id":"5f71e934bcdbf3a8c3ba5061",
				"question_id":l,
				"answer":post_answer,
				"mode_id":my_index,
				"way":"1"
				}
		post_data = requests.post(url4,headers=headers,json=data)
		answer_json = json.loads(post_data.text)
		answer = answer_json['data']['correct_ids']
		word_list = []
		for k in answer:
			word = opsIdWord[k]
			word_list.append(word)
		if title not in q_a:
			every_score -= 1
			q_a[title] = word_list

	url5 = "https://ssxx.univs.cn/cgi-bin/race/finish/"
	race = {"race_code":race_code}
	requests.post(url5,headers=headers,json=race)
	scores.append(every_score)
	print(every_score)
def write_log():
	file = open(my_name+'q_a.txt','w',encoding='utf-8')
	file.write(json.dumps(q_a,ensure_ascii=False))
	file.close()
	file = open(my_name+'score.txt','w')
	file.write(json.dumps(scores))
	file.close()


if __name__ == '__main__':
	url = ""
	# url 为电脑端登录时扫码后get网址,获取方式readme有说,类似下面这个,关键信息已隐藏
	#ex:"https://ssxx.univs.cn/cgi-bin/authorize/token/?t=1606104941788&uid=***************&avatar=https:%2F%2Fnode2d-public.hep.com.cn%2Favatar-*****************-1606104941788&activity_id=5f71e934bcdbf3a8c3ba5061"
	my_name_list = ['英雄','复兴','创新','信念']
	my_index_list = ['5f71e934bcdbf3a8c3ba51d'+str(i) for i in range(5, 9)]
	for i in range(len(my_name_list)):
		my_index = my_index_list[i]
		my_name = my_name_list[i]
		strit =  0
		max_loop = 100
		q_a, scores = get_log(my_name)
		while strit < max_loop:
			try:
				strit += 1
				print(strit)
				get_content(url,my_name,my_index)
			except:
				strit += 10
				print('something is wrong')
				time.sleep(10)
		write_log()

