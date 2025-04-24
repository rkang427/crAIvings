from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, create_engine, func
class Tokenizer:
    def __init__(self):
        pass
    def tokenize(self, text):
        split = text.lower().split()
        return split


def __main__():
    print("Hello there! What would you like to eat?")
    user_input = input()
    token = Tokenizer()
    print(search_restaurant(user_input))
    #print(token.tokenize(user_input))
if __name__ == "__main__":
    __main__()
