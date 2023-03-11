import json
import requests

url = "https://opentdb.com/api.php?amount=10&type=boolean"
res = requests.get(url)

response1 = dict(json.loads(res.text))
response2 = response1["results"]

print(response2)
for i in response2:
    # print each element of the list in a random color

    print(f"\033[32m {i['category']}")

    print(f"\033[33m {i['difficulty']}")

    # ansi code for pink:
    print(f"\033[35m {i['correct_answer']}")

    print(f"\033[34m {i['incorrect_answers']}")

    print(f"\033[31m {i['question']}")
