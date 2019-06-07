"""
zapier variables:
phone_number
contact_name
lead_id
"""

AUTHURL = 'https://<поддомен>.amocrm.ru/private/api/auth.php'
AUTHDATA = {'USER_HASH': '<API-ключ>', 'USER_LOGIN': 'логин'}
ADDCONTACTURL = 'https://<поддомен>.amocrm.ru/api/v2/contacts'
GETCONTACTURL = 'https://<поддомен>.amocrm.ru/private/api/v2/json/contacts'
NOTEURL = 'https://<поддомен>.amocrm.ru/api/v2/notes'

ACCOUNTURL = 'https://<поддомен>.amocrm.ru/private/api/v2/json/accounts/current'
POSTPARAMS = {'api_key': '<API-ключ>', 'login': '<логин>'}

session = requests.Session()
auth = session.post(url=AUTHURL, params=AUTHDATA)

existing_contacts = session.get(url=GETCONTACTURL, params=POSTPARAMS)
json_econtacts = existing_contacts.json()
response = json_econtacts['response']
for contact in response['contacts']:
    custom_fields = contact['custom_fields']
    for field in custom_fields:
        for value in field['values']:
            if value['value'] == str(input['phone_number']):
                # print('existed')
                JSONNOTEDATA = {
                    "add": [
                        {
                            "element_id": input['lead_id'],
                            "element_type": "2",
                            "text": "Получен запрос на заказ обратного звонка",
                            "note_type": "4"
                        }
                    ]
                }
                note = session.post(url=NOTEURL, json=JSONNOTEDATA)
                return

getuserdata = session.get(url=ACCOUNTURL, params=POSTPARAMS)
accountdata = getuserdata.json()
#print(testdata['response']['account'])
account = accountdata['response']['account']

# ПОЛУЧАЕМ СУЩЕСТВУЮЩИЕ ПОЛЯ
amoAllFields = account['custom_fields']    #Все поля
amoContactsFields = account['custom_fields']['contacts']    #Поля контактов
#print(amoContactsFields)

# ФОРМИРУЕМ МАССИВ С ЗАПОЛНЕННЫМИ ПОЛЯМИ КОНТАКТА
# Стандартные поля амо:
sFields = {
    'PHONE': '',
    'EMAIL': ''
}

# Проставляем id этих полей из базы амо
for afield in amoContactsFields:
    if afield['code'] in sFields:
        sFields[afield['code']] = afield['id']

# print(sFields['PHONE'])

JSONCONTACTDATA = {
    "add": [
        {
            "name": input['contact_name'],
            "leads_id": [
                input['lead_id']
            ],
            "custom_fields": [
                {
                    "id": sFields['PHONE'],
                    "values": [
                        {
                        "value": input['phone_number'],
                        "enum": "MOB"
                        }
                    ]
                }
            ]
        }
    ]
}

contact = session.post(url=ADDCONTACTURL, json=JSONCONTACTDATA)
