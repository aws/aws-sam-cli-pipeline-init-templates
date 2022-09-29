import os, boto3
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities import parameters

logger = Logger()
cc = boto3.client('codecommit')
cp = boto3.client('codepipeline')
ssm = boto3.client('ssm')

ssm_prefix = os.environ.get('SSM_PREFIX', '')
app_dir = os.environ.get('APP_DIR_IN_MONOREPO')
pipeline_name = os.environ.get('PIPELINE_NAME')

@logger.inject_lambda_context
def lambda_handler(event, _):
    logger.info(event)
    commit_id = event['detail']['commitId']
    branch_name = event['detail']['referenceName']
    repository = event['detail']['repositoryName']

    paths = get_modified_files_since_last_run(repository, commit_id, branch_name)
    toplevel_dirs = get_unique_toplevel_dirs(paths)
    logger.info({'paths': paths, 'toplevel_dirs': toplevel_dirs, 'pipeline_name': pipeline_name})

    if app_dir in toplevel_dirs:
        start_codepipeline(pipeline_name)
    else:
        logger.info('Not triggering Pipeline %s. No changes under App dir %s', pipeline_name, app_dir)

    update_last_commit(repository, commit_id, branch_name)

def get_unique_toplevel_dirs(modified_files):
    toplevel_dirs = set(filter(lambda a: len(a) > 1, [file.split('/')[0] for file in modified_files]))
    logger.info('toplevel dirs: %s', toplevel_dirs)
    return list(toplevel_dirs)

def start_codepipeline(codepipeline_name):
    try:
        cp.start_pipeline_execution(name=codepipeline_name)
        logger.info(f'Started CodePipeline {codepipeline_name}.')
    except cp.exceptions.PipelineNotFoundException:
        logger.info(f'Could not find CodePipeline {codepipeline_name}.')
        return False
    return True

def param_name_last_commit(repository, branch_name):
    return os.path.join('/', ssm_prefix, repository, branch_name, app_dir, 'LastCommit')  # type: ignore

def get_last_commit(repository, commit_id, branch_name):
    param_name = param_name_last_commit(repository, branch_name)
    try:
        return str(parameters.get_parameter(param_name, force_fetch=True))
    except parameters.GetParameterError:
        logger.info('not found ssm parameter %s', param_name)
        commit = cc.get_commit(repositoryName=repository, commitId=commit_id)['commit']
        parent = commit['parents'][0] if commit['parents'] else ''  # type: ignore
        return parent

def update_last_commit(repository, commit_id, branch_name):
    ssm.put_parameter(Name=param_name_last_commit(repository, branch_name),
                        Description='Keep track of the last commit already triggered',
                        Value=commit_id, Type='String', Overwrite=True)

def get_modified_files_since_last_run(repo_name, after_commit, branch_name):
    last_commit = get_last_commit(repo_name, after_commit, branch_name)
    diff = cc.get_differences(repositoryName=repo_name,
                                beforeCommitSpecifier=last_commit,
                                afterCommitSpecifier=after_commit
                            ).get('differences', None)
    logger.info(f"last_commit: '{last_commit}' - commit_id: '{after_commit}'")
    logger.info(f"diff: {diff}")
    before_blob_paths = {d.get('beforeBlob', {}).get('path') for d in diff}
    after_blob_paths = {d.get('afterBlob', {}).get('path') for d in diff}
    all_modifications = before_blob_paths.union(after_blob_paths)
    return list(filter(lambda f: f is not None, all_modifications))
