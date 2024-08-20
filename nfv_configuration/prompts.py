TEMPLATE = """Convert networking intent to json configuration based on the template. The value in the template is the default. the template is as follow:
{
    "action": "create_vnf", # can be create_vnf, update_vnf, destroy_vnf, create_sfc, update_sfc, destroy_sfc
    "create_vnf": {
        "name": "vnf-name1", # name of the VNF
        "vnf_type": "generic", # can be generic, fw, ids, lb. default is generic
        # flavor is the resource requirement for the VNF. The default value is 1 CPU, 2GB RAM, 10GB storage.
        "flavor": {
            "cpu": 1, # number of CPU cores, default is 1
            "ram_gb": 2, # amount of RAM in GB, default is 2
            "disk_gb": 10 # amount of storage in GB, default is 10
        }
        "num_instances": 1 # number of instances to create, default is 1
    },
    "update_vnf": {
        # use the same format as create_vnf. Only the fields that need to be updated are required, others can be omitted.
        "name": "vnf-name1"
    },
    "destroy_vnf": {
        "name": "vnf-name1"
    },
    "create_sfc": {
        "name": "sfc-name1",
        "max_bandwidth_mbps": 1000,
        "delay_requirement": "normal", # can be normal, low-delay, real-time. default is normal
        "flow_classifiers": [
            # the format is: "source -> destination:port_range"
            "0.0.0.0/0 -> 0.0.0.0/0:80-80",
            "0.0.0.0/0 -> 0.0.0.0/0:5000-10000"
        ],
        "vnfs": [
            # the vnf_type must not repeated in the list
            {
                "vnf_type": "ids",
                "flavor": {
                    "cpu": 1,
                    "ram_gb": 2,
                    "disk_gb": 10
                }
                "num_instances": 1
            },
            {
                "vnf_type": "firewall",
                "flavor": {
                    "cpu": 1,
                    "ram_gb": 2,
                    "disk_gb": 10
            },
                "num_instances": 2
            }
        ]
    },
    "update_sfc": {
        # update sfc with new flow classifiers, delay requirement, and/or bandwidth
        # same fields as create_sfc. Only the fields that need to be updated are required, others can be omitted.
        "name": "sfc-name1",
    },
    "destroy_sfc": {
        "name": "sfc-name1"
    },
}

the input and output are case-sensitive. Do not output anything other than the json configuration. Reply must be a valid json.
"""


# EXAMPLES = """
# input: 'make four firewalls with 1 CPU and 6GB storage. The firewall name should be "example firewall"'
# Output:
# {
#     "action": "create_vnf",
#     "create_vnf": {
#         "name": "example firewall",
#         "vnf_type": "fw",
#         "flavor": {
#                 "cpu": 1,
#                 "ram_gb": 2,
#                 "disk_gb": 6
#         },
#         "num_instances": 4
#     }
# }
# input: 'init a VNF "vnf-instance" using the generic type with 2 cpu and 4GB ram'
# Output:
# {
#     "action": "create_vnf",
#     "create_vnf": {
#         "name": "vnf-instance",
#         "vnf_type": "generic",
#         "flavor": {
#                 "cpu": 2,
#                 "ram_gb": 4,
#                 "disk_gb": 10
#         },
#         "num_instances": 1
#     }
# }
# input: 'create an SFC named "sfc1" with five firewall and ids. It should have a maximum bandwidth of 500Mbps and no latency requirement. Apply traffic filtering on port 8080 and all incoming traffic on port 22.'
# Output:
# {
#     "action": "create_sfc",
#     "create_sfc": {
#         "name": "sfc1",
#         "max_bandwidth_mbps": 500,
#         "delay_requirement": "normal",
#         "flow_classifiers": [
#             "0.0.0.0/0 -> 0.0.0.0/0:8080-8080",
#             "0.0.0.0/0 -> 0.0.0.0/0:22-22"
#         ],
#         "vnfs": [
#             {
#                 "vnf_type": "fw",
#                 "flavor": {
#                     "cpu": 1,
#                     "ram_gb": 2,
#                     "disk_gb": 10
#                 },
#                 "num_instances": 5
#             },
#             {
#                 "vnf_type": "ids",
#                 "flavor": {
#                     "cpu": 1,
#                     "ram_gb": 2,
#                     "disk_gb": 10
#                 },
#                 "num_instances": 1
#             }
#         ]
#     }
# }
# input: 'modify sfc "sfc1" to filter all traffic on port range 4000 to 5000. Also filter http traffic'
# Output:
# {
#     "action": "update_sfc",
#     "update_sfc": {
#         "name": "sfc1",
#         "flow_classifiers": [
#             "0.0.0.0/0 -> 0.0.0.0/0:4000-5000",
#             "0.0.0.0/0 -> 0.0.0.0/0:80-80"
#         ]
#     }
# }
# input: 'delete sfc named "sfc1"'
# Output:
# {
#     "action": "destroy_sfc",
#     "destroy_sfc": {
#         "name": "sfc1"
#     }
# }
# input: 'update vnf "existing-vnf" with a new flavor that has 2GB ram'
# Output: {
#     "action": "update_vnf",
#     "update_vnf": {
#         "name": "existing-vnf",
#         "flavor": {
#                 "ram_gb": 2
#         }
#     }
# }
# input: 'remove the firewall named "firewall-1"'
# Output:
# {
#     "action": "destroy_vnf",
#     "destroy_vnf": {
#         "name": "firewall-1"
#     }
# }
# input: 'update the SFC named "sfc3" with real time latency requirements'
# Output:
# {
#     "action": "update_sfc",
#     "update_sfc": {
#         "name": "sfc3",
#         "delay_requirement": "real-time"
#     }
# }
# Input: 'modify the SFC named "sfc1" to allow traffic from IP range 10.1.1.0/24'
# Output:
# {
#     "action": "update_sfc",
#     "update_sfc": {
#         "name": "sfc1",
#         "flow_classifiers": [
#             "10.1.1.0/24 -> 0.0.0.0/0:0-65535"
#         ]
#     }
# }
# """

# SYSTEM_PROMPT = TEMPLATE + "\n\n" + EXAMPLES
SYSTEM_PROMPT = TEMPLATE
