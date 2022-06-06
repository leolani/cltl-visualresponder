import abc


class VisualResponder(abc.ABC):
    def respond(self, statement: str) -> str:
        raise NotImplementedError("")
