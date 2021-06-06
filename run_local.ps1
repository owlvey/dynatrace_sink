docker run --rm --name=owlvey-dyn `
--mount type=bind,source="$(pwd)"/wip,target=/wip `
-e "app__start_on=2021-03-25 10:00:00"`
-e "app__dyn_entity=Controller"`
-e "app__dyn_tag="`
-e "app__dyn_host="`
-e "app__dyn_token="`
-e "app__dyn_prefix="`
-e "app__dir_output=/wip"`
-p 5000:8050 owlvey/owlvey-dynatrace-sink