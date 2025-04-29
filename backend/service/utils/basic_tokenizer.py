from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, create_engine, func
import spacy
# class Tokenizer:
#
#     def __init__(self):
#         pass
#     def tokenize(self, text):
#         split = text.lower().split()
#         return split
#
# temp = Tokenizer()
# a = Tokenizer.tokenize(temp, "hamburger")
# print(a)
nlp = spacy.load('en_core_web_md')
print(nlp.vocab.vectors.shape)