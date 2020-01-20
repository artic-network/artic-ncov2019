# artic-base
A base template for an implementation of an ARTIC install. This can be forked and modified for specific use-cases. To do this, click the green 'Use this template' button above. You can then give your new repository a name.

You can modify the existing files to suit your use-case but avoid moving or renaming any files or directories that are in this template.

If the template is updated, you will be able to merge these changes into your repository as needed.

To install the `Conda` environment use:

```
conda env create -f environment.yml -n <environment name>
```

Where `<environment_name>` is the name you want to use (probably the same as the repo).

Then activate the environment using:

```
conda activate <environment name>
```
