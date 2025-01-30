import os
import tweepy
import openai
import time

# Récupérer les clés API depuis les variables d'environnement (Config Vars)
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Authentification Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Authentification OpenAI
openai.api_key = OPENAI_API_KEY

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

# Fonction pour publier un tweet automatiquement
def post_tweet():
    tweet = generate_tweet()
    try:
        api.update_status(tweet)
        print(f"Tweet publié : {tweet}")
    except tweepy.TweepError as e:
        print(f"Erreur : {e}")

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

# Fonction principale : Boucle pour publier toutes les 2 heures
def main():
    while True:
        print("\n=== Nouveau cycle ===")
        
        # Publier un tweet
        print("\nPublication d'un nouveau tweet...")
        post_tweet()

        # Répondre aux tweets d'un compte spécifique
        print("\nRéponse aux tweets spécifiques...")
        target_username = "elonmusk"  # Exemple : compte cible
        keywords = ["AI", "Tesla", "SpaceX"]
        reply_to_tweets_with_keywords(target_username, keywords)

        # Pause de 2 heures
        print("\nEn attente de 2 heures avant le prochain cycle...")
        time.sleep(7200)

# Lancer le script
if __name__ == "__main__":
    main()
