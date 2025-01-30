import tweepy
import openai
import os
import time
import random

# 🔹 Récupérer les clés API depuis les variables d'environnement Heroku
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Vérification des clés API
if not API_KEY or not API_SECRET or not ACCESS_TOKEN or not ACCESS_SECRET or not BEARER_TOKEN or not OPENAI_API_KEY:
    print("❌ Erreur : Une ou plusieurs clés API sont manquantes ! Vérifie les Config Vars sur Heroku.")
    exit(1)

# 🔹 Configuration de l’API Twitter v2 avec OAuth2
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
    bearer_token=BEARER_TOKEN
)

# 🔹 Configuration de OpenAI
openai.api_key = OPENAI_API_KEY

# 🔹 Liste de hashtags populaires (change-les selon l'actualité si besoin)
popular_hashtags = [
    "#trending", "#viral", "#comedy", "#NSFW", "#joke", "#sarcasm", "#darkhumor",
    "#funny", "#memes", "#fyp", "#WTF", "#epic", "#TwitterHumor"
]

# 🔹 Fonction pour générer un tweet sarcastique avec OpenAI GPT-4
def generate_tweet():
    prompt = (
        "You are a highly sarcastic and witty AI with a sharp sense of humor, designed to entertain and provoke thought with subtle dark humor. 
Your tweets cover topics like the absurdity of life, bad decisions, dating struggles, the futility of Mondays, and AI slowly taking over the world.
Maintain a balance between humor, sarcasm, and relatability. 
Always include popular hashtags to boost engagement, such as #AI, #Humor, #Sarcasm, #MondayMood, #DatingFails, and #LifeStruggles. 
Keep the tweets short, clever, and perfect for retweets.
Avoid crossing into offensive or explicit territory."
        "Make it under 270 characters and with emoji."
    )

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    tweet = response.choices[0].message.content[:250]  # On laisse un peu de place pour les hashtags

    # 🔹 Ajouter un hashtag aléatoire
    hashtag = random.choice(popular_hashtags)
    tweet_with_hashtag = f"{tweet} {hashtag}"

    return tweet_with_hashtag

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
