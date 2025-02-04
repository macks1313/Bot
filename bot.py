#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot Twitter automatisé pour promouvoir un compte OnlyFans avec l'aide de l'API OpenAI.
- Tweete 10 fois par jour à intervalles réguliers.
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

# Authentification Twitter via Tweepy
auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_SECRET,
    ACCESS_TOKEN,
    ACCESS_SECRET
)
api = tweepy.API(auth)

def generate_tweet():
    """
    Génère un tweet engageant via l'API OpenAI (GPT).
    - Inclut une invitation à découvrir le compte OnlyFans.
    - Inclut un call-to-action et des hashtags pertinents.
    """
    prompt = (
        "Rédige un tweet court, percutant et intrigant pour promouvoir un compte OnlyFans. "
        "N'oublie pas d'inclure un call-to-action, une invitation à découvrir le compte, et "
        "les hashtags pertinents (#OnlyFans, #ExclusiveContent, #FollowMe)."
    )
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=60,
            temperature=0.7,
            n=1
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Erreur OpenAI : {e}")
        # Message de secours en cas d'échec
        return "Découvrez vite mon contenu exclusif sur OnlyFans ! #OnlyFans #ExclusiveContent #FollowMe"

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
    time.sleep(5)  # Petite pause pour éviter d'enchaîner trop vite
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
            time.sleep(60)  # Attend avant de retenter

if __name__ == "__main__":
    main()
