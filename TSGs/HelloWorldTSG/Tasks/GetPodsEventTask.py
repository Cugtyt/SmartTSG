from Core.TaskBase import TaskBase


class GetPodsEventTask(TaskBase):
    def work(self) -> list[str]:
        assert self.inputs is not None and len(
            self.inputs) > 0, f"Task {self.name} inputs is None or empty."

        outputs = [event_call(p, self.inputs[1], self.inputs[2])
                   for p in self.inputs[0]]
        return outputs


def event_call(pod_name, namespace, cluster):
    return f'{pod_name} {namespace} {cluster} event'
