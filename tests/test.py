from pykimori.graphql import client
app = client.GraphQLClient("pykimori")
query = """{
  animes(search: "naruto", limit: 1) {
    id
    name
    russian
    score
  }
}
"""
answer = app.request_id(20, "id", "name", "russian")
print(answer)
    