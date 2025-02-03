import os
import tweepy
import openai
import logging
import random
import requests
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    # Load API keys from environment variables
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    logging.info("Startup: posting a tweet to demonstrate functionality.")

    # Initialize Twitter API
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Retrieve trending topics for the US (WOEID 23424977)
    try:
        trends_result = api.trends_place(23424977)
        trends = trends_result[0]['trends']
        trend_list = [t['name'] for t in trends if t['name'].startswith('#')]
        if not trend_list:
            trend_list = [t['name'] for t in trends]
    except Exception as e:
        logging.error(f"Error fetching trends: {e}")
        trend_list = []

    # Define prompt templates in English
    templates = [
        "Compose an engaging tweet that shares an amazing fact and includes trending topics: {trends}. Add relevant hashtags.",
        "Write a witty and inspiring tweet with a motivational quote. Use trending topics: {trends} and add hashtags.",
        "Create a creative tweet about current trends with a humorous twist. Incorporate trending topics: {trends} and relevant hashtags.",
        "Generate an interactive tweet by asking a question about trending topics: {trends}. Include popular hashtags."
    ]
    chosen_template = random.choice(templates)
    trends_str = ", ".join(trend_list[:3]) if trend_list else ""
    prompt = chosen_template.format(trends=trends_str)

    # Generate tweet text using OpenAI
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
        logging.error(f"Error generating tweet: {e}")
        tweet_text = "Here's an inspiring tweet for you. #Inspiration"

    # Download a random image from Unsplash for enhanced engagement
    media_ids = []
    try:
        image_url = "https://source.unsplash.com/random/800x600"
        img_response = requests.get(image_url, timeout=10)
        if img_response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(img_response.content)
                tmp_file.flush()
                media = api.media_upload(tmp_file.name)
                media_ids.append(media.media_id_string)
    except Exception as e:
        logging.error(f"Error fetching or uploading image: {e}")

    # Post the tweet (with media if available)
    try:
        api.update_status(status=tweet_text, media_ids=media_ids if media_ids else None)
        logging.info("Tweet posted successfully.")
    except Exception as e:
        logging.error(f"Error posting tweet: {e}")

if __name__ == "__main__":
    main()
