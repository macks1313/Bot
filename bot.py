import tweepy
import openai
import os
import time

# 🔹 Récupérer les clés API depuis les variables d'environnement Heroku
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Authentification avec Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# 🔹 Fonction pour générer un tweet sarcastique avec GPT-4
def generate_tweet():
    prompt = "Génère un tweet sarcastique et drôle sur un sujet d'actualité. Max 280 caractères."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )
    
    return response["choices"][0]["message"]["content"][:280]  # Twitter limite à 280 caractères

# 🔹 Fonction pour poster un tweet
def post_tweet():
    tweet = generate_tweet()
    api.update_status(tweet)
    print(f"Tweet envoyé : {tweet}")

# 🔹 Boucle pour tweeter toutes les 2 heures
while True:
    post_tweet()
    time.sleep(7200)  # 2 heures = 7200 secondes