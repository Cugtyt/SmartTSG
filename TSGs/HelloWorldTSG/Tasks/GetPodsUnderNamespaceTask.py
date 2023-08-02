from Core.TaskBase import TaskBase


class GetPodsUnderNamespaceTask(TaskBase):
    def work(self) -> list[list[str]]:
        outputs = [
            [e for e in get_pod_call(self.namespace, self.cluster)],
            [e for e in get_status_call(self.namespace, self.cluster)]
        ]

        return outputs


def get_pod_call(namespace, cluster):
    return ['pod1', 'pod2']


def get_status_call(namespace, cluster):
    return [f'{namespace} {cluster} status1', f'{namespace} {cluster} status2']
