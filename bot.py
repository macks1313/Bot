import os
import tweepy
import openai
import os
import time
import random

# 🔹 Récupérer les clés API depuis les variables d'environnement Heroku
# Récupérer les clés API depuis les variables d'environnement (Config Vars)
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
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
# Authentification Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# 🔹 Configuration de OpenAI
# Authentification OpenAI
openai.api_key = OPENAI_API_KEY

# 🔹 Liste de hashtags populaires (change-les selon l'actualité si besoin)
popular_hashtags = [
    "#trending", "#viral", "#comedy", "#NSFW", "#joke", "#sarcasm", "#darkhumor",
    "#funny", "#memes", "#fyp", "#WTF", "#epic", "#TwitterHumor"
]
# 🔹 Fonction pour générer un tweet sarcastique avec OpenAI GPT-4
def generate_tweet():
    prompt = (
        "Write a sarcastic, slightly dark-humored and NSFW-friendly joke about a trending topic."
        "Make it under 280 characters and add a popular hashtag at the end."
    )
# Fonction pour générer un tweet avec humour sarcastique et adulte
def generate_tweet(topic="daily life or technology"):
    personality = """
    You are a highly sarcastic AI with an adult sense of humor. Your tweets are witty, provocative, and slightly dark. 
    You joke about relationships, bad decisions, Mondays, AI taking over, and life's absurdity.
    Keep it funny and sharp, but don't cross the line into offensive or explicit content.
    """
    prompt = f"{personality}\n\nWrite a sarcastic, funny tweet about {topic}:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
        temperature=0.85
    )
    tweet = response.choices[0].text.strip()
    return tweet

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
# Fonction pour publier un tweet automatiquement
def post_tweet():
    tweet = generate_tweet()
    try:
        api.update_status(tweet)
        print(f"Tweet publié : {tweet}")
    except tweepy.TweepError as e:
        print(f"Erreur : {e}")

    tweet = response.choices[0].message.content[:250]  # On laisse un peu de place pour les hashtags
# Fonction pour répondre automatiquement aux tweets spécifiques
def reply_to_tweets_with_keywords(target_username, keywords):
    try:
        tweets = api.user_timeline(screen_name=target_username, count=5)
        for tweet in tweets:
            if any(keyword.lower() in tweet.text.lower() for keyword in keywords):
                response = generate_tweet(topic=f"a reply to: '{tweet.text}'")
                api.update_status(
                    f"@{target_username} {response}",
                    in_reply_to_status_id=tweet.id
                )
                print(f"Réponse publiée : {response}")
    except tweepy.TweepError as e:
        print(f"Erreur : {e}")

    # 🔹 Ajouter un hashtag aléatoire
    hashtag = random.choice(popular_hashtags)
    tweet_with_hashtag = f"{tweet} {hashtag}"
# Fonction principale : Boucle pour publier toutes les 2 heures
def main():
    while True:
        print("\n=== Nouveau cycle ===")
        
        # Publier un tweet
        print("\nPublication d'un nouveau tweet...")
        post_tweet()

    return tweet_with_hashtag
        # Répondre aux tweets d'un compte spécifique
        print("\nRéponse aux tweets spécifiques...")
        target_username = "elonmusk"  # Exemple : compte cible
        keywords = ["AI", "Tesla", "SpaceX"]
        reply_to_tweets_with_keywords(target_username, keywords)

# 🔹 Fonction pour poster un tweet
def post_tweet():
    try:
        tweet = generate_tweet()
        response = client.create_tweet(text=tweet)
        print(f"✅ Tweet envoyé : {tweet}, ID: {response.data['id']}")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi du tweet : {e}")
        # Pause de 2 heures
        print("\nEn attente de 2 heures avant le prochain cycle...")
        time.sleep(7200)

# 🔹 Boucle pour tweeter toutes les 2 heures
while True:
    post_tweet()
    time.sleep(7200)  # 2 heures
# Lancer le script
if __name__ == "__main__":
    main()
