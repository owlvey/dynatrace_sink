# dynatrace_sink


# fork


# add github remote as "sync"
git remote add sync git@github.com:owlvey/dynatrace_sink.git
git remote add sync git@github.com:owlvey/grafana.git
git remote add sync git@github.com:owlvey/archon.git

# verify remotes
git remote -v


git pull sync main

# setup local "github" branch to track "sync" remote's "master" branch
git branch --track github sync/main

# switch to the new branch
git checkout github
git checkout master
# push local "master" branch to "origin" remote (bitbucket)
git push -u origin master


