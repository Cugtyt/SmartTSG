import logging

from Core.CheckpointBase import CheckpointBase


class HelloBasicCheckpoint(CheckpointBase):
    def check(self) -> bool:
        assert self.inputs is not None

        context = '\n'.join(self.inputs[0])
        logging.info(f"context:\n{context}")
        result = 'world' in context and 'SmartTSG' in context
        logging.info(f"Result:\n{result}")

        return result
