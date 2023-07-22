from Core.CheckpointBase import CheckpointBase


class PodsEventCheckpoint(CheckpointBase):
    def build_context(self):
        assert self.inputs is not None

        pod_names = self.inputs[0]
        pod_events = self.inputs[1]
        context = '\n\n'.join([f'<PodName>\n{pod_name}\n<PodEvents>\n{pod_event}' for pod_name, pod_event in zip(pod_names, pod_events)])
        return context