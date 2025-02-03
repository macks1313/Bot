import os
import tweepy
import openai
import logging
import random

logging.basicConfig(level=logging.INFO)

def main():
    # Chargement des clés API depuis les Config Vars
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_SECRET = os.getenv("ACCESS_SECRET")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    logging.info("Startup: posting a tweet to demonstrate functionality.")

    # Initialisation du client Twitter v2 pour publier le tweet
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )

    # Récupération des tendances via l'API v1.1 (si autorisé), sinon on utilise une liste vide
    trend_list = []
    try:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
        trends_result = api_v1.trends_place(23424977)  # US WOEID
        trends = trends_result[0]['trends']
        trend_list = [t['name'] for t in trends if t['name'].startswith('#')]
        if not trend_list:
            trend_list = [t['name'] for t in trends]
    except Exception as e:
        logging.error(f"Error fetching trends: {e}")
        trend_list = []

    # Création du prompt pour OpenAI
    templates = [
        "Compose an engaging tweet that shares an amazing fact and includes trending topics: {trends}. Add relevant hashtags.",
        "Write a witty and inspiring tweet with a motivational quote. Use trending topics: {trends} and add hashtags.",
        "Create a creative tweet about current trends with a humorous twist. Incorporate trending topics: {trends} and relevant hashtags.",
        "Generate an interactive tweet by asking a question about trending topics: {trends}. Include popular hashtags."
    ]
    chosen_template = random.choice(templates)
    trends_str = ", ".join(trend_list[:3]) if trend_list else ""
    prompt = chosen_template.format(trends=trends_str)

    # Génération du tweet avec OpenAI (GPT-3.5 Turbo)
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative tweet generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=60
        )
        tweet_text = response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating tweet: {e}")
        tweet_text = "Here's an inspiring tweet for you. #Inspiration"

    logging.info(f"Tweet text: {tweet_text}")

    # Publication du tweet via le client v2
    try:
        client.create_tweet(text=tweet_text)
        logging.info("Tweet posted successfully.")
    except Exception as e:
        logging.error(f"Error posting tweet: {e}")

if __name__ == "__main__":
    main()
