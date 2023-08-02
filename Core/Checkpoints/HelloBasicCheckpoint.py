import logging

from Core.CheckpointBase import CheckpointBase


class HelloBasicCheckpoint(CheckpointBase):
    def check(self) -> bool:
        context = '\n'.join(self.message)
        logging.info(f"context:\n{context}")
        result = 'world' in context and 'SmartTSG' in context
        logging.info(f"Result:\n{result}")

        return result
