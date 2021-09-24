$env:app__start_on="2021-06-25 10:00:00"
$env:app__dyn_entity="Controller" # sufijo 
$env:app__dyn_tag="unique" # tag de los controladores
$env:app__dyn_host="https://managed.dynatrace/e/1d4cddc0/api/v1/"
$env:app__dyn_token=""
$env:app__dyn_prefix=""
$env:app__dir_output="./wip"
$env:app__enable_dyn_metric=1
$env:app__enable_dyn_metadata=0
$env:app__enable_dyn_problem=1
python3 ./startup.py

