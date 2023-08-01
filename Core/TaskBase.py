import logging
from Core.StepBase import StepBase


class TaskBase(StepBase):
    def __init__(
            self,
            name: str,
            inputs: list[str] | None,
            output_keys: list[str]) -> None:
        self.name = name
        self.inputs = inputs
        self.output_keys = output_keys
        self.parent_store = None

        assert self.output_keys is not None and len(
            self.output_keys) > 0, f"Task {self.name} output keys is None or empty."

    def run(self):
        logging.debug(f"Task {self.name} running.")
        logging.debug(f"inputs: {self.inputs}")

        result = self.work()
        assert result is not None, f"Task {self.name} result is None."

        assert self.output_keys is not None, f"Task {self.name} output keys is None."
        if len(self.output_keys) == 1:
            self.outputs = {self.output_keys[0]: result}
        else:
            self.outputs = {k: v for k, v in zip(self.output_keys, result)}

        assert self.parent_store is not None, f"Task {self.name} parent store is None."
        self.parent_store[self.name] = self.outputs

        logging.debug(f"outputs: {self.outputs}")
        logging.debug(f"Task {self.name} finished.")
        return self.outputs

    def work(self):
        pass
