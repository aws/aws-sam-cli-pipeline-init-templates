import os
import shutil

output_dir = "{{ cookiecutter.outputDir }}"
project_root_dir = os.path.relpath(".", output_dir)
jenkinsfile = "Jenkinsfile"

# move "Jenkinsfile" to the root of the project
destination_file_path = os.path.join(project_root_dir, jenkinsfile)
if os.path.exists(destination_file_path):
    raise Exception(
        f"{jenkinsfile} already exists in project root directory. Please remove it first."
    )

os.rename(jenkinsfile, os.path.join(project_root_dir, jenkinsfile))

# There is only one file in output_dir, remove it
shutil.rmtree(os.path.join(project_root_dir, output_dir))
