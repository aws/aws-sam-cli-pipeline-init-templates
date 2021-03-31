import pathlib
from typing import List

import click
import yaml

from .yaml import yaml_parse

AWS_SERVERLESS_FUNCTION = "AWS::Serverless::Function"
AWS_LAMBDA_FUNCTION = "AWS::Lambda::Function"


class TemplateNotFoundException(click.ClickException):
    pass


class TemplateFailedParsingException(click.ClickException):
    pass


def get_template_data(template_file):
    """
    Read the template file, parse it as JSON/YAML and return the template as a dictionary.

    Parameters
    ----------
    template_file : string
        Path to the template to read

    Returns
    -------
    Template data as a dictionary
    """

    if not pathlib.Path(template_file).exists():
        raise TemplateNotFoundException("Template file not found at {}".format(template_file))

    with open(template_file, "r", encoding="utf-8") as fp:
        try:
            return yaml_parse(fp.read())
        except (ValueError, yaml.YAMLError) as ex:
            raise TemplateFailedParsingException("Failed to parse template: {}".format(str(ex))) from ex

def get_template_function_runtimes(template_file: str) -> List[str]:
    """
    Get a list of function runtimes from template file.
    Function resource types include
        AWS::Lambda::Function
        AWS::Serverless::Function
    :param template_file: template file location.
    :return: list of runtimes
    """

    template_dict = get_template_data(template_file=template_file)
    _function_runtimes = set()
    for _, resource in template_dict.get("Resources", {}).items():
        if resource.get("Type") in [AWS_SERVERLESS_FUNCTION, AWS_LAMBDA_FUNCTION]:
            runtime = resource.get("Properties", {}).get("Runtime")
            if runtime:  # IMAGE functions don't define a runtime
                _function_runtimes.add(runtime)
    return list(_function_runtimes)
