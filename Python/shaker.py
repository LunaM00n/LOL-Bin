import requests
import json


def buyPack(token):
	auth={"Accept-Encoding":"gzip, deflate","authorization":token,"User-Agent":"MyTM/3.1.0/Android/19","Content-Length": "56"}
	url='https://mytm.telenor.com.mm/mytmapi/v1/en/packs/buy'
	payload={"offerId":"6X1000Ks","isCmp":0,"packId":25,"fee":0.0}
	r1=requests.post(url,headers=auth,data=json.dumps(payload))
	data=json.loads(r1.text)
	requestId=data['data']['attribute']['requestId']
	print(requestId)
	shake_url='https://mytm.telenor.com.mm/mytmapi/v1/en/shake-n-win'
	shakemal={"requestId":requestId}
	r2=requests.post(shake_url,headers=auth,data=json.dumps(shakemal))
	result=json.loads(r2.text)
	amount=result['data']['attribute']['offerWin']
	print(amount)

def balance(token):
	auth={"Accept-Encoding":"gzip, deflate","authorization":token,"User-Agent":"MyTM/3.1.0/Android/19"}
	url='https://mytm.telenor.com.mm/mytmapi/v1/mm/all-balance'
	r3=requests.get(url,headers=auth)
	data=json.loads(r3.text)
	Total=data['data']['attribute']['packsPieData']['data']['convertRemaining']
	print("---------------------------")
	print("Congrats! You have "+str(Total)+" GB.")

if __name__ == '__main__':
	print("LOL Telenor")
	get_token=raw_input("Token :")
	token="Bearer "+get_token
	numberOfLuck=raw_input("Excuse Luck :")
	for i in xrange(1,int(numberOfLuck)):
		print(i)
		print("-----------------------")
		buyPack(token)
	balance(token)	