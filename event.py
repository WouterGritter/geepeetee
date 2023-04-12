from abc import ABC, abstractmethod


class Event(ABC):
    @abstractmethod
    def stringify(self) -> str:
        pass

    def __str__(self):
        return self.stringify()


class SystemEvent(Event):
    def __init__(self, message: str):
        self.message = message

    def stringify(self) -> str:
        return f'[SystemEvent]\n' \
               f'SYSTEM: {self.message}\n'


class GPTEvent(Event):
    def __init__(self, thought: str, reasoning: str, plan: str, speak: str):
        self.thought = thought
        self.reasoning = reasoning
        self.plan = plan
        self.speak = speak

    def stringify(self) -> str:
        return f'[GPTEvent]\n' \
               f'THOUGHT: {self.thought}\n' \
               f'REASONING: {self.reasoning}\n' \
               f'PLAN: {self.plan}\n' \
               f'SPEAK: {self.speak}\n'
