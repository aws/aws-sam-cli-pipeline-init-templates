import os
from pathlib import Path

output_dir = "{{ cookiecutter.outputDir }}"
project_root_dir = os.path.relpath(".", output_dir)
workflow_dir = os.path.join(project_root_dir, '.github', 'workflows')
workflow_file_name = "pipeline.yaml"

# make sure workflow directory exists
Path(workflow_dir).mkdir(parents=True, exist_ok=True)

# move workflow file to the workflow directory
destination_file_path = os.path.join(workflow_dir, workflow_file_name)
if os.path.exists(destination_file_path):
    raise Exception(
        f"{workflow_file_name} already exists in {workflow_dir}. Please remove it first."
    )

os.rename(workflow_file_name, destination_file_path)

# There is only one file in output_dir, remove it
os.rmdir(os.path.join(project_root_dir, output_dir))