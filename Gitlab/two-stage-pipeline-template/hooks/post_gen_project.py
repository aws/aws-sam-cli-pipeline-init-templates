import os
import shutil

output_dir = "{{ cookiecutter.outputDir }}"
project_root_dir = os.path.relpath(".", output_dir)
gitlab_file = ".gitlab-ci.yml"
assume_role_file = "assume-role.sh"

# move ".gitlab-ci.yml" and "assume-role.sh" to the root of the project
gitlab_file_path = os.path.join(project_root_dir, gitlab_file)
assume_role_file_path = os.path.join(project_root_dir, assume_role_file)
if os.path.exists(gitlab_file_path):
    raise Exception(
        f"{gitlab_file} already exists in project root directory. Please remove it first."
    )
if os.path.exists(assume_role_file_path):
    raise Exception(
        f"{assume_role_file} already exists in project root directory. Please remove it first."
    )

os.rename(gitlab_file, os.path.join(project_root_dir, gitlab_file))
os.rename(assume_role_file, os.path.join(project_root_dir, assume_role_file))

shutil.rmtree(os.path.join(project_root_dir, output_dir))
