#!/usr/bin/env python3

import dataclasses
import re
import requests
import requests_cache
from bs4 import BeautifulSoup

import logging

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass
class LeaderboardEntry:
    name: str
    stars: int = 0
    points: int = 0
    completed: dict = dataclasses.field(default_factory=lambda: {})
    badges: list = dataclasses.field(default_factory=lambda: [])


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
            completions = {
                int(x): len(value["completion_day_level"][x])
                for x in value["completion_day_level"]
            }
            name = None
            if value["name"]:
                name = value["name"]
            else:
                name = f"(anonymous user #" + str(value["id"]) + ")"
            lb_entry = LeaderboardEntry(
                name=name,
                stars=value["stars"],
                points=value["local_score"],
                completed=completions,
            )
            leaderboard.append(lb_entry)
        return leaderboard

    def parse_global_leaderboard(self, text):
        soup = BeautifulSoup(text, "html.parser")
        rows = soup.find_all("div", {"class": "leaderboard-entry"})
        leaderboard = list()
        for row in rows:
            if not row:
                continue
            entries = [x for x in row.text.split(" ") if x != ""]
            entry = None
            badges = [x for x in entries if x == "(AoC++)" or x == "(Sponsor)"]
            if entries[0].endswith(")"):
                entry = LeaderboardEntry(
                    points=int(entries[1]),
                    name=" ".join(entries[2 : len(entries) - len(badges)]),
                    badges=badges,
                )
            else:
                entry = LeaderboardEntry(
                    points=int(entries[0]),
                    name=" ".join(entries[1 : len(entries) - len(badges)]),
                    badges=badges,
                )
            leaderboard.append(entry)
        return leaderboard

    def get_global_leaderboard(self, year):
        resp = self.aoc_session.get(f"{self.aoc_url}/{year}/leaderboard")
        leaderboard = self.parse_global_leaderboard(resp.text)
        return leaderboard

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
