#!/usr/bin/env python3

# Modules
import argparse
import re
import os
# import subprocess
# import requests
# See https://gitpython.readthedocs.io/en/stable/tutorial.html
from git import Repo
from github_action_utils import set_output
# from github import Github
# from github import Auth


# Global variables

def parse_args():
    # Arguments
    parser = argparse.ArgumentParser(description='Performs git cherry-pick on the list of commitSHAs')
    parser.add_argument('--commits', type=str, help='Space separated list of commitSHAs')
    parser.add_argument('--repo_path', type=str, help='Path to the repository')
    parser.add_argument('--keep_redundant_commits', action="store_true", help='Keep redundant commits')
    parser.add_argument('--no_execute', action="store_true", help='Just print the commands, do not execute them')
    parser.add_argument('--verbose', action="store_true", help='Verbose output')
    args = parser.parse_args()
    return args

def get_commitSHA_for_tag(repo, tag_name):
    commitSHA = repo.tags[tag_name].commit.hexsha
    return commitSHA

def get_pr_commit_range(pull_request):
    commit = ''
    commit_range = ''
    lines = pull_request.split('\n')
    pr_commit_range = {}
    for line in lines:
        if line.startswith("commit "):
            commit = line.split(' ')[1]
        if line.startswith("Merge:"):
            commit_range = line.split('Merge: ')[1]
    pr_commit_range[commit] = {}
    start = commit_range.split(' ')[0]
    end = commit_range.split(' ')[1]
    pr_commit_range[commit]['start'] = start
    pr_commit_range[commit]['end'] = end
    return pr_commit_range

def get_pr_commit_ranges(pull_requests):
    pr_commit_ranges = {}
    for pull_request in pull_requests:
        pr_commit_range = get_pr_commit_range(pull_request)
        pr_commit_ranges[pr_commit_range] = None
    return pr_commit_ranges

def extract_merge_values(string):
    merge_index = string.find('Merge:') + len('Merge:')
    merge_values = string[merge_index:].split()[:2]
    return merge_values

def extract_commit_value(string):
    commit_index = string.find('commit ') + len('commit ')
    commit_value = string[commit_index:].split()[0]
    return commit_value

def main():
    # Default variable values
    Default = {
        'commits': '.',
        'repo_path': '.',
        'keep_redundant_commits': False,
        'no_execute': False,
        'verbose': False,
    }

    # Get arguments
    args = parse_args()

	# Global variables
    commitSHAs = args.commits.split(' ') if (args.commits != None) else Default['commits']
    repoPath = args.repo_path if (args.repo_path != None) else Default['repo_path']
    keepRedundantCommits = args.keep_redundant_commits if (args.keep_redundant_commits != None) else Default['keep_redundant_commits']
    noExecute = args.keep_redundant_commits if (args.no_execute != None) else Default['no_execute']
    Verbose = True if args.verbose else Default['verbose']
    successfulCommits = []

    # Open the Git repository
    repo = Repo(repoPath)
    git = repo.git

    preCommand = "echo " if noExecute else ""
    head = repo.head.commit
    command = "{}cd {}".format(preCommand, repoPath)
    os.system(command)

    for commitSHA in commitSHAs:
        if commitSHA.startswith('tag:'):
            tag_name = commitSHA.split(':')[1]
            commitSHA = get_commitSHA_for_tag(repo, tag_name)
        commit = repo.commit(commitSHA)
        options = ''
        if keepRedundantCommits:
            options += '--keep-redundant-commits'
        try:
            if commit.parents and len(commit.parents) > 1:
                command = "{}git cherry-pick {} -m 1 {}".format(preCommand, options, commitSHA)
            else:
                command = "{}git cherry-pick {} {}".format(preCommand, options, commitSHA)
            os.system(command)
            successfulCommits.append(commitSHA)
        except git.GitCommandError as e:
            print(e)
            command = "{}git cherry-pick --abort".format(preCommand)
            os.system(command)

    # Return matching commits
    cherry_picked_commits = ' '.join(successfulCommits)
    print("commits={0}".format(cherry_picked_commits))
    if "GITHUB_OUTPUT" in os.environ:
        set_output('commits', cherry_picked_commits)

if __name__ == '__main__':
    main()
# End of file
