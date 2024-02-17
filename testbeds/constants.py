import requests


users = {'dpappire': ('Druva','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jOWU2YjkzMi02OTMwLTQyMTktOWMzMi02MDg0NGZkYjVjZTY'),
        'rdongare': ('Rohit','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iZDViMjAyOC1kNjk4LTQwYjUtYTdmMC1jNzQzNDg3YzkxNjU')}

headers={'Authorization': 'Bearer OGNkNjAyZmMtMjMwOC00N2IwLWJmMWEtZTVlNThiOWJjYjM1Y2I1NjkxMjctZWNh_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f', 'Content-type': 'application/json;charset=utf-8'}

def send_webex_message(weekly_message, username, device, sending_user=None):
        body={'toPersonId': users[username][1]}
        message = f'Device **{device}** has been In Use for over a week please reserve it again or release it'
        if weekly_message:
                body['markdown'] = message
        else:
                body['markdown'] = f'Hi {users[username][0]},\n' + message + f'\n-{users[sending_user][0]} ({sending_user}@cisco.com)'

        requests.post('https://webexapis.com/v1/messages', json=body, headers=headers)