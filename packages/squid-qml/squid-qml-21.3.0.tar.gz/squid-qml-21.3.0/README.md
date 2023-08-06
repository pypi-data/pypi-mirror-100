## Development Environment Installation ##

### Development Setup ###
There are two slightly different procedures for creating a Conda and Pip environments for squid development. Conda is a recommended option, however certain users might prefer pip, either due to flexibility, or storage considerations.

#### Conda ####
```
conda create -n squid python=3.6.8 invoke --yes
conda activate squid
invoke install-required-packages develop
```

To delete Squid conda environment: `conda env remove -n squid`


#### Pip ####
From the root of this repo:
```
mkdir .venv && cd .venv && python3 -m venv squid && cd ..
source .venv/squid/bin/activate
pip install invoke
invoke install-required-packages --pip develop --pip
```

You can additionally add an alias for easier activation in the future.

Copy the output of
```
cd .venv/squid/bin
pwd
```

And paste it into your rc (or profile) file typically (`~/.bashrc` or `~/.zshrc`):
```
alias squid-activate="source <your pwd output>/activate"
```
For example: `source squid-activate="source /home/user/Documents/Research/squid/.venv/squid/bin/activate"`

After that calling: `squid-activate` is sufficient to activate squid pip environment.

To delete squid pip environment: `rm -rf .venv`

##### PyTorch dependency requirements #####
Due to issues with requiring specific versions of PyTorch on installation, we recommend using:

- PyTorch 1.6.0
- TorchVision 0.7.0
- CUDAToolkit 10.2 (This however should correspond to CUDA installed on the device. **Installed only on Conda environment**)

However, other versions should work in principle.

### Contributing ###
If you want to contribute to the project, either through fixing bugs or adding new features please install squid development environment, as explained above.

#### Checking for correctness, testing ####
To check for correctness of the new code run:
```
inv lint
```
This will run check through:

- flake8
- isort
- black
- mypy

Ideally, you should look at the output and fix the issues by hand.
However, if isort and/or black outputs are very large you can run: `inv lint --apply` which will auto-solve **only black and isort** issues.
Please note that black will sometimes break flake8 requirements (specifically with comas close to brackets), so running `inv lint --apply && inv lint` is recommended.

To test the code, and check for coverage:
```
inv test
```

#### Pushing ####
**Never push on the master branch** - Always create a branch and submit a PR, so that the work can be cross-verified.

Before attempting to push ensure that you are passing both linting and testing.

Please rebase and squash all of the commits for a given ticket before submitting a PR.
This can be done through:
```
git rebase -i
```
There mark the first commit chronologically that you have made for a given issue with flag `e`, and all the following ones for a given issue with flag `s`.
This way all of the work from the commits with flag `s` will be included under the commit with flag `e`.

Then type command:
```
git rebase --continue
```

And when prompted to change the name of the commit message. First comment out all of the commit messages from commits that have been squashed.
Then modify the commit message to look something like this:
```
Issue-Tag: Short Summary

- First detailed thing done
- Second detailed thing done
```

For example for an issue *SQUID-1 - Feeding a squid*, would have a commit message:
```
SQUID-1: Feed squid, fixed food delivery system issues.

- Feed a shrimp to a squid.
- Scaled up the delivery system needed for a bigger sized shrimp.
```

If there are multiple issues resolved in a single commit follow this pattern:
```
SQUID-5: SQUID-4: ... SQUID-n: Summary

- Details (order based on importance of changes)
```
where `SQUID-5` is a more important ticket to the project than all the others etc.

This makes the master branch cleaner and easier to go find an issue if something goes wrong. After all these steps ```git push```, and create a PR on bitbucket.
