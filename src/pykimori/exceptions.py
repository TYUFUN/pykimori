class NoAgentError(Exception):
    def __init__(self):
        self.status_code = 400
        super().__init__("Missing required argument agent")
        