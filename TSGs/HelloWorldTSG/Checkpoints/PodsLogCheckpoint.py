from Core.CheckpointBase import CheckpointBase


class PodsLogCheckpoint(CheckpointBase):
    def build_context(self):
        context = '\n\n'.join(
            [f'<PodName>\n{pod_name}\n<PodLog>\n{pod_log}' for pod_name, pod_log in zip(self.pod_names, self.pod_logs)])
        return context
