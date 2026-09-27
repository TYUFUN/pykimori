import requests
from typing import Any
from pykimori.exceptions import NoAgentError

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
    query: str) -> dict[str, Any]:
        res =requests.post(self.link, json={"query": query}, headers=self.header)
        return res.json()
    def request_id(self,
    id: int,
    *args: str) -> dict[str, Any]:
        scopes = " ".join(args) if args else "id"
        query = """{animes(ids: "%s"){
                %s
                }
            }""" % (id, scopes)
        res = requests.post(self.link, json={"query": query}, headers=self.header)
        return res.json()