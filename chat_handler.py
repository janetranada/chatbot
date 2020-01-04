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


def greet_user(message):
    message_to_list = message.split(" ")
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
    negative_emotion = generate_emotion(animation['negative_mood'])
    return f"Dude, bad words are not allowed!", negative_emotion


def handle_optimism():
    reply_options = ["That is awesome!", "That's great!", "Oh... Lovely!", "That's wonderful!"]
    positive_emotion = generate_emotion(animation['positive_mood'])
    random_answer = random.choice(reply_options)
    return random_answer, positive_emotion


def handle_weather_request(message):
    city = message.split(": ")[1]
    return weather.get_weather(city), "takeoff"


def handle_common_question(message):
    global recent_common_question_replies
    positive_emotion = generate_emotion(animation['positive_mood'])
    dict_keys = [key for key in common_questions.keys() if key in message.lower()]
    random_answer = random.choice(common_questions[dict_keys[0]])
    if len(recent_common_question_replies) == 4:
        recent_common_question_replies.pop(0)
    if "how does this work" in dict_keys[0]:
        return common_questions[dict_keys[0]], positive_emotion
    elif random_answer in recent_common_question_replies:
        return handle_common_question(message)
    else:
        recent_common_question_replies.append(random_answer)
        return random_answer, positive_emotion


def handle_common_greeting():
    positive_emotion = generate_emotion(animation['positive_mood'])
    return f"{random_reply(greetings_reply)}!", positive_emotion


def generate_quote():
    global recent_quotes
    with open("quotes.csv", "r") as file:
        lines = file.read().splitlines()
    positive_emotion = generate_emotion(animation['positive_mood'])
    random_quote = random.choice(lines)
    if len(recent_quotes) == 10:
        recent_quotes.pop(0)
    if random_quote not in recent_quotes:
        recent_quotes.append(random_quote)
        return f"Here's a quote for you: '{random_quote}'", positive_emotion
    else:
        return generate_quote()


def process_user_msg(message):
    message = message.strip()
    cleaned_message = remove_special_chars(message)
    not_how_this_work = "how does this work" not in cleaned_message
    not_question_keyword = cleaned_message not in question_keywords
    msg_has_common_greeting = any(substring.lower() in message.lower() for substring in greetings)
    msg_is_common_greeting = msg_has_common_greeting and not_question_keyword and not_how_this_work
    msg_is_profane = profanity.contains_profanity(message)
    msg_in_common_intro = any(substring.lower() in message.lower() for substring in common_introduction_strings)
    msg_possibly_one_word_name = len(cleaned_message.split(" ")) == 1 and cleaned_message not in question_keywords
    msg_in_weather_format = message.startswith("weather:") or message.startswith("Weather:")
    msg_has_optimism = any(substring.lower() in message.lower() for substring in optimistic_strings)
    msg_has_pessimism = any(substring.lower() in message.lower() for substring in pessimistic_strings)
    msg_is_pessimistic = msg_has_pessimism or ('not' in message and msg_has_optimism)
    msg_in_common_questions = any(key in message for key in common_questions.keys())

    if msg_is_common_greeting:
        return handle_common_greeting()
    elif msg_is_profane:
        return handle_profanity()
    elif msg_in_weather_format:
        return handle_weather_request(message)
    elif "weather" in message:
        return "Please use the format 'weather: city' " \
               "(For example, weather: Tel Aviv-Yafo) ", 'waiting'
    elif "joke" in message:
        return generate_joke()
    elif "news" in message or "headline" in message:
        return ny_times.scrape_ny_times(), 'takeoff'
    elif "time" in message:
        return generate_datetime(), 'money'
    elif "quote" in message:
        return generate_quote()
    elif msg_in_common_questions:
        return handle_common_question(message)
    elif "emergency" in message or "sos" in message:
        return f"Is something wrong? I only know emergency numbers in Israel: " \
               f"100 is police, 101 is ambulance, 102 is fire.", "afraid"
    elif 'thank' in message:
        return "You're welcome!", "inlove"
    elif msg_is_pessimistic:
        return "I'm sorry to hear that.", 'crying'
    elif msg_has_optimism:
        return handle_optimism()
    elif "?" in message:
        return f"I'm sorry but I don't understand the question...", "confused"
    elif msg_in_common_intro or msg_possibly_one_word_name:
        return greet_user(cleaned_message)
    else:
        return f"I'm sorry but I don't know what to say. That message is beyond me... You can ask me the weather, " \
               f"the time, and the top news headline. I can also give you a joke or a quote.", "confused"


recent_quotes = []
recent_common_question_replies = []

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
                   'shalom',
                   'hello dear'
                   ]

optimistic_strings = ['okay',
                      'great',
                      'awesome',
                      'good',
                      'terrific',
                      'fantastic',
                      'wonderful',
                      'well'
                      ]

pessimistic_strings = ['bad',
                       'terrible',
                       'terribly',
                       'ugly',
                       'horrible',
                       'horribly',
                       'awful',
                       'lousy',
                       'not much',
                       ]

common_introduction_strings = ["i'm",
                               "name is",
                               "i am",
                               "call me",
                               "calls me",
                               "im",
                               "this is",
                               "called"
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

common_questions = {"how are you": ["I'm doing great!",
                                    "I feel fantastic today!",
                                    "I feel good! So glad to have someone to chat with.",
                                    "Never been better!"],
                    "where are you from": ['Somewhere only we know.',
                                           'Here. There. Everywhere.',
                                           "Somewhere over the rainbow.",
                                           "I don't know, actually."],
                    "and you": ["Hmmm... same same",
                                "I'm okay",
                                "The same.",
                                "The usual."],
                    "how old are you": ["I don't keep track.",
                                        "Hey! It's not cool to ask that.",
                                        "I dunno",
                                        "I don't disclose that",
                                        "Old enough."],
                    "your age": ["I don't keep track.",
                                 "Hey! It's not cool to ask that.",
                                 "I dunno",
                                 "I don't disclose that.",
                                 "Old enough."],
                    "who made you": ["Some girl named Janet.",
                                     "Janet TRIED to make me smart.",
                                     "I'm self-made... joke!",
                                     "My creator."],
                    "do you like": ["Hmmm.. I have to think about that.",
                                    "I have a neutral stand on that.",
                                    "Next question, please.",
                                    "I wish I could tell you, but I'm not allowed to."],
                    "how does this work": ["You can ask me the weather, the time, and the top "
                                           "news headline. I can also give you a joke or a quote. "
                                           "I can also deal with some basic questions."],
                    "what is your name": ["Dude, I told you. My name is Boto.",
                                         "I am Boto",
                                         "I'm called Boto",
                                         "Boto is my name"],
                    "are you a robot": ["Of course, I am!",
                                        "Yup! You got me :)",
                                        "100% YES!",
                                        "Absolutely! Made to take your boredom away."]
                    }

question_keywords = ["what", "when", "where", "how", "why", "which"]