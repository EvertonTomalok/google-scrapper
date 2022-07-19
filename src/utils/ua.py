import json
import os
import re
from typing import List

from random_user_agent.params import OperatingSystem, Popularity, SoftwareName
from random_user_agent.user_agent import UserAgent


def _extract_chrome_version(user_agent: str) -> int:
    version_pattern = r"Chrome/(\d{2})\."

    if match := re.search(version_pattern, user_agent):
        return int(match.group(1))
    return 0


def _filter_user_agents(user_agents_list: List[dict], min_version: int) -> List[dict]:
    user_agents = []

    for ua in user_agents_list:
        version = _extract_chrome_version(ua.get("user_agent", ""))
        if version >= min_version:
            ua["version"] = version
            user_agents.append(ua)

    return user_agents


def _get_user_agents_and_save_in_json_file(min_version) -> List[dict]:
    # Building a new file and return the user agents generated
    software_names = [SoftwareName.CHROME.value, SoftwareName.CHROMIUM.value]
    operating_systems = [
        OperatingSystem.WINDOWS.value,
        OperatingSystem.LINUX.value,
        OperatingSystem.MAC.value,
        OperatingSystem.MACOS.value,
        OperatingSystem.MAC_OS_X,
        OperatingSystem.UNIX.value,
        OperatingSystem.CHROMEOS.value,
    ]
    popularity = [Popularity.COMMON.value, Popularity.POPULAR.value]

    user_agent_rotator = UserAgent(
        software_names=software_names,
        operating_systems=operating_systems,
        popularity=popularity,
    )

    all_user_agents = user_agent_rotator.get_user_agents()
    user_agents = _filter_user_agents(all_user_agents, min_version)

    with open("./user_agents.json", "w") as outfile:
        json.dump(user_agents, outfile, indent=4)
    return user_agents


def _get_user_agents_from_json_file(min_version) -> List[dict]:
    with open("./user_agents.json", "r") as json_file:
        all_user_agents = json.load(json_file)
        return _filter_user_agents(all_user_agents, min_version)


def build_user_agents(min_version=55, cached=True) -> List[dict]:
    if cached and os.path.isfile("./user_agents.json"):
        return _get_user_agents_from_json_file(min_version)
    return _get_user_agents_and_save_in_json_file(min_version)
