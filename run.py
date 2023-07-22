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

def build(tsg_yaml, tsg_file_path, **kwargs):
    name = tsg_yaml['Name']
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
    task_name = task_step['Name']
    task_inputs = task_step.get('Inputs', [])
    task_output_keys = task_step.get('Outputs', [])

    sep = '/'
    if sep in task_template:
        task_file = task_template + '.py'
        task_template = task_template.split(sep)[-1]
    else:
        tsg_dir = os.path.dirname(tsg_file_path)
        task_file = os.path.join(tsg_dir, 'Tasks', f'{task_template}.py')

    task_class = load_class(task_template, task_file)
    task = task_class(
        name=task_name,
        inputs=task_inputs,
        output_keys=task_output_keys
    )

    return task

def build_checkpoint(checkpoint_step, tsg_file_path) -> CheckpointBase:
    checkpoint_template = checkpoint_step['Checkpoint']
    checkpoint_name = checkpoint_step['Name']
    checkpoint_inputs = checkpoint_step.get('Inputs', [])
    checkpoint_rules = checkpoint_step.get('Rules', [])

    sep = '/'
    if sep in checkpoint_template:
        checkpoint_file = checkpoint_template + '.py'
        checkpoint_template = checkpoint_template.split(sep)[-1]
    else:
        tsg_dir = os.path.dirname(tsg_file_path)
        checkpoint_file = os.path.join(tsg_dir, 'Checkpoints', f'{checkpoint_template}.py')

    checkpoint_class = load_class(checkpoint_template, checkpoint_file)
    checkpoint = checkpoint_class(
        name=checkpoint_name,
        inputs=checkpoint_inputs,
        rules=checkpoint_rules
    )

    return checkpoint


def load_class(template, file_path):
    spec = importlib.util.spec_from_file_location(template, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    template_class = getattr(module, template)
    return template_class

if __name__ == '__main__':
    tsg_file_path = os.path.join('TSGs', 'HelloWorldTSG', 'TSGfile.yaml')
    tsg_yaml = load_yaml(tsg_file_path)
    pipeline = build(tsg_yaml, tsg_file_path, namespace='my_namespace', cluster='my_cluster')
    pipeline.run()