
import logging

def check_subnet_exists_in_reachability(router: str, subnet: str, result: dict) -> bool:
    if "reachability" not in result:
        return False

    result = result["reachability"]
    if router in result.keys():
        if subnet in result[router]:
            return True

    return False

def check_value_exists_in_waypoint(waypoint: str, switches: list, result: dict) -> bool:
    if "waypoint" not in result:
        return False

    waypoints = result["waypoint"]
    if waypoint in waypoints and (switch in waypoints[waypoint] for switch in switches):
        return True

    return False


def check_value_exists_in_loadbalacing(loadbalancing: str, num: int, result: dict) -> bool:
    if "loadbalancing" not in result:
        return False

    loadbalancings = result["loadbalancing"]
    if loadbalancing in loadbalancings and int(loadbalancings[loadbalancing]) == num:
        return True

    return False


def compare_result(expected: dict, result: dict) -> None:
    count_expected = 0
    count_res = 0
    count_fail = 0
    count_wrong = 0
    if "reachability" in expected:
        for router, subnets in expected["reachability"].items():
            for subnet in subnets:
                count_expected += 1
                if not check_subnet_exists_in_reachability(router, subnet, result):
                    count_fail += 1
                    logging.warning(f"Fail to translate expected reachability from `{router}` to `{subnet}`.")

    if "waypoint" in expected:
        for waypoint, switches in expected["waypoint"].items():
            count_expected += 1
            if not check_value_exists_in_waypoint(waypoint, switches, result):
                count_fail += 1
                logging.warning(f"Fail to translate expected waypoint `{waypoint}`.")

    if "loadbalancing" in expected:
        for loadbalancing, num in expected["loadbalancing"].items():
            count_expected += 1
            if not check_value_exists_in_loadbalacing(loadbalancing, num, result):
                count_fail += 1
                logging.warning(f"Fail to translate expected load balancing `{loadbalancing}`.")

    if "reachability" in result:
        for router, subnets in result["reachability"].items():
            for subnet in subnets:
                count_res += 1
                if not check_subnet_exists_in_reachability(router, subnet, expected):
                    if "waypoint" not in expected or f"({router},{subnet})" not in expected["waypoint"]:
                        count_wrong += 1
                        logging.warning(f"Translate wrongly reachability from `{router}` to `{subnet}`.")

    if "waypoint" in result:
        for waypoint, switches in result["waypoint"].items():
            count_res += 1
            if not check_value_exists_in_waypoint(waypoint, switches, expected):
                count_wrong += 1
                logging.warning(f"Translate wrongly waypoint `{waypoint}`.")

    if "loadbalancing" in result:
        for loadbalancing, num in result["loadbalancing"].items():
            count_res += 1
            if not check_value_exists_in_loadbalacing(loadbalancing, num, expected):
                count_wrong += 1
                logging.warning(f"Translate wrongly load balancing `{loadbalancing}`.")

    count_correct = count_expected - count_fail
    return (count_correct, count_expected)
