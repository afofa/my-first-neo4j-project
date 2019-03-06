from py2neo import Graph, Node, Relationship, NodeMatcher
from typing import Union
from utils import load_json

def create_graph(   bolt:Union[bool, None]=None, 
                    secure:bool=False, 
                    host:str="localhost", 
                    http_port:int=7473, 
                    https_port:int=7474, 
                    bolt_port:int=7687, 
                    user:str="neo4j", 
                    password:str="neo4j"
                ) -> Graph:

    graph = Graph(bolt=bolt, secure=secure, host=host, http_port=http_port, https_port=https_port, bolt_port=bolt_port, user=user, password=password)
    return graph


def create_nodes(graph:Graph, tbmm_json):
    city_json = tbmm_json['cities']
    mp_json = tbmm_json['mps']
    party_json = tbmm_json['parties']

    # create city nodes
    for city in city_json:
        city_node = Node("City", **city)
        graph.create(city_node)

    # create mp nodes
    for mp in mp_json:
        mp_node = Node("MP", **mp)
        graph.create(mp_node)

    # create party nodes
    for party in party_json:
        party_node = Node("Party", **party)
        graph.create(party_node)


def create_relations(graph:Graph):
    # create IS_MEMBER_OF and IS_FROM relationships

    matcher = NodeMatcher(graph)
    mp_matched = matcher.match("MP")

    for mp in mp_matched:
        # IS_MEMBER_OF
        party_matched = matcher.match("Party", name=mp["party"])
        party = party_matched.first()
        rel_party = Relationship(mp, "IS_MEMBER_OF", party)
        graph.create(rel_party)
        # IS_FROM
        city_matched = matcher.match("City", name=mp["city"])
        city = city_matched.first()
        rel_city = Relationship(mp, "IS_MP_FROM", city)
        graph.create(rel_city)


if __name__ == '__main__':
    
    my_neo4j_password = "" # set this to your password
    tbmm_json = load_json("tbmm.json")
    graph = create_graph(password=my_neo4j_password)
    create_nodes(graph, tbmm_json)
    create_relations(graph)
    