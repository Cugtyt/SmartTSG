from Core.CheckpointBase import CheckpointBase


class HelloCheckpoint(CheckpointBase):
    def build_context(self):
        assert self.inputs is not None

        context = '\n'.join(self.inputs[0])
        return context