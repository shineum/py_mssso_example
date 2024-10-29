Django Sample Project for Azure SSO


# Prerequisites
Install Python 3.12.x or later

Create Azure App with MS Azure Protal "App registrations".
These information from Azure App are required.
- Directory (tenant) ID (Overview)
- Application (client) ID (Overview)
- Client secret (Manage - Certificates & secrets)
- scopes (Manage - API permissions)
- redirect url (Manage - Authentication - Web Redirect URIs)
<br>
Redirect url for this sample is:<br>
http://localhost:8000/sso_login_callback/<br>
(Can be vary depending on port. it is assumed that port will be 8000 for this sample.)<br>

# Installation

#### Download source code
```
git clone https://github.com/shineum/py_mssso_sample.git
```

#### Change working directory
```
cd py_mssso_sample
```

#### Set environment variables
copy sample.env to .env<br>
open .env file<br>
fill in the required values


#### Setup vritual environment
```
python -m venv .venv
```

#### Activate vritual environment
For linux or macos
```
source ./.venv/bin/activate
```
For windows (cmd)
```
.\.venv\Scripts\activate.bat
```

#### Install modules
```
python -m pip install -r requirements.txt
```

#### Initialize DB
```
python manage.py migrate
```

#### Run server
```
python manage.py runserver
```

# Test
Open browser and type in this url:<br>
http://localhost:8000<br>
<br>
According to the login status text will be different.<br>
When you click sso login link, it will redirect to MS login page.<br>
Login with ms account, then it will be back to redirect url.<br>