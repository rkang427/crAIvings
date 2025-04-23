class Restaurant:
    def __init__(self, id, name, address, city, state, postal_code,
                 latitude, longitude, stars, review_count, is_open):
        self.id = id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.stars = stars
        self.review_count = review_count
        self.is_open = is_open

