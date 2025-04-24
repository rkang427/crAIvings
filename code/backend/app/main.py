from service.utils.basic_tokenizer import Tokenizer
from service.restaurant_service import RestaurantService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://craivings_user:password@localhost/db_craivings')
Session = sessionmaker(bind=engine)

def main():
    print("What would you like to eat?")
    user_input = input()
    #TODO: incorporate Tokenizer feature
    # tokenizer = Tokenizer()
    # tokens = tokenizer.tokenize(user_input)
    # query = " & ".join(tokens)  # concat multiple search fields
    with Session() as session:
        service = RestaurantService(session)
        results = service.search_restaurant(user_input) #should be query
        print("\n".join(results))

if __name__ == "__main__":
    main()
