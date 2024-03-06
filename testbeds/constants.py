import requests


users = {'dpappire': ('Druva','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jOWU2YjkzMi02OTMwLTQyMTktOWMzMi02MDg0NGZkYjVjZTY'),
        'rdongare': ('Rohit','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iZDViMjAyOC1kNjk4LTQwYjUtYTdmMC1jNzQzNDg3YzkxNjU'),
        'shponnap': ('Shreya','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9lZTE0YTVhMC1mMzlkLTRlNGEtYTBlMi04MWUyZTEzZGY3ZmE'),
        'rajpill': ('Raj','Y2lzY29zcGFyazovL3VzL1BFT1BMRS84YzlkMDAxNi01NGRkLTQwZTktYTU3MS04MWI0OTVjYzVkNzE'),
        'alapham': ('Alan','Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wNGI5MGRmZC01MGJjLTRlYmEtOWU5ZC1lNDNmNzlkMWJlYzY'),
        'anujjai2': ('Anuj','Y2lzY29zcGFyazovL3VzL1BFT1BMRS85MGJjODYyNC0wMjNkLTRjZmMtODZlNi1mZGUxYzhjMDUzM2U'),
        'weilia': ('Wei','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9kODI2Njk5Ny05ZmViLTRmOTAtODFjYy0yMDJmMTBkYzE4Yzk'),
        'rskumar': ('Ramya','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9lNjk5MWQ4NS01ZGE5LTRiN2ItOGU0NS0xNDBiYzVmYTg4Zjg'),
        'sundaraj': ('Jaganathan','Y2lzY29zcGFyazovL3VzL1BFT1BMRS84MWQ1ZDBkMy03MGIzLTQyMmUtYjA2ZS0zMmVmOWY3MjljNDI')
        }

headers={'Authorization': 'Bearer OGNkNjAyZmMtMjMwOC00N2IwLWJmMWEtZTVlNThiOWJjYjM1Y2I1NjkxMjctZWNh_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f', 'Content-type': 'application/json;charset=utf-8'}

def send_webex_message(weekly_message, username, device, sending_user=None):
        body={'toPersonId': users[username][1]}
        message = f'Device **{device}** has been In Use for over a week please reserve it again or release it'
        if weekly_message:
                body['markdown'] = message
        else:
                body['markdown'] = f'Hi {users[username][0]},\n' + message + f'\n-{users[sending_user][0]} ({sending_user}@cisco.com)'

        requests.post('https://webexapis.com/v1/messages', json=body, headers=headers)