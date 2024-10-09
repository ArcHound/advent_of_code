#!/usr/bin/env python3

import dataclasses
import re
import requests
import requests_cache
from bs4 import BeautifulSoup

import logging

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass
class PrivateLeaderboardEntry:
    name: str
    stars: int
    points: int
    completed: list


class AOC_Service:
    def __init__(self, aoc_token, aoc_url, proxy, proxies):
        requests_cache.install_cache(
            cache_name="advent_of_code_requests_cache",
            backend="sqlite",
            cache_control=True,
        )
        log.info("Init service session...")
        self.aoc_url = aoc_url
        self.aoc_session = requests.Session()
        self.aoc_session.cookies["session"] = aoc_token
        if proxy:
            log.info("Got proxy {} for service {}".format(proxies, "aoc"))
            self.aoc_session.proxies.update(proxies)
            self.aoc_session.verify = False

    def get_input(self, year, day):
        resp = self.aoc_session.get(f"{self.aoc_url}/{year}/day/{day}/input")
        return resp.text

    def parse_user(self, text):
        soup = BeautifulSoup(text, "html.parser")
        user = soup.find("div", {"class": "user"})
        return user.text

    def get_user(self):
        r = self.aoc_session.get(f"{self.aoc_url}/")
        user = self.parse_user(r.text)
        return user

    def parse_private_leaderboards(self, text):
        soup = BeautifulSoup(text, "html.parser")
        links = soup.find("article").find("div").find_all("a")
        return [l["href"].split("/")[-1] for l in links]

    def get_private_leaderboards(self):
        resp = self.aoc_session.get(f"{self.aoc_url}/leaderboard/private")
        leaderboards = self.parse_private_leaderboards(resp.text)
        return leaderboards

    def get_private_leaderboard(self, year, leaderboard_id):
        resp = self.aoc_session.get(
            f"{self.aoc_url}/{year}/leaderboard/private/view/{leaderboard_id}.json"
        ).json()
        leaderboard = list()
        for entry, value in resp.get("members", dict()).items():
            completions = [
                (int(x), len(value["completion_day_level"][x]))
                for x in value["completion_day_level"]
            ]
            lb_entry = PrivateLeaderboardEntry(
                name=value["name"],
                stars=value["stars"],
                points=value["local_score"],
                completed=completions,
            )
            leaderboard.append(lb_entry)
        return leaderboard

    def get_global_leaderboard(self, year):
        pass

    def parse_stars(self, text):
        pattern = "Your puzzle answer was"
        stars = len(re.findall(pattern, text))
        return stars

    def get_stars(self, year, day):
        log.info("Get stars")
        stars = 0
        headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
        resp = self.aoc_session.get(f"{self.aoc_url}/{year}/day/{day}", headers=headers)
        stars = self.parse_stars(resp.text)
        log.info(f"Got {stars} stars on this day")
        return stars

    def parse_solution_result(self, text):
        soup = BeautifulSoup(text, "html.parser")
        msg = soup.find("article").find("p").text
        success = False
        if msg.startswith("That's the right answer"):
            success = True
        return success, msg

    def send_solution(self, year, day, part, answer):
        resp = self.aoc_session.post(
            f"{self.aoc_url}/{year}/day/{day}/answer",
            data={"level": str(part), "answer": str(answer)},
        )
        success, msg = self.parse_solution_result(resp.text)
        return success, msg
