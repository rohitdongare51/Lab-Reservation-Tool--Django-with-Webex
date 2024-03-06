import requests
import random


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

# shponnap Y2lzY29zcGFyazovL3VzL1BFT1BMRS9lZTE0YTVhMC1mMzlkLTRlNGEtYTBlMi04MWUyZTEzZGY3ZmE
# rajpill Y2lzY29zcGFyazovL3VzL1BFT1BMRS84YzlkMDAxNi01NGRkLTQwZTktYTU3MS04MWI0OTVjYzVkNzE
# dpappire Y2lzY29zcGFyazovL3VzL1BFT1BMRS9jOWU2YjkzMi02OTMwLTQyMTktOWMzMi02MDg0NGZkYjVjZTY
# alapham Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wNGI5MGRmZC01MGJjLTRlYmEtOWU5ZC1lNDNmNzlkMWJlYzY
# anujjai2 Y2lzY29zcGFyazovL3VzL1BFT1BMRS85MGJjODYyNC0wMjNkLTRjZmMtODZlNi1mZGUxYzhjMDUzM2U
# weilia Y2lzY29zcGFyazovL3VzL1BFT1BMRS9kODI2Njk5Ny05ZmViLTRmOTAtODFjYy0yMDJmMTBkYzE4Yzk
# rskumar Y2lzY29zcGFyazovL3VzL1BFT1BMRS9lNjk5MWQ4NS01ZGE5LTRiN2ItOGU0NS0xNDBiYzVmYTg4Zjg

headers={'Authorization': 'Bearer OGNkNjAyZmMtMjMwOC00N2IwLWJmMWEtZTVlNThiOWJjYjM1Y2I1NjkxMjctZWNh_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f', 'Content-type': 'application/json;charset=utf-8'}
def send_webex_message(username):
        body={'toPersonId': users[username][1]}
        random_code = ''.join(random.choices('0123456789', k=5))
        message = f'Enter the code {random_code}'
        body['markdown'] = message

        requests.post('https://webexapis.com/v1/messages', json=body, headers=headers)
        return random_code