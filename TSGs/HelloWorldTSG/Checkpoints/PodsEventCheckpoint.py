from Core.CheckpointBase import CheckpointBase


class PodsEventCheckpoint(CheckpointBase):
    def build_context(self):
        context = '\n\n'.join(
            [f'<PodName>\n{pod_name}\n<PodEvents>\n{pod_event}' for pod_name, pod_event in zip(self.pod_names, self.pod_events)])
        return context
