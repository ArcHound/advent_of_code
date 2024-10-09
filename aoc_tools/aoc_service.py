#!/usr/bin/env python3

import re
import requests
import requests_cache
from bs4 import BeautifulSoup

import logging

log = logging.getLogger("aoc_logger")


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

    def parse_stars(self, text):
        pattern = "Your puzzle answer was"
        stars = len(re.findall(pattern, text))
        return stars

    def parse_solution_result(self, text):
        soup = BeautifulSoup(text, "html.parser")
        msg = soup.find("article").find("p").text
        success = False
        if msg.startswith("That's the right answer"):
            success = True
        return success, msg

    def get_stars(self, year, day):
        log.info("Get stars")
        stars = 0
        headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
        resp = self.aoc_session.get(f"{self.aoc_url}/{year}/day/{day}", headers=headers)
        stars = self.parse_stars(resp.text)
        log.info(f"Got {stars} stars on this day")
        return stars

    def send_solution(self, year, day, part, answer):
        resp = self.aoc_session.post(
            f"{self.aoc_url}/{year}/day/{day}/answer",
            data={"level": str(part), "answer": str(answer)},
        )
        success, msg = self.parse_solution_result(resp.text)
        return success, msg
