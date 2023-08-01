import logging
from Core.StepBase import StepBase


class TSGPipeline:
    def __init__(
            self,
            name: str,
            input_keys: list[str] | None,
            **kwargs) -> None:
        self.name = name
        self.steps: list[StepBase] = []
        self.store = dict()
        self.input_keys = input_keys
        if self.input_keys is not None:
            input_store = dict()
            for key in self.input_keys:
                input_store[key] = kwargs[key]
            self.store[self.name] = input_store

    def add_step(self, step: StepBase):
        self.steps.append(step)
        step.parent_store = self.store

    def run(self):
        for step in self.steps:
            if not self.build_step_inputs(step):
                return None

            step.run()

    def build_step_inputs(self, step: StepBase) -> bool:
        if step.inputs is None:
            return True

        for i, input_key in enumerate(step.inputs):
            if '.' in input_key:
                step_name, output_key = input_key.split('.')
                if step_name not in self.store:
                    logging.error(
                        f"Step {step_name} not found in store: {self.store}")
                    logging.error(
                        f"Please check the order of steps in TSG file")
                    return False
                if output_key not in self.store[step_name]:
                    logging.error(
                        f"Output key {output_key} not found in store: {self.store}")
                    logging.error(
                        f"Please check the order of steps in TSG file")
                    return False
                step.inputs[i] = self.store[step_name][output_key]

        return True
