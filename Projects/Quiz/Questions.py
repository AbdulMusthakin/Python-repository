import json
import requests

url = "https://opentdb.com/api.php?amount=10&type=boolean"
res = requests.get(url)

response1 = dict(json.loads(res.text))
response2 = response1['results']

response3 = {}
for item in response2:
    name = item['question']
    response3[name] = item

keys = ['question', 'correct_answer']
quiz = {}
for i in response3:
    quiz[i] = {'question' : response3[i]['question'], 'answer' : response3[i]['correct_answer']}
print(quiz)

