from uuid import uuid4


class ConversationService:

    def __init__(self):
        self.sessions = {}

    def create_session(self):
        session_id = str(uuid4())

        self.sessions[session_id] = []

        return session_id

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_history(self, session_id: str):

        return self.sessions.get(
            session_id,
            []
        )

    def clear_session(self, session_id: str):

        self.sessions.pop(
            session_id,
            None
        )