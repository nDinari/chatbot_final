import json
from fuzzywuzzy import fuzz
import random
import re

# Load intents from intents.json file
def load_intents():
    with open('intents.json', 'r') as file:
        return json.load(file)

# Save intents to intents.json file
def save_intents(intents):
    with open('intents.json', 'w') as file:
        json.dump(intents, file, indent=4)

# Function to match user input with intents
def match_intent(user_input, intents):
    max_score = 0
    matched_intent = None
    threshold = 80  # Adjust the threshold as needed

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            score = fuzz.token_sort_ratio(user_input.lower(), pattern.lower())
            if score > max_score and score >= threshold:
                max_score = score
                matched_intent = intent

    return matched_intent

# Load intents from file
intents = load_intents()

# Input loop
while True:
    user_input = input("You: ")

    # Match user input with intents
    matched_intent = match_intent(user_input, intents)

    # If user input matches an intent
    if matched_intent:
        # print(matched_intent['tag'])
        if matched_intent['tag'] == 'goodbye':
            if 'responses' in matched_intent:
                response = random.choice(matched_intent['responses'])
                print("Bot:", response)
            break
        elif 'responses' in matched_intent:
            response = random.choice(matched_intent['responses'])
            print("Bot:", response)
    else:
        # Check if the user input contains name and age information in any order
        name_age_match = re.match(r"(?:myself|i'm) (\w+)?(?:,? of age (\d+))?", user_input, re.IGNORECASE)
        if name_age_match:
            name = name_age_match.group(1)
            age = name_age_match.group(2)
            if name and age:
                print(f"Bot: Nice to meet you, {name}! You are {age} years old.")
            elif name:
                print(f"Bot: Nice to meet you, {name}!")
            elif age:
                print(f"Bot: You are {age} years old.")
        else:
            print('no matching intent is found')
            tag_name = input(f"Bot: Please provide the expected tag: ")
            response = input(f"Bot: Please provide the expected response for the tag '{tag_name}': ")
            # Check if tag name already exists
            tag_exists = False
            for intent in intents['intents']:
                if intent['tag'] == tag_name:
                    intent['patterns'].append(user_input)
                    intent['responses'].append(input("Bot: Please provide the expected response for this utterance: "))
                    tag_exists = True
                    break
                
            # If tag name doesn't exist, add a new intent
            if not tag_exists:
                new_intent = {
                    'tag': tag_name,
                    'patterns': [user_input],
                    'responses': [response]
                }
                intents['intents'].append(new_intent)
                save_intents(intents)
                print("Bot: Utterance added to intents.json file.")