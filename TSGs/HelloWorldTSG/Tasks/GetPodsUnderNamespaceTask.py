from Core.TaskBase import TaskBase

class GetPodsUnderNamespaceTask(TaskBase):
    def work(self) -> list[list[str]]:
        assert self.inputs is not None and len(self.inputs) == 2, f"Task {self.name} inputs is None or empty."

        outputs = [
            [e for e in get_pod_call(*self.inputs)],
            [e for e in get_status_call(*self.inputs)]
        ]

        return outputs


def get_pod_call(namespace, cluster):
    return [f'{namespace} {cluster} pod1', f'{namespace} {cluster} pod2']


def get_status_call(namespace, cluster):
    return [f'{namespace} {cluster} status1', f'{namespace} {cluster} status2']