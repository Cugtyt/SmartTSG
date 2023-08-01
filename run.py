import os
import logging
import importlib
import importlib.util
import yaml

from Core.TaskBase import TaskBase
from Core.TSGPipeline import TSGPipeline
from Core.CheckpointBase import CheckpointBase

logging.basicConfig(level=logging.INFO, format='%(message)s')


def load_yaml(tsg_file_path):
    with open(tsg_file_path, 'r') as f:
        tsg_yaml = yaml.safe_load(f)
    return tsg_yaml


def build(tsg_file_path, **kwargs):
    tsg_yaml = load_yaml(tsg_file_path)

    name = tsg_yaml['Id']
    inputs = tsg_yaml.get('Inputs', [])
    tsg_pipeline = TSGPipeline(name, inputs, **kwargs)
    for step_yaml in tsg_yaml['Steps']:
        step = None
        if 'Task' in step_yaml.keys():
            step = build_task(step_yaml, tsg_file_path)
        elif 'Checkpoint' in step_yaml.keys():
            step = build_checkpoint(step_yaml, tsg_file_path)

        assert step is not None, f"Step is None: {step_yaml}"
        tsg_pipeline.add_step(step)

    return tsg_pipeline


def build_task(task_step, tsg_file_path) -> TaskBase:
    task_template = task_step['Task']
    task_name = task_step['Id']
    task_inputs = task_step.get('Inputs', [])
    task_output_keys = task_step.get('Outputs', [])

    task_class = load_class(task_template, tsg_file_path)
    task = task_class(
        name=task_name,
        inputs=task_inputs,
        output_keys=task_output_keys
    )

    return task


def build_checkpoint(checkpoint_step, tsg_file_path) -> CheckpointBase:
    checkpoint_template = checkpoint_step['Checkpoint']
    checkpoint_name = checkpoint_step['Id']
    checkpoint_inputs = checkpoint_step.get('Inputs', [])
    checkpoint_rules = checkpoint_step.get('Rules', [])

    checkpoint_class = load_class(checkpoint_template, tsg_file_path)
    checkpoint = checkpoint_class(
        name=checkpoint_name,
        inputs=checkpoint_inputs,
        rules=checkpoint_rules
    )

    return checkpoint


def load_class(template, tsg_file_path):
    if '.' in template:
        class_name = template.split('.')[-1]
        module = importlib.import_module(template)
        template_class = getattr(module, class_name)
    else:
        tsg_file_path = os.path.normpath(tsg_file_path)
        path_split = tsg_file_path.split(os.sep)
        folder = 'Tasks' if 'Task' in template else 'Checkpoints'
        module = importlib.import_module('.'.join(path_split[:2] + [folder, template]))
        template_class = getattr(module, template)
    return template_class


if __name__ == '__main__':
    tsg_file_path = os.path.join('TSGs', 'HelloWorldTSG', 'TSGfile.yaml')
    pipeline = build(tsg_file_path, namespace='my_namespace',
                     cluster='my_cluster')
    pipeline.run()
