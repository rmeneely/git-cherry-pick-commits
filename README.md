# git-cherry-pick-commits
This GitHub Action is provided a space delimited string of git commit SHAs. It will execute a `git cherry-pick` command on each commit. If the commit is a merge commit it will execute a `git cherry-pick -m 1` command.

This GitHub Action is intended to be used with the `rmeneely/git-matching-commits` action which generates a list of matching commits.


## Usage
```yaml
    - uses: rmeneely/git-cherry-pick-commits@v1
      with:
        commits: "list of commitSHAs"
```

### Inputs
All inputs are optional. If not set the default value will be used.

| Name                   | Description                                 | Default              |
| ---------------------- |:------------------------------------------- | :------------------------------------------- |
| commits                | Space delimited list of commitSHAs  | (required) |
| repo_path              | Path to git reporitory    | '.' |
| keep_redundant_commits | See `git cherry-pick --keep-redundant-commits` | False |
| no_execute | Print commands, but do not execute them | False |

## Examples
```yaml
    # Cherry picks the list of commits and returns those that were successful
    - uses: rmeneely/git-cherry-pick-commits@v1
      id: git-cherry-pick-commits
      with:
        commits: 'f9e96e6afbf893795c3c5f44d968b19fa51925cc e5b84631f0824d9e8c57d44893abdae96917aab9 186e65812e63c80fbf3690723454ebc5f09fb05b'
    - name: Get cherry-picked commits
      run: echo "CHERRY_PICKED_COMMITS=${{ steps.git-cherry-pick-commits.outputs.commits }}" >> $GITHUB_ENV
```

```yaml
    # Displays the git cherry-pick commands, but does not execute them
    - uses: rmeneely/git-cherry-pick-commits@v1
      id: git-cherry-pick-commits
      with:
        commits: 'f9e96e6afbf893795c3c5f44d968b19fa51925cc e5b84631f0824d9e8c57d44893abdae96917aab9 186e65812e63c80fbf3690723454ebc5f09fb05b'
        no_execute: true
    - name: Get cherry-picked commits
      run: echo "CHERRY_PICKED_COMMITS=${{ steps.git-cherry-pick-commits.outputs.commits }}" >> $GITHUB_ENV
```

## Output
```shell
steps.git-cherry-pick-commits.outputs.commits      # Space delimited list of sucessful cherry-picked commitSHAs

Example:
steps.git-cherry-pick-commits.outputs.commits=f9e96e6afbf893795c3c5f44d968b19fa51925cc e5b84631f0824d9e8c57d44893abdae96917aab9 186e65812e63c80fbf3690723454ebc5f09fb05b
```

## License
The MIT License (MIT)
