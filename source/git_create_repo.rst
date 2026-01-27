===========================
Create local git repository
===========================

*2025-12-10*

***************
Create function
***************

.. code-block:: bash

    set -U GIT_HOME_<name of repository> "/Users/abby/Library/Mobile\ Documents/com~apple~CloudDocs/Programming/.git/.<name of repository>

    funced --save <name of repository>

    function <name of repository> --description 'Git for <reository>'
        /usr/bin/git --git-dir=$GIT_HOME_<NAME OF REPOSITORY>/.git --work-tree=<directory with files for repository> $argv
    end

***********************
Create local repository
***********************

*For ease: name of repository = repotest*

.. code-block:: bash

    repotest init $GIT_HOME_REPOTEST

************************
Create remote repository
************************

.. code-block:: bash

    gh repo create

    ? What would you like to do?  [Use arrows to move, type to filter]
    > Create a new repository on GitHub from scratch
    Create a new repository on GitHub from a template repository
    Push an existing local repository to GitHub

    ? Repository name repotest

    ? Description Place for tests

    ? Visibility  [Use arrows to move, type to filter]
    Public
    > Private
    Internal

    ? Would you like to add a README file? (y/N) N

    ? Would you like to add a README file? No

    ? Would you like to add a .gitignore? No

    ? Would you like to add a license? No

    ? This will create "repotest" as a private repository on GitHub. Continue? (Y/n) Y
    ✓ Created repository abby/testrepo on GitHub
    https://github.com/abby/testrepo

    ? Clone the new repository locally? No


Configure files to track
========================

.. code-block:: bash

    testrepo config --local status.showUntrackedFiles no

    cd <directory with files for repository>

.. code-block::

    repotest add <directories or files>


**Examples:**

``testrepo add test1/``  
\--Adds entire directory and subdirectories

``testrepo add test1/*.txt``  
\--Adds only the .txt files in that directory

``testrepo add $(find test1/test2/ -type f -maxdepth 1)``  
\--Adds only the files in test1/test2 directory without adding any files from test1/test2/test3 subdirectory

Commit files
============

.. code-block:: bash

    testrepo commit -m "<Description of commit>"

Configure push and push files
=============================

.. code-block:: bash

    testrepo remote add origin <url to repo created earlier>

    testrepo branch -M main

    testrepo push -u origin main

Check status of local repository
================================

.. code-block:: bash

    testrepo status
