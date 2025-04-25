from typing import List, Dict

class RestaurantPresenter:
    def present_search_results(self, restaurants: List) -> List[Dict]:
        formatted_results = []
        for restaurant in restaurants:
            formatted_results.append({
                "name": restaurant.name
            })
        return formatted_results