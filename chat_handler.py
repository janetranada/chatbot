import random
import requests
from better_profanity import profanity
import ny_times
import weather

greetings = ['hi',
             'hello',
             'good morning',
             'good day',
             'good evening',
             'good afternoon',
             'shalom'
             ]

introduction_strings = ["i'm",
                        "name is",
                        "i am",
                        "call me",
                        "calls me",
                        "im",
                        "this is"
                        ]

introduction_reply = ["what's up?",
                      "how are you?",
                      "how are things going?",
                      "hi there!"
                      ]
animation = {'positive_mood': ['inlove', 'laughing', 'dancing', 'excited', 'giggling', 'ok'],
             'negative_mood': ['afraid', 'bored', 'confused', 'crying', 'heartbroke', 'no'],
             'playful_mood': ['money', 'takeoff', 'waiting', 'dog']
             }


def remove_special_chars(message):
    special_chars = [';', ':', '!', "*", ",", ".", "/", "@", "'", "#", "$", "%", "^", "&", "(", ")"]
    clean_message = "".join(char for char in message if char not in special_chars)
    return clean_message


def handle_intro(message):
    cleaned_msg = remove_special_chars(message)
    message_to_list = cleaned_msg.split()
    reply_index = random.randint(0, len(introduction_reply))
    return message_to_list[-1].capitalize() + ". " + introduction_reply[reply_index].capitalize()


def generate_emotion(mood):
    emotion_index = random.randint(0, len(mood))
    emotion = mood[emotion_index]
    return emotion


def generate_joke():
    response = requests.get(
        "https://icanhazdadjoke.com/",
        headers={'Accept': 'application/json'}
    )
    resp_json = response.json()
    random_joke = resp_json["joke"]
    if "money" in random_joke:
        emotion = "money"
    elif "dog" in random_joke:
        emotion = "dog"
    else:
        emotion = "laughing"
    return f"Here's a joke for you: \"{random_joke}\"", emotion


def process_user_msg(message):
    message = message.strip()
    if message in greetings:
        emotion = generate_emotion(animation['positive_mood'])
        return "I'm happy!", emotion
    elif profanity.contains_profanity(message):
        emotion = generate_emotion(animation['negative_mood'])
        return f"Dude, bad words are not allowed!", emotion
    elif message.startswith("weather:"):
        city = message.split(": ")[1]
        return weather.get_weather(city), "takeoff"
    elif 'weather' in message:
        return "Please use the format 'weather: city' " \
                "(For example, weather: Tel Aviv-Yafo) ", 'waiting'
    elif 'joke' in message:
        return generate_joke()
    elif any(substring.lower() in message.lower() for substring in introduction_strings):
        emotion = generate_emotion(positive_mood)
        return "Hello," + handle_intro(message) + "!", emotion
    elif 'news' in message:
        return ny_times.scrape_ny_times(), 'takeoff'
    else:
        return f"Hello {message.capitalize()}! It's nice to meet you!", "excited"