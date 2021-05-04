import os
import shutil

output_dir = "{{ cookiecutter.outputDir }}"
project_root_dir = os.path.relpath(".", output_dir)
gitlabFile = ".gitlab-ci.yml"
assumeRoleFile = "assume-role.sh"

# move ".gitlab-ci.yml" and "assume-role.sh" to the root of the project
gitlab_file_path = os.path.join(project_root_dir, gitlabFile)
assume_role_file_path = os.path.join(project_root_dir, assumeRoleFile)
if os.path.exists(gitlab_file_path):
    raise Exception(
        f"{gitlabFile} already exists in project root directory. Please remove it first."
    )
if os.path.exists(assume_role_file_path):
    raise Exception(
        f"{assumeRoleFile} already exists in project root directory. Please remove it first."
    )

os.rename(gitlabFile, os.path.join(project_root_dir, gitlabFile))
os.rename(assumeRoleFile, os.path.join(project_root_dir, assumeRoleFile))

shutil.rmtree(os.path.join(project_root_dir, output_dir))
