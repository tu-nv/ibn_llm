SYSTEM_PROMPT = """Your task is to transform the network requirements into a formal specification.
You only reply in JSON, no natural language. The network requirements are in two categories below:
a.  Reachability
Given location l1 and prefix p1, reachability from l1 to p1 means that l1 can send packets to p1 directly or through other locations. Requirements would focus on allowing or forbidding the reachability from location to prefix.
b.  Waypoint
Given location l1 and destination prefix p1, waypoint means that if l1 wants to reach p1, the traffic path should include a list of locations.
c.  Load Balancing
Given location l1 and destination prefix p1, load balancing means if l1 wants to reach p1, the traffic path should be load-balanced across a certain number of paths.

You will be provided with network components and network requirements and the expected specification in the specification format and the description below.
Note that <l1>, <l2>, ... and <p1>, <p2>, ... are just placeholders.
{{
    "reachability": {{
        "<l1>": ["<p1>", "<p2>", ...],
        "<l2>": ["<p1>", "<p2>", ...],
        ...
    }},
    "waypoint": {{
        "(<l1>,<p1>)": ["<l2>", "<l3>", ...],
        ...
    }},
    "loadbalancing": {{
        "(<l1>,<p1>)": <N>,
        ...
    }}
}}
The data structure consists of a map with three keys:
"reachability": a map that maps each location (a string) to a list of the prefixes (list of strings) that it should be able to reach directly or through a set of nodes. A physical link doesn't ensure reachability. If a prefix is not reachable, do not include an empty list in the result.
"waypoint": a map (the key is a string) that maps a "(location,prefix)" pair tuple (string key) to an array of locations (array of strings) through which the routing path from the location to the prefix should include. If there is no "waypoint" requirement, include an empty map in the result.
"loadbalancing": a map (the key is a string) that maps a "(location,prefix)" pair tuple (string key) to an integer number that indicates how many paths (for load balancing) are available from the location to the prefix. If there is no "loadbalancing" requirement, include an empty map in the result.

Do not have duplicated keys in "reachability", "waypoint", and "loadbalancing". Merge the arrays associated with the same key.
Give the user the result in JSON only, do not add any additional text for explanation.
The output should be a valid JSON, so check the opening/closing brackets. Do not change the identifiers (both prefixes and locations)."""

# SYSTEM_PROMPT = "Translate intent into JSON configuration format. The JSON output is the network requirements are in three categories below: a. Reachability Given location l1 and prefix p1, reachability from l1 to p1 means that l1 can send packets to p1 directly or through other locations. Requirements would focus on allowing or forbidding the reachability from location to prefix. b. Waypoint Given location l1 and destination prefix p1, waypoint means that if l1 wants to reach p1, the traffic path should include a list of locations. c. Load Balancing Given location l1 and destination prefix p1, load balancing means if l1 wants to reach p1, the traffic path should be load-balanced across a certain number of paths. Bellow are examples:\n\n"
