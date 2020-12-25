import time, requests, json, re
from bs4 import BeautifulSoup



def decrypt(op):
	soup = BeautifulSoup(op, 'lxml')
	soup_text = soup.text
	# p = re.compile(r'display: ?none;">(.*?)<')
	p = re.compile(r'display: ?none;(text-decoration:none;)?">(.*?)<')
	for i in p.findall(op):
		if i:
			soup_text = soup_text.replace(i[1], '')
	return soup_text

if __name__ == '__main__':
	url = ''
	this_time = str(int(time.time()))
	my_name = '英雄'
	my_index = '5f71e934bcdbf3a8c3ba51d5'
	q_a = {}
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
	with open(my_name+'.txt','a') as f:
		for l in question_id:
			url3 = 'https://ssxx.univs.cn/cgi-bin/race/question/?t='+this_time+'&activity_id=5f71e934bcdbf3a8c3ba5061&question_id='+l+'&mode_id='+my_index+'&way=1'
			a = requests.get(url3, headers)
			all_data = json.loads(a.text)
			title = decrypt(all_data['data']['title'])
			ops = []
			ops_id = []
			for i in range(len(all_data['data']['options'])):
				ops.append(decrypt(all_data['data']['options'][i]['title']))
				ops_id.append(all_data['data']['options'][i]['id'])
			url4 = 'https://ssxx.univs.cn/cgi-bin/race/answer/'
			if q_a.get(l, 0) != 0:
				post_answer = q_a[l]
			else:
				post_answer = [ops_id[0]]
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
				word = decrypt(ops[ops_id.index(k)])
				word_list.append(word)
			if q_a.get(l) == 0:
				q_a[l] = answer
			if l not in q_a:
				every_score -= 1
				q_a[l] = answer
				try:
					f.write(title)
				except:
					f.write(title[:12])
				f.write('\n')
				f.write(json.dumps(word_list,ensure_ascii=False))
				f.write('\n')
		url5 = "https://ssxx.univs.cn/cgi-bin/race/finish/"
		race = {"race_code":race_code}
		requests.post(url5, headers=headers, json=race)
