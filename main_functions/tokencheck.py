from requests import get

def check_token(authorization):
    headers = {'Content-Type': 'application/json', 'authorization': authorization}
    url = "https://discordapp.com/api/v6/users/@me/library"
    response = get(url, headers=headers)
    if response.status_code == 200:
        token = authorization
        return 'Valid token'
    else:
        return 'Invalid token'