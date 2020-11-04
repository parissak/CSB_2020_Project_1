# CSB_2020_Project_1

The first course project for University of Helsinki's course "Cyber Security Base 2020".

According to the project instructions, the task "*is to create a web application that has at least five different flaws from the OWASP top ten list.*" 

The app was created with Python & Django.

---
## Installation instructions
1. Download or git clone the existing project.
2. Create necessary database tables with the following command: python3 manage.py migrate
3. Create an admin user with following command: python manage.py createsuperuser and enter username (in this project 'admin' was used), email and password. 
4. Start the app with the following command: python3 manage.py runserver

Note: the app doesn't contain database or any existing users so for possible testing purposes users should be created manually. The app includes functionality for registration.

---
## Flaws

### Cross-Site Scripting (XSS):
**Description of the flaw**: The apps message.html contains an XSS vulnerability: the relevant text field will run JavaScript code. User could send malicious code to a different end user with the messaging system.  

**Example**: 
1. Login an existing user and navigate to the user's messages page.
2. Type a script (for example <script>alert(document.cookie)</script>) to the message box and send it to some user.
3. Now whenever the message page is rendered by the messages sender or receiver, an alert containing the users cookies will pop up.

**Fix**: Currently the 'safe' template tag is added to message content in the html template. This tag marks a string to not require HTML escaping prior to output. So a simple fix to prevent aforementioned script from running is to remove the tag. Also in the settings SESSION_COOKIE_HTTPONLY should be set to True or the line removed completely to prevent the client to have an access to session related cookie (this is more a security misconfiguration though).

### Broken Authentication:
**Description of the flaw**: The application allows weak passwords (only password length is checked, which is only 3). This is because the Django's default password validation settings were removed / bypassed. Weak passwords make for example brute-force attacks, like password spraying, possible.

**Example**: 
1. Try to register a new user with a weak password (example '1234') - it will work.

**Fix**: Proper validation for passwords should be implemented: password confirmation should be required and passwords should be required to be complex and not common. Django's default configuration for password validation meets all these requirements. 

### Broken Access Control:
**Description of the flaw**: An unauthorized user has an access to functionality that changes user passwords. This is because the user is not validated properly: the user is fetched based on the URL parameter alone. An unauthorized user can change any users password to his or hers liking because of this.

**Example**: 
Create the following python script and run it while the server is also running ("test" is considered to be an existing user):
```python
import requests
urlUser = 'http://localhost:8000/users/test'
urlAdmin = 'http://localhost:8000/admin'
session = requests.Session()
response = session.get(urlAdmin)
token = response.cookies['csrftoken']
response = session.post(urlUser, {'newPassword' : 'test', 'csrfmiddlewaretoken' : token })
```
**Fix**: The current user should be validated and user should be fetched with an user object related to session. Also the relevant password form should contain some validation, like require old password and require to retype the new one. 

### Security misconfiguration:
**Description of the flaw**: Debugging is turned on and therefore detailed error pages are rendered whenever an error is encountered. This will reveal unnecessary and detailed information, like the app's configuration, about the app to the user. This information could help an attacker to gain more information about the system. Another security misconfiguration is that the admin account uses default username. 

**Example**:
1. Type some nonexisting username after localhost:8000/users/ to the address bar.
2. App's settings are shown.

**Fix**: Turning debugging to false and defining allowed_hosts (for example '.localhost' for testing) in the configuration settings will prevent the unnecessary debugging information from showing. The app's methods also should return relevant HTTP status codes when an error is encountered, for example status code 403 if the user is not authorized to do some action. The default username for admin account should be changed and adding some other non-default url to the admin site should be considered for security reasons as this could mitigate some automated attacks. 

### Sensitive data:
**Description of the flaw**: App's sensitive data, user passwords in this case, are not protected properly. Stored passwords are hashed with unsalted MD5, which is considered unsafe as it allows the passwords to be cracked. Cracking unsalted MD5 is possible with some dedicated tools and you can find hashes for common and weak passwords from online databases. Therefore if the database is breached, the passwords are also compromised. Worse solution would have been to use plaintext passwords, but this was way more complicated to implement in Django, so unsalted MD5 was used. Another flaw is that app only supports HTTP: the data is transmitted in clear text, which allows malicious user to sniff information transferred between the app and client.

**Example**:  
1. Create new user with a weak password (for example 'password' or '1234').
2. Get the password (for example manually from database).
3. Crack the password with some downloadable app or decrypt the password in an online database.

**Fix**: More robust hashing function and salting should be used. Djangos default settings are enough, so they should be restored and the current password hasher in the settings should be removed. Also the app should be configured to use HTTPS.
