from code.backend.app.db.repository import fetch_restaurant, fetch_parking
#
# print("Hello, how are you?")
# s = input("Enter to continue...")
# print(s)

for a in fetch_parking():
    print(a)
def tokenize(text):
    split = text.split()

