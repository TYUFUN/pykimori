from unittest.mock import MagicMock, patch
import pytest
import requests

from pykimori.graphql import GraphQLClient
from pykimori.exceptions import GraphQLError, NoAgentError
from pykimori.types import Anime


@pytest.fixture
def client() -> GraphQLClient:
    """Fixture providing a GraphQLClient instance with a test user agent."""
    return GraphQLClient(agent="test-agent")


class TestGraphQLClientInit:
    def test_init_success(self, client: GraphQLClient):
        """Test successful initialization with valid agent."""
        assert client.link == "https://shikimori.io/api/graphql"
        assert client.header == {
            "User-Agent": "test-agent",
            "Content-Type": "application/json"
        }

    def test_init_empty_agent_raises_no_agent_error(self):
        """Test initialization with empty agent raises NoAgentError."""
        with pytest.raises(NoAgentError) as exc_info:
            GraphQLClient(agent="")
        assert exc_info.value.status_code == 400
        assert "Missing required argument agent" in str(exc_info.value)

    def test_init_none_agent_raises_no_agent_error(self):
        """Test initialization with None agent raises NoAgentError."""
        with pytest.raises(NoAgentError):
            GraphQLClient(agent=None)  # type: ignore[arg-type]


class TestGraphQLClientRequest:
    def test_request_success(self, client: GraphQLClient):
        """Test request sends correct payload and returns JSON response."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.json.return_value = {"data": {"animes": [{"id": "1"}]}}

        query = "{ animes(limit: 1) { id } }"
        with patch("requests.post", return_value=mock_response) as mock_post:
            result = client.request(query)

            mock_post.assert_called_once_with(
                client.link,
                json={"query": query},
                headers=client.header
            )
            assert result == {"data": {"animes": [{"id": "1"}]}}

    def test_request_network_error(self, client: GraphQLClient):
        """Test request propagates network exceptions."""
        with patch("requests.post", side_effect=requests.ConnectionError("Network down")):
            with pytest.raises(requests.ConnectionError):
                client.request("{ animes { id } }")


class TestGraphQLClientRequestId:
    def test_request_id_with_args(self, client: GraphQLClient):
        """Test request_id formats query with given field scopes."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.json.return_value = {"data": {"animes": [{"id": "21", "name": "One Piece"}]}}

        with patch("requests.post", return_value=mock_response) as mock_post:
            result = client.request_id(
                category="animes",
                id=21,
                args=["id", "name", "score"]
            )

            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args.kwargs
            sent_query = call_kwargs["json"]["query"]

            assert 'animes(ids: "21")' in sent_query
            assert "id name score" in sent_query
            assert call_kwargs["headers"] == client.header
            assert result == {"data": {"animes": [{"id": "21", "name": "One Piece"}]}}

    def test_request_id_empty_args_defaults_to_id(self, client: GraphQLClient):
        """Test request_id defaults scope to 'id' when args sequence is empty."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.json.return_value = {"data": {"animes": [{"id": "5"}]}}

        with patch("requests.post", return_value=mock_response) as mock_post:
            client.request_id(category="animes", id=5, args=[])

            call_kwargs = mock_post.call_args.kwargs
            sent_query = call_kwargs["json"]["query"]
            assert "id" in sent_query


class TestGraphQLClientRequestName:
    def test_request_name_success_returns_item(self, client: GraphQLClient):
        """Test request_name returns the first matched item dictionary."""
        anime_data: Anime = {
            "id": "20",
            "name": "Naruto",
            "score": 7.9,
            "status": "released"
        }
        mock_response = MagicMock(spec=requests.Response)
        mock_response.json.return_value = {
            "data": {
                "animes": [anime_data]
            }
        }

        with patch("requests.post", return_value=mock_response) as mock_post:
            result = client.request_name(
                category="animes",
                name="Naruto",
                args=["id", "name", "score", "status"],
                limit=1
            )

            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args.kwargs
            sent_query = call_kwargs["json"]["query"]

            assert 'animes(search: "Naruto", limit:1)' in sent_query
            assert "id name score status" in sent_query
            assert result == anime_data

    def test_request_name_empty_args_defaults_to_name(self, client: GraphQLClient):
        """Test request_name defaults scope to 'name' when args is empty."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.json.return_value = {
            "data": {
                "animes": [{"name": "Bleach"}]
            }
        }

        with patch("requests.post", return_value=mock_response) as mock_post:
            result = client.request_name(
                category="animes",
                name="Bleach",
                args=[]
            )

            call_kwargs = mock_post.call_args.kwargs
            sent_query = call_kwargs["json"]["query"]

            assert 'animes(search: "Bleach", limit:1)' in sent_query
            assert "name" in sent_query
            assert result == {"name": "Bleach"}

    def test_request_name_custom_limit(self, client: GraphQLClient):
        """Test request_name passes custom limit parameter in query."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.json.return_value = {
            "data": {
                "mangas": [{"id": "100"}]
            }
        }

        with patch("requests.post", return_value=mock_response) as mock_post:
            client.request_name(
                category="mangas",
                name="Berserk",
                args=["id"],
                limit=5
            )

            sent_query = mock_post.call_args.kwargs["json"]["query"]
            assert 'mangas(search: "Berserk", limit:5)' in sent_query

    def test_request_name_no_data_returns_empty_dict(self, client: GraphQLClient):
        """Test request_name returns empty dict when no results found in list."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.json.return_value = {
            "data": {
                "animes": []
            }
        }

        with patch("requests.post", return_value=mock_response):
            result = client.request_name(
                category="animes",
                name="nonexistent_title",
                args=["id", "name"]
            )
            assert result == {}

    def test_request_name_missing_category_returns_empty_dict(self, client: GraphQLClient):
        """Test request_name returns empty dict when data does not contain category."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.json.return_value = {"data": {}}

        with patch("requests.post", return_value=mock_response):
            result = client.request_name(
                category="animes",
                name="Naruto",
                args=["id"]
            )
            assert result == {}

    def test_request_name_raises_graphql_error(self, client: GraphQLClient):
        """Test request_name raises GraphQLError when API response contains errors."""
        mock_response = MagicMock(spec=requests.Response)
        errors = [
            {"message": "Field 'invalid_field' does not exist on type 'Anime'"}
        ]
        mock_response.json.return_value = {"errors": errors}

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(GraphQLError) as exc_info:
                client.request_name(
                    category="animes",
                    name="Naruto",
                    args=["invalid_field"]
                )

            assert exc_info.value.errors == errors
            assert "Field 'invalid_field' does not exist" in str(exc_info.value)

    def test_request_name_raises_graphql_error_empty_errors_list(self, client: GraphQLClient):
        """Test request_name raises GraphQLError with fallback message when errors list is empty."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.json.return_value = {"errors": []}

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(GraphQLError) as exc_info:
                client.request_name(
                    category="animes",
                    name="Naruto",
                    args=["id"]
                )

            assert str(exc_info.value) == "GraphQL Error"


class TestGraphQLClientRequestRaw:
    def test_request_raw_returns_response_object(self, client: GraphQLClient):
        """Test request_raw returns the raw requests.Response object."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = '{"data": {}}'

        query = "{ test }"
        with patch("requests.post", return_value=mock_response) as mock_post:
            response = client.request_raw(query)

            mock_post.assert_called_once_with(
                client.link,
                json={"query": query},
                headers=client.header
            )
            assert response is mock_response
            assert response.status_code == 200
            assert response.text == '{"data": {}}'
            # Verify json() was not called by request_raw
            mock_response.json.assert_not_called()

