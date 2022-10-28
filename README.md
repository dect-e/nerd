# Setup NERD

## create VENV and install requirements
```
python3 -mvenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## create config
copy sample-config src/nerf.cfg.example to src/nerd.cfg.
Add an E-Mail-Address to the from-Line.
Without an From-Line Dijango throws an error while sending an e-mail for the user register

## setup database
```
cd src
../venv/bin/python manage.py migrate
```

## start nerd
```
cd src
../venv/bin/python manage.py runserver
```

## register user and grant access to /admin

- register user on the website
- get your e-mail from src/emails/
- open the verification link

- stop nerd!!!
- open sqlite-db
- grant /admin access
```
update auth_user set is_staff = 1, is_superuser = 1;
```

## add extenstion

use the /admin Page