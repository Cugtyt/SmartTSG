from abc import ABC, abstractmethod


class StepBase(ABC):
    name: str
    parent_store: dict | None
    inputs: list | None
    output_keys: list | None
    outputs: dict | None

    @abstractmethod
    def run(self):
        pass
