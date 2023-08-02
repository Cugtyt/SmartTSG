import logging
from Core.StepBase import StepBase


class TSGPipeline:
    def __init__(
            self,
            input_keys: list[str] | None,
            **kwargs) -> None:
        self.steps: list[StepBase] = []
        self.store = dict(kwargs)
        self.input_keys = input_keys

    def add_step(self, step: StepBase):
        self.steps.append(step)
        step.parent_store = self.store

    def run(self):
        for step in self.steps:
            step.build_step_inputs()
            step.run()
