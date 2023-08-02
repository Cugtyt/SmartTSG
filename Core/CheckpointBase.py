import logging

from Core.GPTCall import ai_check, FAIL, PASS
from Core.StepBase import StepBase, StepInput


class CheckpointBase(StepBase):
    def __init__(
            self,
            name: str,
            inputs: list[StepInput],
            rules: list[str]) -> None:
        self.name = name
        self.inputs = inputs
        self.rules = rules
        self.parent_store = None

        assert self.inputs is not None, f"Checkpoint {self.name} inputs is None."

    def run(self) -> bool:
        logging.info('=' * 20 + f"Checkpoint {self.name} running." + '=' * 20)

        if not self.check():
            logging.error(f"Checkpoint {self.name} failed.")
            raise Exception(f"Checkpoint {self.name} failed.")

        logging.info('=' * 20 + f"Checkpoint {self.name} finished." + '=' * 20)
        return True

    def build_context(self) -> str:
        return ''

    def check(self) -> bool:
        context = self.build_context()
        logging.info(f"context:\n{context}")
        rules = '\n'.join(self.rules)
        logging.info(f"Rules:\n{rules}")

        result = ai_check(context, rules)

        logging.debug(f"Result:\n{result}")

        if result.strip().startswith(FAIL):
            logging.error(f"Checkpoint {self.name} failed.")
            report = result[result.index(FAIL) + len(FAIL):].strip()
            logging.error(f"Report:\n{report}")
            return False
        elif result.strip().startswith(PASS):
            logging.info(f"Checkpoint {self.name} passed.")
            report = result[result.index(PASS) + len(PASS):].strip()
            logging.info(f"Report:\n{report}")
            return True

        return False
