from Core.CheckpointBase import CheckpointBase


class PodsLogCheckpoint(CheckpointBase):
    def build_context(self):
        assert self.inputs is not None

        pod_names = self.inputs[0]
        pod_logs = self.inputs[1]
        context = '\n\n'.join([f'<PodName>\n{pod_name}\n<PodLog>\n{pod_log}' for pod_name, pod_log in zip(pod_names, pod_logs)])
        return context