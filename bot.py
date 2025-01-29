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

# 🔹 Vérification des clés API
if not API_KEY or not API_SECRET or not ACCESS_TOKEN or not ACCESS_SECRET or not OPENAI_API_KEY:
    print("❌ Erreur : Une ou plusieurs clés API sont manquantes ! Vérifie les Config Vars sur Heroku.")
    exit(1)

# 🔹 Configuration de l’API Twitter v2
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# 🔹 Configuration de OpenAI
openai.api_key = OPENAI_API_KEY

# 🔹 Fonction pour générer un tweet sarcastique avec OpenAI GPT-4
def generate_tweet():
    prompt = "Génère un tweet sarcastique et drôle sur un sujet d'actualité en moins de 280 caractères."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content[:280]  # Limite à 280 caractères

# 🔹 Fonction pour poster un tweet
def post_tweet():
    try:
        tweet = generate_tweet()
        response = client.create_tweet(text=tweet)
        print(f"✅ Tweet envoyé : {tweet}, ID: {response.data['id']}")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi du tweet : {e}")

# 🔹 Boucle pour tweeter toutes les 2 heures
while True:
    post_tweet()
    time.sleep(7200)  # 2 heures