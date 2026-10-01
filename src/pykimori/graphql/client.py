import requests
from requests import Response
from typing import Sequence
from pykimori.exceptions import NoAgentError
from pykimori.types import Anime

class GraphQLClient:
    def __init__(self,
        agent: str):
        self.link = "https://shikimori.io/api/graphql"
        if not agent:
            raise NoAgentError
        self.header = {
            "User-Agent": agent,
            "Content-Type": "application/json"
        }
    def request(self,
    query: str) -> Anime:
        res =requests.post(self.link, json={"query": query}, headers=self.header)
        return res.json()
    def request_id(self,
    category: str,
    id: int,
    args: Sequence[str]) -> Anime:
        scopes = " ".join(args) if args else "id"
        query = """{%s(ids: "%s"){
                %s
                }
            }""" % (category, id, scopes)
        res = requests.post(self.link, json={"query": query}, headers=self.header)
        return res.json()
    def request_name(self,
    category: str,
    name: str,
    args: Sequence[str], # sequence = any data with index and len() like list, tuple or set
    limit: int = 1) -> list[Anime]:
        scopes = " ".join(args) if args else "name"
        query = """{%s(search: "%s", limit:%d){
            %s
            }
        }""" % (category, name, limit, scopes)
        res = requests.post(self.link, json={"query": query}, headers=self.header)
        return res.json().get("data", {}).get(category, [])

    def request_raw(self, 
    query: str) -> Response:
        return requests.post(self.link, json={"query": query}, headers=self.header)
    
#unpack res more to return only dict (look requesr_name) and write GraphqlEror and catch if api returns error so user dont get empty list