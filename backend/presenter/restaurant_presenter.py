from typing import List, Dict

class RestaurantPresenter:
    def present_search_results(self, restaurants: List) -> List[Dict]:
        formatted_results = []
        for restaurant in restaurants:
            #if restaurant.name not in formatted_results:
            formatted_results.append({
                "name": restaurant.name,
                "address": restaurant.address,
                "stars": restaurant.stars
            })
        return formatted_results