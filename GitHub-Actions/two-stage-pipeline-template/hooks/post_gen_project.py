import os
import shutil
from pathlib import Path

output_dir = "{{ cookiecutter.outputDir }}"
project_root_dir = os.path.relpath(".", output_dir)
workflow_dir = Path(project_root_dir, ".github", "workflows")
workflow_file_name = "pipeline.yaml"

# make sure workflow directory exists
workflow_dir.mkdir(parents=True, exist_ok=True)

# move workflow file to the workflow directory
destination_file = Path(workflow_dir, workflow_file_name)
if destination_file.exists():
    raise Exception(
        f"{workflow_file_name} already exists in {workflow_dir}. Please remove it first."
    )

os.rename(workflow_file_name, destination_file)

# There is only one file in output_dir, remove it
# on Windows, cwd cannot be deleted. Change the cwd to project_root first.
os.chdir(project_root_dir)
shutil.rmtree(output_dir)
