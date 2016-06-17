from requests import session

payload = {
    'action': 'login',
    'username': 'user',
    'password': 'pass'
}

with session() as c:
    c.post('http://djland.citr.ca/index.php', data=payload)
    for i in range (1,456):
        response = c.get('http://djland.citr.ca/api2/public/show/' + str(i) + '/xml')
        print(response.headers)
        print(response.text)
