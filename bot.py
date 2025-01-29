import tweepy
import os
import time
from openai import OpenAI

# 🔹 Récupérer les clés API depuis les variables d'environnement Heroku
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Initialisation de Tweepy pour Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# 🔹 Initialisation de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# 🔹 Fonction pour générer un tweet sarcastique avec OpenAI
def generate_tweet():
    prompt = "Génère un tweet sarcastique et drôle sur un sujet d'actualité. Max 280 caractères."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content[:280]  # Twitter limite à 280 caractères

# 🔹 Fonction pour poster un tweet
def post_tweet():
    tweet = generate_tweet()
    api.update_status(tweet)
    print(f"Tweet envoyé : {tweet}")

# 🔹 Boucle pour tweeter toutes les 2 heures
while True:
    post_tweet()
    time.sleep(7200)  # 2 heures = 7200 secondes