# TODO: we should be able to take in a yaml file specifying different projects,
# generate containers for the projects, and update the yaml to reflect the location 
# of these containers 

import os
import sys
import yaml

def mongo_container_generator(init_path):
     with open(init_path, 'r') as stream:
        try:
            # TODO:
            parsed_container_config = yaml.safe_load(stream)

        #     max_port = 27017
        #     for project_id in parsed_mongo_config:
        #         project = parsed_mongo_config[project_id]
        #         port = project['port']
        #         if port != -1:
        #             max_port = port
        #         else:
        #             # update the port for the project
        #             location = project['location']
        #             port = max_port + 1
                    
        #             max_port = port
        #             project['port'] = port

        #             # generate daemon
        #             # os.system("sudo ./generate_mongo_daemon.sh {0} {1}".format(location, port))
        #             os.system("sudo mongod --fork --logpath {0}/mongodb.log --dbpath {0} --port {1}".format(location, port))
                    

        #     # update the yaml
        #     with open(init_path, "w") as stream:
        #         yaml.dump(parsed_mongo_config, stream)

        # except yaml.YAMLError as exc:
        #     print(exc)

# monogo_daemon_generator('mongo-project-config.yaml')

# if len(sys.argv) != 2:
#     raise Exception("Please provide a path to a Mongo Project Configuration file.")

# mongo_daemon_generator(sys.argv[1])
