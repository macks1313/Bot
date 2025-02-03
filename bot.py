import os
import tweepy
import openai
import logging
import random

logging.basicConfig(level=logging.INFO)

def main():
    # Chargement des clés API depuis les variables d'environnement
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_SECRET = os.getenv("ACCESS_SECRET")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # Non utilisé ici
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    logging.info("Startup: posting a tweet to demonstrate functionality.")

    # Initialisation de l'API Twitter (OAuth 1.1)
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Récupération des tendances pour les États-Unis (WOEID 23424977)
    try:
        # Tweepy peut proposer get_place_trends si trends_place n'existe pas
        if hasattr(api, "trends_place"):
            trends_result = api.trends_place(23424977)
        else:
            trends_result = api.get_place_trends(23424977)
        trends = trends_result[0]['trends']
        trend_list = [t['name'] for t in trends if t['name'].startswith('#')]
        if not trend_list:
            trend_list = [t['name'] for t in trends]
    except Exception as e:
        logging.error(f"Error fetching trends: {e}")
        trend_list = []

    # Définition des templates de prompt en anglais
    templates = [
        "Compose an engaging tweet that shares an amazing fact and includes trending topics: {trends}. Add relevant hashtags.",
        "Write a witty and inspiring tweet with a motivational quote. Use trending topics: {trends} and add hashtags.",
        "Create a creative tweet about current trends with a humorous twist. Incorporate trending topics: {trends} and relevant hashtags.",
        "Generate an interactive tweet by asking a question about trending topics: {trends}. Include popular hashtags."
    ]
    chosen_template = random.choice(templates)
    trends_str = ", ".join(trend_list[:3]) if trend_list else ""
    prompt = chosen_template.format(trends=trends_str)

    # Génération du tweet avec OpenAI (utilisation de gpt-3.5-turbo)
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

    # Publication du tweet (texte uniquement, sans média)
    try:
        api.update_status(status=tweet_text)
        logging.info("Tweet posted successfully.")
    except Exception as e:
        logging.error(f"Error posting tweet: {e}")

if __name__ == "__main__":
    main()
