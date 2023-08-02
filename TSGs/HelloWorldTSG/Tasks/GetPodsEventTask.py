from Core.TaskBase import TaskBase


class GetPodsEventTask(TaskBase):
    def work(self) -> list[str]:
        outputs = [event_call(p, self.namespace, self.cluster)
                   for p in self.pod_names]
        return outputs


def event_call(pod_name, namespace, cluster):
    return f'{pod_name} {namespace} {cluster} event'
