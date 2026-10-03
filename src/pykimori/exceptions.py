class NoAgentError(Exception):
    def __init__(self):
        self.status_code = 400
        super().__init__("Missing required argument agent")
        
class GraphQLError(Exception):
    def __init__(self, errors: list):
        self.errors = errors
        message = errors[0].get("message", "Unknown GraphQL error") if errors else "GraphQL Error"
        super().__init__(message)
        
class NoDataFoundError(Exception):
    def __init__(self, category: str, scope: str):
        super().__init__(f"No data found for {category} with scope {scope}.")