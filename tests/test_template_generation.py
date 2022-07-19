import json
import tempfile
from pathlib import Path
from unittest import TestCase

from samcli.commands.pipeline.init.interactive_init_flow import (
    _initialize_pipeline_template,
)


class TestTemplateGeneration(TestCase):
    def _generate_and_verify(
        self,
        template_dir: Path,
        context_override_file: Path,
        file_name: str,
        expected_file: Path,
    ):
        self.maxDiff = None

        with open(template_dir.joinpath("cookiecutter.json")) as context_file, open(
            context_override_file
        ) as context_overrides:
            context = json.load(context_file)
            context.update(json.load(context_overrides))

        pipeline_template = _initialize_pipeline_template(template_dir)

        with tempfile.TemporaryDirectory() as tmp_dir:
            pipeline_template.generate_project(context, tmp_dir)
            with open(expected_file, "r") as expected, open(
                Path(tmp_dir, context["outputDir"], file_name)
            ) as generated_file:
                self.assertEqual(expected.read(), generated_file.read())

    def test_jenkins(self):
        template_dir = Path(__file__).parent.parent.joinpath(
            "Jenkins/two-stage-pipeline-template"
        )
        context_overrides_file = Path(__file__).parent.joinpath(
            "testfile_jenkins", "context_overrides.json"
        )
        expected_file = Path(__file__).parent.joinpath("testfile_jenkins", "expected")

        self._generate_and_verify(
            template_dir, context_overrides_file, "Jenkinsfile", expected_file
        )

    def test_bitbucket_oidc(self):
        template_dir = Path(__file__).parent.parent.joinpath(
            "Bitbucket-Pipelines/two-stage-pipeline-template"
        )
        context_overrides_file = Path(__file__).parent.joinpath(
            "testfile_bitbucket", "context_overrides_oidc.json"
        )
        expected_file = Path(__file__).parent.joinpath("testfile_bitbucket", "expected_oidc.yml")

        self._generate_and_verify(
            template_dir, context_overrides_file, "bitbucket-pipelines.yml", expected_file
        )

    def test_bitbucket_iam(self):
        template_dir = Path(__file__).parent.parent.joinpath(
            "Bitbucket-Pipelines/two-stage-pipeline-template"
        )
        context_overrides_file = Path(__file__).parent.joinpath(
            "testfile_bitbucket", "context_overrides_iam.json"
        )
        expected_file = Path(__file__).parent.joinpath("testfile_bitbucket", "expected_iam.yml")

        self._generate_and_verify(
            template_dir, context_overrides_file, "bitbucket-pipelines.yml", expected_file
        )

    def test_github_actions_oidc(self):
        template_dir = Path(__file__).parent.parent.joinpath(
            "GitHub-Actions/two-stage-pipeline-template"
        )
        context_overrides_file = Path(__file__).parent.joinpath(
            "testfile_github", "context_overrides_oidc.json"
        )
        expected_file = Path(__file__).parent.joinpath("testfile_github", "expected_oidc.yaml")

        self._generate_and_verify(
            template_dir, context_overrides_file, "./.github/workflows/pipeline.yaml", expected_file
        )

    def test_github_actions_iam(self):
        template_dir = Path(__file__).parent.parent.joinpath(
            "GitHub-Actions/two-stage-pipeline-template"
        )
        context_overrides_file = Path(__file__).parent.joinpath(
            "testfile_github", "context_overrides_iam.json"
        )
        expected_file = Path(__file__).parent.joinpath("testfile_github", "expected_iam.yaml")

        self._generate_and_verify(
            template_dir, context_overrides_file, "./.github/workflows/pipeline.yaml", expected_file
        )

    def test_gitlab(self):
        template_dir = Path(__file__).parent.parent.joinpath(
            "Gitlab/two-stage-pipeline-template"
        )
        context_overrides_file = Path(__file__).parent.joinpath(
            "testfile_gitlab", "context_overrides.json"
        )
        expected_file = Path(__file__).parent.joinpath("testfile_gitlab", "expected.yml")

        self._generate_and_verify(
            template_dir, context_overrides_file, ".gitlab-ci.yml", expected_file
        )