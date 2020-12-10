import json
import os

from github import Github


def read_json(filepath):
    """
    Read a json file as a dictionary.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    data : dict

    """
    with open(filepath, 'r') as f:
        return json.load(f)


def get_actions_input(input_name):
    """
    Get a Github actions input by name.

    Parameters
    ----------
    input_name : str

    Returns
    -------
    action_input : str

    Notes
    -----
    GitHub Actions creates an environment variable for the input with the name:

    INPUT_<CAPITALIZED_VARIABLE_NAME> (e.g. "INPUT_FOO" for "foo")

    References
    ----------
    .. [1] https://help.github.com/en/actions/automating-your-workflow-with-github-actions/metadata-syntax-for-github-actions#example  # noqa: E501

    """
    return os.getenv('INPUT_{}'.format(input_name).upper())


def load_template(filename):
    """
    Load a template.

    Parameters
    ----------
    filename : template file name

    Returns
    -------
    template : str

    """
    template_path = filename
    with open(template_path, 'r') as f:
        return f.read()


def main():
    # search a pull request that triggered this action
    gh = Github(os.getenv('GITHUB_TOKEN'))
    workflow_id = os.getenv('GITHUB_RUN_ID')
    event = read_json(os.getenv('GITHUB_EVENT_PATH'))
    repo = gh.get_repo(event['repository']['full_name'])
    pr = repo.issue(event['issue']['number'])


    # load template
    template = load_template(get_actions_input('filename'))

    # build a comment
    pr_info = {
        'workflow_id': workflow_id
    }
    new_comment = template.format(**pr_info)

    # add the comment
    pr.create_issue_comment(new_comment)


if __name__ == '__main__':
    main()
