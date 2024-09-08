import requests
import random


users = {'user1_cec_id': ('User1 Name','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jOWU2YjkzMi02OTMwLTQyMTktOWMzMi02MDg0NGZkYjVjZTY'),
        'user2_cec_id': ('User2 Name','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iZDViMjAyOC1kNjk4LTQwYjUtYTdmMC1jNzQzNDg3YzkxNjU'),
        'user3_cec_id': ('User3 Name','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9lZTE0YTVhMC1mMzlkLTRlNGEtYTBlMi04MWUyZTEzZGY3ZmE'),
        'user4_cec_id': ('User4 Name','Y2lzY29zcGFyazovL3VzL1BFT1BMRS84YzlkMDAxNi01NGRkLTQwZTktYTU3MS04MWI0OTVjYzVkNzE'),
        'user5_cec_id': ('User5 Name','Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wNGI5MGRmZC01MGJjLTRlYmEtOWU5ZC1lNDNmNzlkMWJlYzY'),
        'user6_cec_id': ('User6 Name','Y2lzY29zcGFyazovL3VzL1BFT1BMRS85MGJjODYyNC0wMjNkLTRjZmMtODZlNi1mZGUxYzhjMDUzM2U'),
        'user7_cec_id': ('User7 Name','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9kODI2Njk5Ny05ZmViLTRmOTAtODFjYy0yMDJmMTBkYzE4Yzk'),
        'user8_cec_id': ('User8 Name','Y2lzY29zcGFyazovL3VzL1BFT1BMRS9lNjk5MWQ4NS01ZGE5LTRiN2ItOGU0NS0xNDBiYzVmYTg4Zjg'),
        'user9_cec_id': ('User9 Name','Y2lzY29zcGFyazovL3VzL1BFT1BMRS84MWQ1ZDBkMy03MGIzLTQyMmUtYjA2ZS0zMmVmOWY3MjljNDI')
        }

headers={'Authorization': 'Bearer <Token ID>', 'Content-type': 'application/json;charset=utf-8'}
def send_webex_message(username):
        body={'toPersonId': users[username][1]}
        random_code = ''.join(random.choices('0123456789', k=5))
        message = f'Enter the code {random_code}'
        body['markdown'] = message

        requests.post('https://webexapis.com/v1/messages', json=body, headers=headers)
        return random_code
