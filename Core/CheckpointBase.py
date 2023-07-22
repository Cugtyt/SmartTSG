import logging
from Core.StepBase import StepBase


class CheckpointBase(StepBase):
    def __init__(
            self,
            name: str,
            inputs: list[str],
            rules: list[str]) -> None:
        self.name = name
        self.inputs = inputs
        self.rules = rules
        self.parent_store = None

        assert self.inputs is not None, f"Checkpoint {self.name} inputs is None."
        assert self.rules is not None and len(self.rules) > 0, f"Checkpoint {self.name} rules is None or empty."

    def run(self) -> bool:
        logging.info('=' * 20 + f"Checkpoint {self.name} running." + '=' * 20)

        context = self.build_context()
        logging.info(f"context:\n{context}")
        rules = '\n'.join(self.rules)
        logging.info(f"Rules:\n{rules}")
        if not self.check():
            logging.error(f"Checkpoint {self.name} failed.")
            raise Exception(f"Checkpoint {self.name} failed.")
        

        logging.info('=' * 20 + f"Checkpoint {self.name} finished." + '=' * 20)
        return True

    def build_context(self) -> str:
        return ''
    
    def check(self) -> bool:
        logging.info(f"Checkpoint {self.name} passed.")
        return True