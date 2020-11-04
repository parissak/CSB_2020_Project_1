import requests

urlUser = 'http://localhost:8000/users/test'
urlAdmin = 'http://localhost:8000/admin'

session = requests.Session()
response = session.get(urlAdmin)
token = response.cookies['csrftoken']
 

response = session.post(urlUser, {'newPassword' : 'works', 'csrfmiddlewaretoken' : token })
print(response.text)
