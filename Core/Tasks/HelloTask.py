from Core.TaskBase import TaskBase


class HelloTask(TaskBase):
    def work(self) -> list[str]:
        return [
            'hello world!',
            'hello SmartTSG!'
        ]
