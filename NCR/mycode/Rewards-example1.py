#!/usr/bin/python

import urllib
import json
import requests

url = 'http://153.73.247.25:8080/rewards/basket-rewards/1.0/calculate/1.1'
head = {"Content-Type": "application/json",
    "Accept-Language": "en-US",
    "Application-Key": "ECOM_URORA",
    "Organization-Key": "NCR",
    "EnterpriseUnitId": "ncrue1",
    "DeviceId": "1",
    "UserId": "pm185205",
    "Authorization": "123"}

transaction = {
    "transactionId": "02281551",
    "transactionFinal": False,
    "transactionBeginTime": "2019-02-28T15:52:12",
    "customerIds":
        [
            {
            "id": "0000000000000250329",
            "idType": "PRIMARY_MEMBER_CARD"
            }
        ],
    "saleItems":
        [
            {
            "sequenceId": "0001",
            "itemId": "501",
            "quantity":
                {
                "units": 6,
                "unitType": "SIMPLE_QUANTITY"
                },
            "unitPrice": 0.89,
            "discountable": True,
            "considerForBasketCondition": True
            }
        ],
    "totalCheck": True
}
payload = json.dumps(transaction)
print(json.dumps(transaction))
ret = requests.post(url, headers=head, data=payload)
print("status_code = ", ret.status_code)
print ("json = ", ret.json())
