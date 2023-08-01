from abc import ABCMeta, abstractmethod


class StepBase:
    __metaclass__ = ABCMeta

    name: str
    parent_store: dict | None
    inputs: list | None
    output_keys: list | None
    outputs: dict | None

    @abstractmethod
    def run(self):
        pass
