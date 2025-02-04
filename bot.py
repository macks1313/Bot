import tweepy
import openai
import os
import time
import schedule
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Variables d'environnement
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Authentification Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Authentification OpenAI
openai.api_key = OPENAI_API_KEY

def generate_tweet():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a marketing assistant specialized in generating engaging tweets for an OnlyFans account."},
                {"role": "user", "content": "Generate a tweet to promote an OnlyFans account. Make it engaging, with a call-to-action and relevant hashtags."}
            ],
            max_tokens=280
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating tweet: {e}")
        return None

def post_tweet():
    tweet = generate_tweet()
    if tweet:
        try:
            twitter_api.update_status(tweet)
            print(f"Tweet posted: {tweet}")
        except Exception as e:
            print(f"Error posting tweet: {e}")
    else:
        print("No tweet generated.")

# Poster deux tweets au démarrage
print("Posting initial tweets...")
post_tweet()
time.sleep(10)  # Pause de 10 secondes entre les deux tweets
post_tweet()

# Planification des tweets (10 fois par jour)
schedule.every().day.at("09:00").do(post_tweet)
schedule.every().day.at("11:00").do(post_tweet)
schedule.every().day.at("13:00").do(post_tweet)
schedule.every().day.at("15:00").do(post_tweet)
schedule.every().day.at("17:00").do(post_tweet)
schedule.every().day.at("19:00").do(post_tweet)
schedule.every().day.at("21:00").do(post_tweet)
schedule.every().day.at("23:00").do(post_tweet)
schedule.every().day.at("01:00").do(post_tweet)
schedule.every().day.at("03:00").do(post_tweet)

print("Bot is running...")
while True:
    schedule.run_pending()
    time.sleep(60)
