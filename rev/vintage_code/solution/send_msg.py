import requests

webhook_url = "https://discord.com/api/webhooks/1323648717194137620/OQRcCZo4JWbk9hrQgqjtWSI1KE2otS9oaIAB16_WP8ywN-hAdEDbVYhgWQSqBkL62Jdn"

data = {"content": "Toasters got the flag", "username": "Toasters"}

requests.post(webhook_url, json=data)
