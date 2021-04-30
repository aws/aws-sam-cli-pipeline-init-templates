import os

output_dir = "{{ cookiecutter.outputDir }}"
project_root_dir = os.path.relpath(".", output_dir)
gitlabFile = ".gitlab-ci.yml"

# move ".gitlab-ci.yml" to the root of the project
destination_file_path = os.path.join(project_root_dir, gitlabFile)
if os.path.exists(destination_file_path):
    raise Exception(
        f"{gitlabFile} already exists in project root directory. Please remove it first."
    )

os.rename(gitlabFile, os.path.join(project_root_dir, gitlabFile))
