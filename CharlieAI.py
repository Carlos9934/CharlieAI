import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random
import datetime
import json
import os
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

class CharlieAI:
    def __init__(self):
        self.patterns = {
            "greeting": {
                "patterns": ["hello", "hi", "hey", "greetings"],
                "responses": ["Hello! I'm CharlieAI, how can I help you?", "Hi there! CharlieAI at your service!", "Hey! I'm CharlieAI, nice to meet you!"]
            },
            "farewell": {
                "patterns": ["bye", "goodbye", "see you", "farewell"],
                "responses": ["Goodbye! Have a great day!", "See you later!", "Take care!"]
            },
            "thanks": {
                "patterns": ["thank", "thanks", "appreciate"],
                "responses": ["You're welcome!", "My pleasure!", "Happy to help!"]
            },
            "time": {
                "patterns": ["time", "hour", "clock"],
                "responses": ["The current time is: {}"]
            },
            "name": {
                "patterns": ["your name", "who are you", "what are you"],
                "responses": ["I'm CharlieAI, your friendly chatbot!", "You can call me CharlieAI!"]
            }
        }
        self.conversation_history = []
        self.stop_words = set(stopwords.words('english'))

    def solve_math(self, expression):
        try:
            # Remove any non-math characters and spaces
            expression = re.sub(r'[^0-9+\-*/().]', '', expression)
            # Evaluate the expression safely
            result = eval(expression)
            return f"The result is: {result}"
        except:
            return "I couldn't solve that math problem. Please make sure it's a valid expression."

    def preprocess_text(self, text):
        # Tokenize and remove stop words
        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word not in self.stop_words]
        return tokens

    def get_response(self, user_input):
        # Save conversation
        self.conversation_history.append({"user": user_input, "timestamp": str(datetime.datetime.now())})
        
        # Check if input contains math operations
        if any(op in user_input for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
            return self.solve_math(user_input)
        
        # Preprocess input
        tokens = self.preprocess_text(user_input)
        
        # Check for matches
        for intent, data in self.patterns.items():
            if any(pattern in user_input.lower() for pattern in data["patterns"]):
                response = random.choice(data["responses"])
                
                # Special handling for time
                if intent == "time":
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    response = response.format(current_time)
                
                return response
        
        return "I'm not sure how to respond to that. Could you try asking something else?"

    def save_conversation(self):
        # Save conversation history to a file
        with open('conversation_history.json', 'w') as f:
            json.dump(self.conversation_history, f, indent=4)

def main():
    print("CharlieAI Chatbot (type 'quit' to exit)")
    print("----------------------------------------")
    print("I can help you with basic math operations!")
    print("Examples: '2 + 2', '10 * 5', '100 / 4'")
    print("----------------------------------------")
    
    ai = CharlieAI()
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            print("CharlieAI: Goodbye! Saving our conversation...")
            ai.save_conversation()
            break
            
        response = ai.get_response(user_input)
        print("CharlieAI:", response)

if __name__ == "__main__":
    main()