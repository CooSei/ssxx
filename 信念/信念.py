import requests
import json,time,os
try:
	all_ids = json.load(open('信念id.txt','r'))
	all_answer_id = json.load(open('信念answer_id.txt','r'))
	scores = json.load(open('信念score.txt','r'))
except:
	all_ids = []
	all_answer_id = []
	scores = []
every_score = 0
print(len(all_answer_id))
test = 0
strit = 0
size_1 = os.path.getsize('信念.txt')
while 1:
	if strit>500:
		break
	strit += 1
	size_2 = os.path.getsize('信念.txt')
	time.sleep(5)
	try:

		if size_2 - size_1 == 0:
			test += 1
			if test > 20:
				break
		else:
			size_1 = size_2
			test = 0
		print(strit)
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
		'Cookie': '_ga=GA1.2.406742327.1606105391;_gid=GA1.2.379454702.1606105391;tgw_l7_route=e05ea26683e7555591184c50c194d59f;_gat=1',
		}
		url = "https://ssxx.univs.cn/cgi-bin/authorize/token/?t="+this_time+"&uid=5fbb376da8faed8fbba03e7c&avatar=https:%2F%2Fnode2d-public.hep.com.cn%2Favatar-5fbb376da8faed8fbba03e7c-1606104941788&activity_id=5f71e934bcdbf3a8c3ba5061"
		response = requests.get(url, headers=headers)
		ll = json.loads(response.text)
		token = ll['token']
		url2 = 'https://ssxx.univs.cn/cgi-bin/race/beginning/?t='+this_time+'&activity_id=5f71e934bcdbf3a8c3ba5061&mode_id=5f71e934bcdbf3a8c3ba51d8&way=1'
		headers['Authorization'] = 'Bearer '+token
		response = requests.get(url2,headers=headers)
		question = json.loads(response.text)
		question_id = question['question_ids']
		race_code = question['race_code']
		headers['Referer'] = 'https://ssxx.univs.cn/client/exam/5f71e934bcdbf3a8c3ba5061/1/1/5f71e934bcdbf3a8c3ba51d8'
		every_score = 0
		with open('信念.txt','a') as f:
			for l in question_id:
				url3 = 'https://ssxx.univs.cn/cgi-bin/race/question/?t='+this_time+'&activity_id=5f71e934bcdbf3a8c3ba5061&question_id='+l+'&mode_id=5f71e934bcdbf3a8c3ba51d8'
				a = requests.get(url3,headers)
				all_data = json.loads(a.text)
				title = all_data['data']['title']
				ops = []
				ops_id = []
				for i in range(len(all_data['data']['options'])):
					ops.append(all_data['data']['options'][i]['title'])
					ops_id.append(all_data['data']['options'][i]['id'])
				url4 = 'https://ssxx.univs.cn/cgi-bin/race/answer/'
				if l in all_ids:
					post_answer = all_answer_id[all_ids.index(l)]
				else:
					post_answer = [ops_id[0]]
				data = {"activity_id":"5f71e934bcdbf3a8c3ba5061",
				        "question_id":l,
				        "answer":post_answer,
				        "mode_id":"5f71e934bcdbf3a8c3ba51d8",
				        "way":"1"
				        }
				post_data = requests.post(url4,headers=headers,json=data)
				answer_json = json.loads(post_data.text)
				answer = answer_json['data']['correct_ids']
				if answer_json['data']['correct'] == True:
					every_score += 1
				word_list = []
				for k in answer:
					word = ops[ops_id.index(k)]
					word_list.append(word)
				if l not in all_ids:
					all_ids.append(l)
					all_answer_id.append(answer)
					try:
						f.write(title)
					except:
						f.write(title[:12])
					f.write('\n')
					f.write(json.dumps(word_list,ensure_ascii=False))
					f.write('\n')
			url5 = "https://ssxx.univs.cn/cgi-bin/race/finish/"
			race = {"race_code":race_code}
			requests.post(url5,headers=headers,json=race)
		scores.append(every_score)
	except:
		strit += 10
		print(99999)
		time.sleep(10)
file = open('信念id.txt','w')
file.write(json.dumps(all_ids))
file.close()
file = open('信念answer_id.txt','w')
file.write(json.dumps(all_answer_id))
file.close()
file = open('信念score.txt','w')
file.write(json.dumps(scores))
file.close()
# os.system('shutdown -s -t 120')
