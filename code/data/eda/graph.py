import pandas as pd
import numpy as np

import http.client
import json
import csv
import requests
class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]

    def add_node(self, id: str, name: str) -> None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        node = (str(id), name)
        check = [x[0] for x in self.nodes]
        if str(id) not in check:
            self.nodes.append(node)

            # these comments are for debugging purposes
            # print(f"node {node} added.")
        else:
            # print(f"node {node} already exists.")
            return

    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        if str(source) == str(target):
            return
        if (str(source), str(target)) not in self.edges and (str(target), str(source)) not in self.edges:
            check = [x[0] for x in self.nodes]
            if str(target) not in check:
                print(f"oh no target {target} not in check")
                return
            if str(source) not in check:
                print(check)
                print(f"oh no source {source} not in check")
                return
            self.edges.append((str(source), str(target)))
            # print(f"edge ({source}, {target}) added.")
        else:
            # print(f"edge ({source}, {target}) already exists.")
            return

    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return len(self.nodes)

    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return len(self.edges)

    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        dct = {}
        for a in self.nodes:
            dct[a[0]] = len(  # second element in tuple is target therefore the node
                list(filter(lambda x: x[1] == a[0], self.edges)))
        dct_lst = sorted(dct.items(), key=lambda a: a[1], reverse=True)
        dct = dict(dct)
        tmp = dct_lst[0][1]
        kv = [k for k, value in dct_lst if value == tmp]
        return {k: v + 1 for k, v in dct.items() if k in kv}

    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)

    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)

    # Do not modify
    def write_edges_file(self, path="edges.csv") -> None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")

    # Do not modify
    def write_nodes_file(self, path="nodes.csv") -> None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")


class TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_movie_cast(self, movie_id: str, limit: int = None, exclude_ids: list[int] = None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param string movie_id: a movie_id
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :param integer limit: maximum number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after excluding, there are fewer cast members than the specified limit, then return the remaining members (excluding the ones whose order values are outside the limit range).
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            If after excluding, the limit is not specified, then return all remaining cast members."
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ... ]
                Note that this is an example of the structure of the list and some of the fields returned by the API.
                The result of the API call will include many more fields for each cast member.
        """
        BASE_URL = 'https://api.themoviedb.org/3'
        url = f"{BASE_URL}/movie/{movie_id}/credits?language=en-US"  # the text f allows me to embed variables into the string
        params = {'api_key': self.api_key,
                  'language': 'en-US'}
        response = requests.get(url, params=params)  # an HTTPS GET request
        if response.status_code == 200:  # 200 is successful
            data = response.json()  # json is usually the format for api's parsed
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return NotImplemented
        cast = sorted(data['cast'], key=lambda x: x['order'])
        lst = []
        for a in cast[:limit]:
            lst.append(a)
        if exclude_ids:
            for a in lst:
                if a['id'] in exclude_ids:
                    lst.remove(a)
        return lst

    def get_movie_credits_for_person(self, person_id: str, start_date: str = None, end_date: str = None) -> list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param start_date: optional parameter to return the movie credit if the release date >= the specified date
            dates should be formatted like 'YYYY-MM-DD'
            e.g., if the start_date is '2024-01-01', then only return credits with a release_date on or after '2024-01-01'
        :param end_date: optional parameter to return the movie credit if the release date <= the specified date
            dates should be formatted like 'YYYY-MM-DD'
            e.g., if the end_date is '2024-01-01', then only return credits with a release_date on or before '2024-01-01'
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'release_date': '2024-01-01' # the string value of the release_date value for the credit}, ... ]

        IMPORTANT: You should format your dates like 'YYYY-MM-DD' e.g. '2024-01-29'.  You can assume the API will
            format them in the same way. You can compare these as strings without doing any conversion.
        """
        BASE_URL = 'https://api.themoviedb.org/3'
        url = f"{BASE_URL}/person/{person_id}/movie_credits?language=en-US"  # the text f allows me to embed variables into the string
        params = {'api_key': self.api_key,
                  'language': 'en-US'}
        response = requests.get(url, params=params)  # an HTTPS GET request
        data = None
        if response.status_code == 200:
            data = response.json()
        cast = list(filter(lambda x: 'release_date' in x
                                     and end_date >= x['release_date'] >= start_date, data['cast']))
        lst = []
        for a in cast:
            # tmp = {'id': a['id'], 'title': a['title'], 'release_date': a['release_date']}
            lst.append(a)
        return lst


#############################################################################################################################
#
# BUILDING YOUR GRAPH
#
# Working with the API:  See use of http.request: https://docs.python.org/3/library/http.client.html#examples
#
# Using TMDb's API, build a co-actor network for the actor's/actress' movies released in 1999.
# In this graph, each node represents an actor
# An edge between any two nodes indicates that the two actors/actresses acted in a movie together in 1999.
# i.e., they share a movie credit.
# e.g., An edge between Samuel L. Jackson and Robert Downey Jr. indicates that they have acted in one
# or more movies together in 1999.
#
# For this assignment, we are interested in a co-actor network of highly rated movies; specifically,
# we only want the first 5 co-actors in each movie credit with a release date in 1999.
# Build your co-actor graph on the actor 'Laurence Fishburne' w/ person_id 2975.
#
# You will need to add extra functions or code to accomplish this.  We will not directly call or explicitly grade your
# algorithm. We will instead measure the correctness of your output by evaluating the data in your nodes.csv and edges.csv files.
#
# GRAPH SIZE
# Since the TMDB API is a live database, the number of nodes / edges in the final graph will vary slightly depending on when
# you execute your graph building code. We take this into account by rebuilding the solution graph every few days and
# updating the auto-grader.  We compare your graph to our solution with a margin of +/- 200 for nodes and +/- 300 for edges.
#
# e.g., if the current solution contains 507 nodes then the min/max range is 307-707.
# The same method is used to calculate the edges with the exception of using the aforementioned edge margin.
# ----------------------------------------------------------------------------------------------------------------------
# BEGIN BUILD CO-ACTOR NETWORK
#
# INITIALIZE GRAPH
#   Initialize a Graph object with a single node representing Laurence Fishburne
#
# BEGIN BUILD BASE GRAPH:
#   Find all of Laurence Fishburne's movie credits that have a release date in 1999.
#   FOR each movie credit:
#   |   get the movie cast members having an 'order' value between 0-4 (these are the co-actors)
#   |
#   |   FOR each movie cast member:
#   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
#   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actor) node
#   |   |   and each new node (co-actor/co-actress)
#   |   END FOR
#   END FOR
# END BUILD BASE GRAPH
#
#
# BEGIN LOOP - DO 2 TIMES:
#   IF first iteration of loop:
#   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
#   ELSE
#   |    nodes = The nodes added in the previous iteration:
#   ENDIF
#
#   FOR each node in nodes:
#   |  get the movie credits for the actor that have a release date in 1999.
#   |
#   |   FOR each movie credit:
#   |   |   try to get the 5 movie cast members having an 'order' value between 0-4
#   |   |
#   |   |   FOR each movie cast member:
#   |   |   |   IF the node doesn't already exist:
#   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
#   |   |   |   ENDIF
#   |   |   |
#   |   |   |   IF the edge does not exist:
#   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
#   |   |   |   ENDIF
#   |   |   END FOR
#   |   END FOR
#   END FOR
# END LOOP
#
# Your graph should not have any duplicate edges or nodes
# Write out your finished graph as a nodes file and an edges file using:
#   graph.write_edges_file()
#   graph.write_nodes_file()
#
# END BUILD CO-ACTOR NETWORK
# ----------------------------------------------------------------------------------------------------------------------

# Exception handling and best practices
# - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
# - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
# - Some movie_credits do not return cast data. Handle this situation by skipping these instances.
# - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
#   can occasionally result in timeout errors. If you continue to experience 'ConnectionRefusedError : [Errno 61] Connection refused',
#   - wait a while and then try again.  It may be necessary to insert periodic sleeps when you are building your graph.


def return_name() -> str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    return 'rkang33'


# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.

if __name__ == "__main__":
    if __name__ == "__main__":
        # BEGIN BUILD CO-ACTOR NETWORK
        #
        # INITIALIZE GRAPH
        #   Initialize a Graph object with a single node representing Laurence Fishburne
        #
        graph = Graph()
        API_KEY = 'a9f01558bfe24937338ae7f587876bbb'
        graph.add_node(id='2975', name='Laurence Fishburne')
        tmdb_api_utils = TMDBAPIUtils(api_key=API_KEY)

        # BEGIN BUILD BASE GRAPH:
        #   Find all of Laurence Fishburne's movie credits that have a release date in 1999.
        #   FOR each movie credit:
        #   |   get the movie cast members having an 'order' value between 0-4 (these are the co-actors)
        #   |
        base = tmdb_api_utils.get_movie_credits_for_person(person_id='2975', start_date='1999-01-01',
                                                           end_date='1999-12-31')

        #
        ne = set()
        nn = set()

        #   FOR each movie credit:
        for a in base:
            #   |   get the movie cast members having an 'order' value between 0-4 (these are the co-actors)
            list_of_cast_members = tmdb_api_utils.get_movie_cast(movie_id=a['id'], limit=5)
            for actor in list_of_cast_members:
                actor_id = str(actor['id'])
                actor_name = actor['name'].replace(',', '')

                #   |   FOR each movie cast member:
                #   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
                #   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actor) node
                #   |   |   and each new node (co-actor/co-actress)

                if actor_id not in nn:
                    graph.add_node(id=actor_id, name=actor_name)
                    nn.add(actor_id)

                # Add edge between Laurence Fishburne and co-actor if it doesn't exist
                if (actor_id, '2975') not in ne and ('2975', actor_id) not in ne:
                    graph.add_edge(source='2975', target=actor_id)
                    ne.add(('2975', actor_id))

        # END BUILD BASE GRAPH
        # BEGIN LOOP - DO 2 TIMES:
        #   IF first iteration of loop:
        #   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
        #   ELSE
        #   |    nodes = The nodes added in the previous iteration:
        #   ENDIF
        for yeehaw in range(2):
            graph_nodes = list(new_nodes)

            for node_id in graph_nodes:
                #   |  get the movie credits for the actor that have a release date in 1999.
                credits = tmdb_api_utils.get_movie_credits_for_person(person_id=node_id, start_date='1999-01-01',
                                                                      end_date='1999-12-31')
                #   FOR each node in nodes:
                #   |  get the movie credits for the actor that have a release date in 1999.
                #   |
                #   |   FOR each movie credit:
                #   |   |   try to get the 5 movie cast members having an 'order' value between 0-4
                #   |   |
                #   |   |   FOR each movie cast member:
                #   |   |   |   IF the node doesn't already exist:
                #   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
                #   |   |   |   ENDIF
                #   |   |   |
                #   |   |   |   IF the edge does not exist:
                #   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)

                for c in credits:
                    list_of_cast_members = tmdb_api_utils.get_movie_cast(movie_id=c['id'], limit=5)
                    for actor in list_of_cast_members:
                        actor_id = str(actor['id'])
                        actor_name = actor['name'].replace(',', '')

                        if actor_id not in nn:
                            graph.add_node(id=actor_id, name=actor_name)
                            nn.add(actor_id)

                        if (node_id, actor_id) not in ne and (actor_id, node_id) not in ne:
                            graph.add_edge(source=node_id, target=actor_id)
                            ne.add((node_id, actor_id))

        # END LOOP

        # Write the final graph data to CSV
        graph.write_edges_file()
        graph.write_nodes_file()

    # If you have already built & written out your graph, you could read in your nodes & edges files
    # to perform testing on your graph.
    graph = Graph(with_edges_file="edges.csv", with_nodes_file="nodes.csv")
