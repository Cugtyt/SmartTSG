from Core.TaskBase import TaskBase


class GetPodsLogTask(TaskBase):
    def work(self) -> list[str]:
        outputs = [log_call(p, self.namespace, self.cluster)
                   for p in self.pod_names]

        return outputs


def log_call(pod_name, namespace, cluster):
    return f'{pod_name} {namespace} {cluster} log'
