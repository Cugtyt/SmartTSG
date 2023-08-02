from Core.CheckpointBase import CheckpointBase


class HelloGptCheckpoint(CheckpointBase):
    def build_context(self) -> str:
        context = '\n'.join(self.message)
        return context
