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
answer = app.request_name("animes", "naruto", 1, "malId", "name", "russian", "japanese", "licenseNameRu")
print(answer)
    