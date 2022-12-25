from typing import List
import re
from copy import deepcopy
from math import ceil, prod
from time import time


class Run:
    def __init__(self, blueprint: List[List[int]], minutes: int):
        self.blueprint = blueprint
        self.resources: List[int] = [0, 0, 0, 0]
        self.bots: List[int] = [1, 0, 0, 0]
        self.minutes = minutes

    def pass_minutes(self, amount: int):
        for i, bot_count in enumerate(self.bots):
            self.resources[i] += bot_count * amount
        self.minutes -= amount

    def get_branches(self) -> List:
        branches = []
        for bot in range(4):
            minutes = self.minutes_needed(bot)
            if self.should_build_bot(bot) and minutes != -1 \
                    and minutes <= self.minutes:
                new_run = deepcopy(self)
                if minutes > 0:
                    new_run.pass_minutes(minutes)
                new_run.pass_minutes(1)
                new_run.build_bot(bot)
                branches.append(new_run)
        return branches

    def should_build_bot(self, bot: int) -> bool:
        # should build bot if amount X of bots of type R is lower
        #   than the max amount of resources of type R needed to build any bot
        # or if bot_type == geode
        # but should not build if bot_type == ore and won't be profitable
        return bot == 3 or ((
            self.bots[bot] < max(
                [costs[bot] for costs in self.blueprint]
            ) and
            (bot != 0 or self.minutes-1 > self.blueprint[0][0]))
        )

    def minutes_needed(self, bot: int) -> int:
        minutes_per_ressource = []
        for cost, bot_count, ressource_count in zip(
            self.blueprint[bot], self.bots, self.resources
        ):
            if cost > 0 and bot_count == 0:
                return -1
            if bot_count != 0:
                minutes_per_ressource.append(
                    ceil((cost - ressource_count) / bot_count)
                )
        return max(minutes_per_ressource)

    def build_bot(self, bot: int):
        for i, cost in enumerate(self.blueprint[bot]):
            self.resources[i] -= cost
        self.bots[bot] += 1

    def repr_str(self) -> str:
        return f"Bots: {self.bots}, Resources: {self.resources}"


def main():
    with open("input.txt") as f:
        blueprints = [parse_blueprint(line.strip())
                      for line in f.readlines()]

    # #### Puzzle 1 #### #

    start_time = time()
    max_geodes_counts = [find_max_geodes_count(bp, 24) for bp in blueprints]
    print("Sum of quality levels:",
          sum([(i+1)*gc for i, gc in enumerate(max_geodes_counts)]))
    print(f"Total seconds taken: {time() - start_time:.2f}\n")

    # #### Puzzle 2 #### #

    start_time = time()
    max_geodes_counts = [find_max_geodes_count(bp, 32, 2)
                         for bp in blueprints[:3]]
    print("Product of highest geode counts:", prod(max_geodes_counts))
    print(f"Total seconds taken: {time() - start_time:.2f}")


def parse_blueprint(blueprint_str: str) -> List[List[int]]:
    patterns = [f"Each {bot_type} robot costs ([^.]+)\\."
                for bot_type in ["ore", "clay", "obsidian", "geode"]]
    costs = []
    for pattern in patterns:
        bot_costs = [0 for _ in range(4)]
        cost_strs = re.search(pattern, blueprint_str)\
            .groups()[0].split(" and ")
        for cost_str in cost_strs:
            cost_i = 0 if cost_str.endswith("ore")\
                else 1 if cost_str.endswith("clay") else 2
            bot_costs[cost_i] = int(cost_str.split(" ")[0])
        costs.append(bot_costs)
    return costs


def find_max_geodes_count(blueprint: List[List[int]], minutes: int,
                          verbosity: int = 0) -> int:
    start_time = time()
    start = Run(blueprint, minutes)
    runs = [start]
    highest_geode_count = 0
    while len(runs) != 0:
        run = runs.pop()
        branches = run.get_branches() if run.minutes > 1 else None
        if not branches:
            run.pass_minutes(run.minutes)
            geode_count = run.resources[3]
            if geode_count > highest_geode_count:
                highest_geode_count = geode_count
        else:
            runs += branches
    if verbosity >= 1:
        print("Highest geode count:", highest_geode_count)
    if verbosity >= 2:
        print(f"Seconds taken to find: {time() - start_time:.2f}")
    return highest_geode_count


if __name__ == "__main__":
    main()
