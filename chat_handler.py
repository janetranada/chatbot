from better_profanity import profanity
from datetime import datetime
import random
import requests
import ny_times
import weather


def random_reply(reply_list):
    reply_index = random.randint(0, len(reply_list) - 1)
    return reply_list[reply_index].capitalize()


def remove_special_chars(message):
    special_chars = [';', ':', '!', "*", ",", ".", "/", "@", "'", "#", "$", "%", "^", "&", "(", ")"]
    clean_message = "".join(char for char in message if char not in special_chars)
    return clean_message


# def handle_intro(message):
#     cleaned_msg = remove_special_chars(message)
#     message_to_list = cleaned_msg.split()
#     return message_to_list[-1].capitalize() + ". " + random_reply(introduction_reply)


def greet_user(message):
    cleaned_msg = remove_special_chars(message)
    message_to_list = cleaned_msg.split()
    user_name = message_to_list[-1].capitalize()
    positive_emotion = generate_emotion(animation['positive_mood'])
    return f"Hello {user_name}. {random_reply(introduction_reply)}!", positive_emotion


def generate_emotion(mood):
    emotion_index = random.randint(0, len(mood) - 1)
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


def generate_datetime():
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    current_date = now.strftime('%B %d, %Y')
    return f"The current time is {current_time}. Just a reminder, today is {current_date}."


def handle_profanity():
    emotion = generate_emotion(animation['negative_mood'])
    return f"Dude, bad words are not allowed!", emotion


def process_user_msg(message):
    message = message.strip()
    msg_has_common_greeting = any(substring.lower() in message.lower() for substring in greetings)
    msg_is_profane = profanity.contains_profanity(message)
    msg_in_common_intro = any(substring.lower() in message.lower() for substring in common_introduction_strings)
    msg_is_one_word = len(message.split()) == 1
    msg_in_weather_format = message.startswith("weather:") or message.startswith("Weather:")
    msg_has_optimism = any(substring.lower() in message.lower() for substring in optimistic_strings)
    msg_has_pessimism = any(substring.lower() in message.lower() for substring in pessimistic_strings)
    msg_is_pessimistic = msg_has_pessimism or ('not' in message and msg_has_optimism)

    if msg_has_common_greeting:
        positive_emotion = generate_emotion(animation['positive_mood'])
        return f"{random_reply(greetings_reply)}!", positive_emotion
    elif msg_is_profane:
        return handle_profanity()
    elif msg_in_weather_format:
        city = message.split(": ")[1]
        return weather.get_weather(city), "takeoff"
    elif 'weather' in message:
        return "Please use the format 'weather: city' " \
               "(For example, weather: Tel Aviv-Yafo) ", 'waiting'
    elif 'joke' in message:
        return generate_joke()
    elif 'news' in message:
        return ny_times.scrape_ny_times(), 'takeoff'
    elif 'time' in message:
        return generate_datetime(), 'money'
    elif msg_is_pessimistic:
        return "I'm sorry to hear that.", 'crying'
    elif msg_has_optimism:
        positive_emotion = generate_emotion(animation['positive_mood'])
        return "Awesome!", positive_emotion
    elif msg_in_common_intro or msg_is_one_word:
        return greet_user(message)
    else:
        return f"I'm sorry but I don't know what to say. That message is beyond me..", "confused"


greetings = ['hi',
             'hey',
             'hello',
             'good morning',
             'good day',
             'good evening',
             'good afternoon',
             'shalom'
             ]

greetings_reply = ['hi',
                   'hello',
                   'good day',
                   'hey there',
                   'shalom'
                   ]

optimistic_strings = ['okay',
                      'great',
                      'awesome',
                      'good',
                      'terrific',
                      'fantastic',
                      'wonderful'
                      ]

pessimistic_strings = ['bad',
                       'terrible',
                       'terribly',
                       'ugly',
                       'horrible',
                       'horribly',
                       'awful',
                       'lousy'
                       ]

common_introduction_strings = ["i'm",
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

common_questions = {"how are you": ["I'm doing great!", "Fantastic!", "I'm good! So glad to have someone to chat with."],
                    "where are you from": ['Somewhere...', 'Here, there, everywhere...'],
                    "and you": ["Hmmm... same same", "I'm okay"]
                    }