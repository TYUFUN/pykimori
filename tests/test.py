from pykimori.graphql import GraphQLClient
app = GraphQLClient("pykimori")
query = """{
  animes(search: "naruto", limit: 1) {
    id
    name
    russian
    score
  }
}
"""
answer = app.request_name("animes", "svinopas", ["id", "rating", "score", "status", "episodes"])
print(answer.get("id"))
# for list in answer:
#   for key, data in list.items():
#     print(key, data, " is type: ", type(data))
    