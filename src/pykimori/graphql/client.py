import requests
from typing import Any


class GraphQLClient:
    def __init__(self,
        agent: str):
        self.link = "https://shikimori.io/api/graphql"
        self.header = {
            "User-Agent": agent,
            "Content-Type": "application/json"
        }
    def request(self,
    query: str) -> dict[dict, Any]:
        res =requests.post(self.link, json={"query": query}, headers=self.header)
        return res.json()
    def request_id(self,
    id: int,
    *args: str) -> dict[dict, Any]:
        fields = " ".join(args) if args else "id"
        query = """{animes(ids: "%s"){
                %s
                }
            }""" % (id, fields)
        res = requests.post(self.link, json={"query": query}, headers=self.header)
        return res.json()