#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot Twitter automatisé pour promouvoir un compte OnlyFans avec l'aide de l'API OpenAI.
- Tweete 10 fois par jour à intervalles réguliers (1 tweet environ toutes les 2h24).
- Publie 2 tweets immédiatement au lancement.
- Gère les erreurs et permet le redémarrage automatique.
- Compatible Heroku/GitHub et utilisation des variables d'environnement.
"""

import os
import time
import schedule
import openai
import tweepy
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis un fichier .env
load_dotenv()

# Récupération des clés d'authentification Twitter
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Clé OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Authentification Twitter via Tweepy (API v1.1)
auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_SECRET,
    ACCESS_TOKEN,
    ACCESS_SECRET
)
api = tweepy.API(auth)

def generate_tweet():
    """
    Génère un tweet engageant via l'API OpenAI Chat (GPT-3.5).
    - Inclut une invitation à découvrir le compte OnlyFans.
    - Inclut un call-to-action et des hashtags pertinents.
    """
    prompt = (
        "Rédige un tweet court, percutant et intrigant pour promouvoir un compte OnlyFans. "
        "Inclus un call-to-action, une invitation à découvrir le compte, et "
        "des hashtags pertinents (#OnlyFans, #ExclusiveContent, #FollowMe)."
    )
    try:
        # Utilisation de ChatCompletion (GPT-3.5)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.7
        )
        # Récupère le contenu généré par GPT
        tweet_text = response.choices[0].message.content.strip()
        return tweet_text
    except Exception as e:
        print(f"Erreur OpenAI : {e}")
        # Message de secours en cas d'échec
        return "Découvrez mon contenu exclusif sur OnlyFans ! #OnlyFans #ExclusiveContent #FollowMe"

def send_tweet():
    """
    Récupère un texte généré et le poste sur Twitter.
    Gère les exceptions éventuelles lors de la publication.
    """
    tweet_content = generate_tweet()
    try:
        api.update_status(tweet_content)
        print(f"Tweet publié : {tweet_content}")
    except Exception as e:
        print(f"Erreur lors de l'envoi du tweet : {e}")

def main():
    """
    Programme principal :
    - Envoie immédiatement 2 tweets.
    - Programme ensuite l'envoi de 10 tweets par jour (1 tweet toutes les ~2h24).
    - Boucle infinie pour exécuter les tâches planifiées.
    """
    # 1. Publie 2 tweets immédiatement
    send_tweet()
    time.sleep(5)  # Petite pause pour éviter un enchaînement trop brutal
    send_tweet()

    # 2. Programme 10 tweets/jour => 1 tweet toutes les 2h24 (144 minutes)
    schedule.every(144).minutes.do(send_tweet)

    # 3. Boucle infinie pour exécuter les tweets planifiés
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Vérifie les tâches chaque minute
        except Exception as e:
            print(f"Erreur imprévue : {e}")
            time.sleep(60)  # Attend avant de réessayer

if __name__ == "__main__":
    main()
