# CSB_2020_Project_1

The first course project for University of Helsinki's course "Cyber Security Base 2020".

According to the project instructions, the task "*is to create a web application that has at least five different flaws from the OWASP top ten list.*" 

The app was created with Python & Django.

---
## Installation instructions

---
## Flaws

### Cross-Site Scripting (XSS):
**Flaw**: The apps message.html contains an XSS vulnerability: the relevant text field will run JavaScript code.

**Example**: 
1. Login and go to the messages page
2. Type a script (for example <script>alert(document.cookie)</script>) to the message box and send it to some user.
3. Now whenever the message page is rendered by the messages sender or receiver, an alert containing the users cookies will pop up

**Fix**: Currently the 'safe' template tag is added to message content in the html template. This tag marks a string to not require HTML escaping prior to output. So a simple fix to prevent aforementioned script from running is to remove the tag. Also in the settings SESSION_COOKIE_HTTPONLY should be set to True or the line removed completely to prevent the client to have an access to session related cookie (this is more a security misconfiguration though).

### Broken Authentication:
**Flaw**: The application allows weak passwords (only password length is checked, which is only 3) because the default password validation settings are removed / bypassed. Weak passwords make for example brute-force attacks, like password spraying, possible.

**Fix**: Proper validation for passwords should be implemented: require password confirmation and require that passwords are complex and not common. Django's default configuration for validation meets all these requirements. 

### Broken Access Control:
**Flaw**: The method that changes password is not coded properly: user object is fetched with username from url parameter. An unauthorized user can change any users password because of this.

**Example**: 
Create and run the following script ("test" is an existing user):
```python
import requests
urlUser = 'http://localhost:8000/users/test'
urlAdmin = 'http://localhost:8000/admin'
session = requests.Session()
response = session.get(urlAdmin)
token = response.cookies['csrftoken']
response = session.post(urlUser, {'newPassword' : 'test', 'csrfmiddlewaretoken' : token })
```
**Fix**: Password should be changed with an user object related to request. Also the relevant form should contain some validation relating to password change, like require old password and retyping the new one. 

### Security misconfiguration:
**Flaw**: Debugging is left on and this exposes app's url patterns (including admin site) and programming logic when error occurs.

**Example**:
1. Type localhost:8000/allUlrs
2. Examine urls including the admin site.

**Fix**:
Turn debugging to false in the configuration settings and define allowed_hosts (for example '.localhost' for testing). Also the admin site should be behind some other, non-default, url for security reasons. The app should return HTTP status codes when an error is encountered. 

### Sensitive data:
**Flaw**: Passwords are hashed with unsalted MD5, which makes the passwords vulnerable for brute-force attacks. Cracking unsalted MD5 is possible and you can find hashes for common and weak passwords from online databases. Therefore if the database is breached, the passwords are also compromised. Worse solution would have been to use plaintext passwords, but this was way more complicated to implement in Django. Another flaw is that app only supports HTTP.

**Example**:  
1. Create new user with a weak password (for example 'password' or '1234').
2. Get the password (for example manually from database).
3. Crack the password with some downloadable app or decrypt the password in an online database.

**Fix**: A better hashing function and salting should be used. Djangos default settings are enough, so the current password hasher in the settings can be removed.
Also the app should be configured to use HTTPS.
