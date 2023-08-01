from Core.CheckpointBase import CheckpointBase


class HelloGptCheckpoint(CheckpointBase):
    def build_context(self) -> str:
        assert self.inputs is not None

        context = '\n'.join(self.inputs[0])
        return context
