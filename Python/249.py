import requests 
import json
import threading
import os


def purchasePlan(token,phone_number):
	payload="platform=android&tml_flexiplan_bundle_id=CMP005001-00000000000000&gift=&voice=0&msisdn="+phone_number+"&data=25&addition_info=2017-1-29&type=Onnet&sms=0&lang=my&last_sync_time=2019-03-31+22%3A27%3A34&version_code=7&amount=39.88&validity=1&access_token="+token
	headers={'Content-Type': 'application/json','Content-Length': str(len(payload)),'Accept-Encoding': 'gzip, deflate','Content-Type': 'application/x-www-form-urlencoded'}
	url="https://flexiplan.telenor.com.mm/FlexiPlanAppBackend/api/v1/purchase_plan"
	r1=requests.post(url,headers=headers,data=payload)
	print("Purchased")

def activateBonus(token,phone_number,bonus_id):
	payload="platform=android&spin_bonus_id="+str(bonus_id)+"&lang=my&access_token="+token+"&msisdn="+phone_number+"&version_code=7&plan_id=CMP005001-00000000000000"
	headers={'Content-Type': 'application/json','Content-Length': str(len(payload)),'Accept-Encoding': 'gzip, deflate','Content-Type': 'application/x-www-form-urlencoded'}
	url="https://flexiplan.telenor.com.mm/FlexiPlanAppBackend/api/v1/spin-and-win/activate-bonus"
	r2=requests.post(url,headers=headers,data=payload)
	print(r2.text)

if __name__ == '__main__':
	print("LOL Flexi")
	token=input("Token :")
	phone_number=input("Phone Number :")
	number_of_time=input("Number of time :")
	bonus_id=249
	for i in range(0,int(number_of_time)):
		purchasePlan(token,phone_number)
		activateBonus(token,phone_number,bonus_id)