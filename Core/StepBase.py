from abc import ABC, abstractmethod
import logging


class StepInput:
    def __init__(self, name, value=None, ref=None) -> None:
        self.name: str = name
        self.value: any = value
        self.ref: str = ref


class StepBase(ABC):
    name: str
    parent_store: dict | None
    inputs: list[StepInput] | None
    output_keys: list | None
    outputs: dict | None

    def build_step_inputs(self) -> bool:
        if self.inputs is None:
            return True

        for inp in self.inputs:
            if not inp.value:
                try:
                    inp.value = self.parent_store[inp.ref]
                except KeyError:
                    logging.error(f'Step {self.name} failed to build inputs: {inp.name} can not reference {inp.ref}.')
                    return False
            
            setattr(self, inp.name, inp.value)
    
        return True

    @abstractmethod
    def run(self):
        pass
