# Git

Git is a free and open source distributed tracking system [git-scm.com](https://git-scm.com/). It is a powerful source-control
tool with powerful multi-user features. The ease of creating and working with multiple branches enables the "Pull-Request" model
of development used on [GitHub] and several other Git-based hosting sites.

If you are developing code as part of your job or as a student doing reasearch, you should take the time to learn a little bit
about Git. This page is here to provide a few tips that the MOOSE team has learned over the years. It is not meant as a
beginners tutorial.

## Git tutorials and resources

[Learning Resources](https://help.github.com/articles/git-and-github-learning-resources/)

## Downloading a single PR from Github

If you want to try out somebody elses code, you can always add a new remote to pull in their repository. If you do this a lot
however, you might find yourself with a huge number of remotes that you don't really care about. There is a better way:
[https://help.github.com/articles/checking-out-pull-requests-locally/](https://help.github.com/articles/checking-out-pull-requests-locally/)

## Git completion

To enable bash completion for git (so you can tab-complete 'git co' or 'git br' commands) download [git_completion.sh](http://mooseframework.org/static/media/uploads/files/git_completion.sh) to your home directory, and append the following line to the end of your ~/.bash_profile (or ~/.bashrc)

```bash
source ~/git_completion.sh
```

If you would like to have the name of the current branch in your prompt, download [git_prompt.sh](http://mooseframework.org/static/media/uploads/files/git_prompt.sh) to your home directory, and append the following lines to the end of your ~/.bash_profile (or ~/.bashrc)

```bash
source ~/git_prompt.sh
export PS1='$(__git_ps1 "(%s)")$ '
```

Assuming your prompt is just '$ ', adding this line to your `.bash_profile` will cause it to look like `(master)$` whenever you `cd` into a directory containing a git repo in where the `master` branch is checked out.


## Git Config

The first time you try to commit to git a new machine, it'll likely complain that it doesn't know who you are and will tell you to set your
name and email address. Once you run those commands a hidden file will be created in your home directory called `.gitconfig`. This file can
be customized to make using git easier once you learn your way around. As a start, you might try to shorten up some of the longer commands so
that you don't have to type them all the time. You might also turn on more color, especially if you work on the command line all day. Here are
a few suggestions to get you started. There are many more options that can be added [git-config](https://git-scm.com/docs/git-config).


```
[user]
        name = <Your Name>
        email = <Your Email Address>

[color]
        diff = auto
        status = auto
        branch = auto
        interactive = auto
        ui = true
        pager = true

[alias]
        co = checkout
        di = diff
        st = status
        ci = commit
        stat = status
        br = branch
```