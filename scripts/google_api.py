import requests
import googleapiclient

url = "https://googlebooksraygorodskijv1.p.rapidapi.com/getVolume"

payload = "accessToken=%3CREQUIRED%3E&volumeId=%3CREQUIRED%3E"
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Key": "afa27ff828mshd13581cf9059468p1d870ajsn31b29e38cb14",
    "X-RapidAPI-Host": "GoogleBooksraygorodskijV1.p.rapidapi.com"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
