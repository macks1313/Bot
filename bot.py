import os
import tweepy
import openai
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)

def main():
    # Chargement des clés API depuis les variables d'environnement
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Initialisation de l'API Twitter
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Récupération des tendances mondiales (WOEID 1)
    try:
        trends_result = api.trends_place(1)
        trends = trends_result[0]['trends']
        # Extraction des hashtags ou, à défaut, des noms de tendance
        trend_list = [t['name'] for t in trends if t['name'].startswith('#')]
        if not trend_list:
            trend_list = [t['name'] for t in trends]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des tendances : {e}")
        trend_list = []

    # Création du prompt pour générer un tweet engageant
    prompt = (
        "Rédige un tweet original, court et percutant en français, "
        "intégrant un fait étonnant, une citation inspirante ou une référence tendance. "
        f"Utilise les tendances suivantes si possible : {', '.join(trend_list[:3])}. "
        "Ajoute des hashtags pertinents."
    )

    # Initialisation de l'API OpenAI et génération du contenu
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=60,
            temperature=0.8,
            n=1
        )
        tweet_text = response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Erreur lors de la génération du tweet : {e}")
        tweet_text = "Voici un tweet automatique pour partager une pensée positive. #Inspiration"

    # Publication du tweet sur Twitter
    try:
        api.update_status(tweet_text)
        logging.info("Tweet publié avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de la publication du tweet : {e}")

if __name__ == "__main__":
    main()
