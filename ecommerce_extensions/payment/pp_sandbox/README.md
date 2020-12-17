# Sandbox

This django project is a sandbox to make tests for the payment processor edupay.

## Usage

I recommend to follow this steps:

1. Create a virtual enviroment with python 3 for the sandbox, here is an [example](https://docs.python-guide.org/dev/virtualenvs/)
2. Install the requirements:
```bash
pip install -r requirements.txt
```
3. Run the app:
```bash
python manage.py runserver PORT
```
You can define the PORT number that you want.

### Configure ngrok
In order to use this sandbox in stage, i used ngrok.
1. Download [ngrok](https://ngrok.com/download) and create an account.
2. Once you install and connect your account, now you can start a http tunnel in the port that you defined for the sandbox:
```bash
./ngrok http PORT
```
3. Add the ngrok tunnel to ALLOWED_HOSTS in settings:

```python
ALLOWED_HOST = ['37f2d07894fe.ngrok.io', 'localhost']
```