import argparse
import itertools
import json
from functools import lru_cache
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Dict, List, Tuple

import numpy as np
import pandas as pd

from groups import GroupingFactory


# Constants
class GameConstants:
    MINUTES_PER_TICK = 5
    CAT_STAY_TICK_AVG = 9.5  # (5 + 14) / 2
    STAY_TICK_RANGE = list(range(5, 15))
    GOLD_FISH_ROUND_DOWN_FACTOR = (
        sum(map(lambda x: x // 2, STAY_TICK_RANGE)) / sum(STAY_TICK_RANGE) * 2
    )
    SILVER_FISH_MULTIPLIER_RANGE = (1, 1.5)
    SILVER_FISH_PER_GOLD_FISH = 25
    # Well you can buy things (remodeling) with silver fish, and hence the conversion rate
    GOLD_FISH_PER_SILVER_FISH = 1 / 50


class WeatherTypes:
    NONE = 0
    SPRING = 1
    SUMMER = 2
    AUTUMN = 4
    WINTER = 8
    SNOW = 16
    BURNING = 32
    ALL = 4294967295


# Data loading and preprocessing
class DataLoader:
    @staticmethod
    @lru_cache(maxsize=None)
    def load_json_data(filename: str) -> List[Dict]:
        with open(filename) as f:
            return json.load(f)

    @staticmethod
    @lru_cache(maxsize=None)
    def load_json_data_as_df(filename: str) -> pd.DataFrame:
        with open(filename) as f:
            data = json.load(f)
            return pd.DataFrame(data)

    @staticmethod
    def create_cat_vs_food_dict(data: List[Dict], food_type: int) -> Dict[int, float]:
        return {
            int(record["Id"]): record["Dict"].get(str(food_type), 0) for record in data
        }

    @staticmethod
    def create_cat_vs_cat_dict(data: List[Dict]) -> Dict[int, Dict]:
        return {int(record["Id"]): record["Dict"] for record in data}

    @staticmethod
    def create_playspace_weather_dict(
        data: List[Dict], weather: int
    ) -> Dict[int, float]:
        return {
            int(record["Id"]): record["Dict"].get(str(weather), 0) for record in data
        }

    @staticmethod
    def create_goodie_existence_set(data: List[Dict]) -> Dict[int, Dict]:
        return {int(record["Id"]) for record in data}


class ProbabilityCalculator:
    @staticmethod
    def expectation_of_uniform_rounded_down(a: float, b: float) -> float:
        a_frac = a - int(a)
        b_frac = b - int(b)
        return (a + b) / 2 - (int(b) - int(a) + b_frac**2 - a_frac**2) / (b - a) / 2

    @staticmethod
    def expectation_of_uniform_rounded_down_clipped(a: float, b: float) -> float:
        if b < 1:
            return 1
        if a < 1:
            return ((1 - a) / (b - a)) * 1 + (
                (b - 1) / (b - a)
            ) * ProbabilityCalculator.expectation_of_uniform_rounded_down(1, b)
        return ProbabilityCalculator.expectation_of_uniform_rounded_down(a, b)

    @staticmethod
    def remove_interactions(probs: List[float]) -> List[float]:
        probs_mul = itertools.accumulate(
            [1 - p for p in probs], lambda x, y: x * y, initial=1
        )
        return [p * next(probs_mul) for p in probs]


@dataclass
class MinCalculationUnit:
    item_id: int
    playspace_id: int
    cat_idx: int


@dataclass
class ConstraintGroup:
    # What is considered as a group
    entries: List[MinCalculationUnit]


@dataclass
class Constraint:
    # Each group of records in the groups is mutually exclusive
    groups: List[ConstraintGroup]


class NekoAtsumeAnalyzer:
    def __init__(self, args):
        self.args = args

        self.is_custom_grouping = self.args.group_def == "custom"

        self.outdoor_weather = None
        if self.args.group_def == "custom":
            if self.args.weather == WeatherTypes.SUMMER:
                self.outdoor_weather = WeatherTypes.BURNING
        else:
            if not self.args.is_indoor and self.args.weather == WeatherTypes.SUMMER:
                self.args.weather = WeatherTypes.BURNING

        self.initialize_data()

        self.grouping_strategy = GroupingFactory.create_strategy(
            self.args.group_def,
            playspace_to_item_id=self.playspace_mappings["item_id"],
            items_of_interest_indoors=self.args.items_of_interest_indoors,
            items_of_interest_outdoors=self.args.items_of_interest_outdoors,
        )

        # Structure: {item_id: {playspace_id: {...}}}
        self.all_data = defaultdict(dict)

        # Where are we assuming the same cat cannot appear at the same time?
        # Possible definition of a group: yard/cat/(per cat calcs)
        # Structure: {group_id: {cat_id: [(probability, silver_rate), ...]}}
        # We should migrate to the enumerate conflict method, but idk a good
        # update schema so it's staying
        self.same_cat_interaction_term_calc_space = defaultdict(
            lambda: defaultdict(list)
        )
        self.items = defaultdict(int)

    def access_key_of_cal_unit(self, cal_unit: MinCalculationUnit, key: str) -> any:
        return self.all_data[cal_unit.item_id][cal_unit.playspace_id][key][
            cal_unit.cat_idx
        ]

    def set_key_of_cal_unit(
        self, cal_unit: MinCalculationUnit, key: str, new_data: any
    ):
        self.all_data[cal_unit.item_id][cal_unit.playspace_id][key][
            cal_unit.cat_idx
        ] = new_data

    def initialize_data(self):
        # Load all necessary data
        self.item_to_name = DataLoader.load_json_data("data_inferred/item_to_name.json")
        self.item_to_size = DataLoader.load_json_data("data_inferred/item_to_size.json")
        self.cat_vs_food_indoor = DataLoader.create_cat_vs_food_dict(
            DataLoader.load_json_data("NekoAtsume2Data/tables/CatVsFoodTable.json"),
            self.args.food_type_indoor,
        )
        self.cat_vs_food_outdoor = DataLoader.create_cat_vs_food_dict(
            DataLoader.load_json_data("NekoAtsume2Data/tables/CatVsFoodTable.json"),
            self.args.food_type_outdoor,
        )
        self.cat_vs_cat_all = DataLoader.create_cat_vs_cat_dict(
            DataLoader.load_json_data("NekoAtsume2Data/tables/CatVsCatTable.json")
        )
        self.playspace_to_weather_mul = DataLoader.create_playspace_weather_dict(
            DataLoader.load_json_data(
                "NekoAtsume2Data/tables/PlaySpaceVsWeatherTable.json"
            ),
            self.args.weather,
        )
        self.item_existence_set = DataLoader.create_goodie_existence_set(
            DataLoader.load_json_data("NekoAtsume2Data/tables/GoodsRecordTable.json")
        )

        if self.outdoor_weather:
            self.additional_playspace_to_weather_mul = (
                DataLoader.create_playspace_weather_dict(
                    DataLoader.load_json_data(
                        "NekoAtsume2Data/tables/PlaySpaceVsWeatherTable.json"
                    ),
                    self.outdoor_weather,
                )
            )

        df_cats = DataLoader.load_json_data_as_df(
            "NekoAtsume2Data/tables/CatRecordTable.json"
        )
        self.cat_to_silver_mul = dict(zip(df_cats["Id"], df_cats["Niboshi"]))
        self.cat_to_weather_impact = dict(zip(df_cats["Id"], df_cats["WeatherImpact"]))

        df_playspace = DataLoader.load_json_data_as_df(
            "NekoAtsume2Data/tables/PlaySpaceRecordTable.json"
        )
        self.playspace_mappings = {
            "silver_mul": dict(zip(df_playspace["Id"], df_playspace["Niboshi"])),
            "item_id": dict(zip(df_playspace["Id"], df_playspace["ItemId"])),
            "charm": dict(zip(df_playspace["Id"], df_playspace["Charm"])),
            "conflicted_idxs": dict(
                zip(df_playspace["Id"], df_playspace["ConflictIndices"].fillna(""))
            ),
        }

    def calculate_per_cat_stay_rate(self):
        """Calculate stay rate for each cat. Converts cat visit probabilities
        to stay rates."""
        for item_id, playspace_dict in self.all_data.items():
            for playspace_id, data in playspace_dict.items():
                cat_ids = data["cat_ids"]
                draw_weights = data["draw_weights"]
                cat_visit_prob_permyriad = data["cat_visit_prob_permyriad"]
                # Calculated in `calculate_cat_on_cat_interactions`
                cat_on_cat_interactions = data.get(
                    "cat_on_cat_interactions", np.full(len(cat_ids), 100)
                )

                interacted_draw_weights = draw_weights * cat_on_cat_interactions / 100
                draw_probability = (
                    interacted_draw_weights / interacted_draw_weights.sum()
                )
                per_cat_visit_prob = draw_probability * cat_visit_prob_permyriad

                playspace_visit_prob = per_cat_visit_prob.sum()

                if playspace_visit_prob == 0:
                    data["per_cat_visit_prob"] = per_cat_visit_prob / 10000
                    data["per_cat_stay_rate"] = np.zeros(len(cat_ids))
                    continue

                per_cat_visit_prob_given_visit = (
                    per_cat_visit_prob / playspace_visit_prob
                )

                # Assume the spot is only for one cat, what is the percentage of time it
                # will be filled for each cat. There are two states, the cat is there or
                # not there, and consider (not appear, appear) as a cycle. When the cat is
                # not there, there is a p chance that the cat will appear. Therefore, the
                # time the cat is not there is geometrically distributed with a mean of
                # 1/p - 1
                playspace_cat_stay_rate = GameConstants.CAT_STAY_TICK_AVG / (
                    10000 / playspace_visit_prob - 1 + GameConstants.CAT_STAY_TICK_AVG
                )

                data["per_cat_visit_prob"] = per_cat_visit_prob / 10000
                data["per_cat_stay_rate"] = (
                    playspace_cat_stay_rate * per_cat_visit_prob_given_visit
                )

    def enumerate_item_conflict_idx_constraint(self):
        """Calculate interactions between conflicting item indices."""
        all_data = self.all_data
        conflicts = []
        for item_id, playspace_dict in all_data.items():
            conflicting_groups = defaultdict(set)
            for this_playspace_id, data in playspace_dict.items():
                conflicting_idxs = tuple(data["conflicted_idxs"])
                if not conflicting_idxs:
                    continue
                conflicting_groups[conflicting_idxs].add(this_playspace_id)

            if not conflicting_groups:
                continue

            processed_conflict_keys = set()
            for this_key, this_playspace_ids in conflicting_groups.items():
                if this_key in processed_conflict_keys:
                    continue
                other_playspace_ids = set(
                    [int(str(item_id) + str(idx)) for idx in this_key]
                )
                # Can't do two groups in the current implementation yet. Needs
                # probably iteratively updating the amount of time spent
                # waiting for the conflicting groups
                if len(other_playspace_ids) > 1:
                    continue
                processed_conflict_keys.add(this_key)
                for other_key, possible_playspace_ids in conflicting_groups.items():
                    # if other_playspace_ids == possible_playspace_ids:
                    # >= here cuz Sebas is hardcoded to appear after Sapphire appears
                    if other_playspace_ids >= possible_playspace_ids:
                        if other_playspace_ids > possible_playspace_ids:
                            other_playspace_ids = possible_playspace_ids
                        processed_conflict_keys.add(other_key)
                        group_1, group_2 = [], []
                        for playspace_id in this_playspace_ids:
                            for cat_idx in range(
                                len(playspace_dict[playspace_id]["cat_ids"])
                            ):
                                group_1.append(
                                    MinCalculationUnit(item_id, playspace_id, cat_idx)
                                )
                        for playspace_id in other_playspace_ids:
                            for cat_idx in range(
                                len(playspace_dict[playspace_id]["cat_ids"])
                            ):
                                group_2.append(
                                    MinCalculationUnit(item_id, playspace_id, cat_idx)
                                )
                        conflicts.append(
                            Constraint(
                                [ConstraintGroup(group_1), ConstraintGroup(group_2)]
                            )
                        )
        return conflicts

    def calculate_cat_on_cat_interactions(self):
        """Calculate interactions between cats."""
        for item_id, playspace_dict in self.all_data.items():
            for playspace_id, data in playspace_dict.items():
                cat_ids = data["cat_ids"]
                cat_on_cat_interactions = [100 for _ in cat_ids]

                for other_playspace_id, other_data in playspace_dict.items():
                    if other_playspace_id == playspace_id:
                        continue

                    other_cat_ids = other_data["cat_ids"]
                    other_per_cat_stay_rate = other_data["per_cat_stay_rate"]
                    other_cat_ids_to_cat_stay_rate = dict(
                        zip(other_cat_ids, other_per_cat_stay_rate)
                    )

                    for idx, cat_id in enumerate(cat_ids):
                        cat_vs_cat = self.cat_vs_cat_all[cat_id]
                        for other_cat_id in other_cat_ids:
                            cat_on_cat_interactions[
                                idx
                            ] += other_cat_ids_to_cat_stay_rate[
                                other_cat_id
                            ] * cat_vs_cat.get(
                                str(other_cat_id), 0
                            )

                # Technically, the clipping should directly affect the interaction
                # score as averaging make it much harder to do stuff, but alas
                cat_on_cat_interactions = np.clip(cat_on_cat_interactions, 30, 400)
                data["cat_on_cat_interactions"] = cat_on_cat_interactions

    def calculate_non_interactive_variables(self):
        data = DataLoader.load_json_data(
            "NekoAtsume2Data/tables/PlaySpaceVsCatTable.json"
        )

        for record in data:
            playspace_id = record["Id"]
            if "Dict" not in record or not record["Dict"]:
                continue

            if (
                self.is_custom_grouping
                and self.grouping_strategy.get_corresponding_group(playspace_id) is None
            ):
                continue

            cat_ids, weights = zip(*record["Dict"].items())
            cat_ids = [int(cat_id) for cat_id in cat_ids]
            draw_weights = np.array(
                [
                    (
                        w[self.args.item_damage_state]
                        if len(w) > self.args.item_damage_state
                        else w[-1]
                    )
                    for w in weights
                ]
            )

            if sum(draw_weights) == 0:
                continue

            multiplier_cats = np.array(
                [self.cat_to_silver_mul[cat_id] for cat_id in cat_ids]
            )
            multiplier_goodies = self.playspace_mappings["silver_mul"][playspace_id]
            is_indoor = (
                self.grouping_strategy.get_is_indoors(playspace_id)
                if self.is_custom_grouping
                else self.args.is_indoor
            )
            cat_vs_food = (
                self.cat_vs_food_indoor if is_indoor else self.cat_vs_food_outdoor
            )
            cat_visit_prob_by_food = np.array(
                [cat_vs_food[cat_id] for cat_id in cat_ids]
            )
            multiplier_goodie_charms = self.playspace_mappings["charm"][playspace_id]
            multiplier_weather_by_playspace_delta = self.playspace_to_weather_mul.get(
                playspace_id, 0
            )

            if self.is_custom_grouping and self.outdoor_weather and is_indoor:
                multiplier_weather_by_playspace_delta = (
                    self.additional_playspace_to_weather_mul[playspace_id]
                )

            multiplier_cat_weather_impact = np.array(
                [self.cat_to_weather_impact[cat_id] for cat_id in cat_ids]
            )

            # Calculate cat visit probabilities before interactions
            cat_visit_prob_permyriad = (
                cat_visit_prob_by_food
                * multiplier_goodie_charms
                * (
                    (
                        multiplier_weather_by_playspace_delta
                        * (multiplier_cat_weather_impact / 100)
                        + 100
                    )
                    / 100
                )
            )

            #
            # Silver rate Calculation
            #

            # Calculate cat silver rate without round down nor random multiplier
            per_cat_silver_rate_prior_multiplier = (
                multiplier_cats * multiplier_goodies / 100 / 250
            )

            per_cat_expected_silver_per_collection = np.array(
                [
                    sum(
                        [
                            ProbabilityCalculator.expectation_of_uniform_rounded_down_clipped(
                                r * t * GameConstants.SILVER_FISH_MULTIPLIER_RANGE[0],
                                r * t * GameConstants.SILVER_FISH_MULTIPLIER_RANGE[1],
                            )
                            for t in GameConstants.STAY_TICK_RANGE
                        ]
                    )
                    / len(GameConstants.STAY_TICK_RANGE)
                    for r in per_cat_silver_rate_prior_multiplier
                ]
            )

            per_cat_silver_rate = (
                per_cat_expected_silver_per_collection / GameConstants.CAT_STAY_TICK_AVG
            )

            # Store calculated values
            item_id = self.playspace_mappings["item_id"][playspace_id]
            self.all_data[item_id][playspace_id] = {
                "cat_ids": cat_ids,
                "draw_weights": draw_weights,
                "cat_visit_prob_permyriad": cat_visit_prob_permyriad,
                "per_cat_silver_rate": per_cat_silver_rate,
                "conflicted_idxs": self.playspace_mappings["conflicted_idxs"][
                    playspace_id
                ],
            }

    def enumerate_constraints(self):
        constraints: List[Constraint] = []
        constraints += self.enumerate_item_conflict_idx_constraint()
        # # would be nice if someone can do this in place of what is done
        # constraints += self.enumerate_same_cat_constraint()
        self.constraints = constraints

    # Half finished. Can only handle constraints on a playspace level
    def resolve_constraints(self):
        playspace_id_to_item_id = self.playspace_mappings["item_id"]
        constraints = self.constraints
        for constraint in constraints:
            # Let me assume all entries from a group belong to the same
            # playspace
            visit_probs_orig = []

            for group in constraint.groups:
                group_playspace_visit_probs = []
                entries_grouped_by_playspace: Dict[int, List[MinCalculationUnit]] = (
                    defaultdict(list)
                )
                for entry in group.entries:
                    entries_grouped_by_playspace[entry.playspace_id].append(entry)

                # Initially the code is designed to calculate at the cat level for the same cat constraint, but ig im no longer doing that
                for playspace_id, entries in entries_grouped_by_playspace.items():
                    playspace_visit_prob = 0
                    for entry in entries:
                        playspace_visit_prob += self.access_key_of_cal_unit(
                            entry, "per_cat_visit_prob"
                        )
                    group_playspace_visit_probs.append(playspace_visit_prob)
                group_playspace_visit_probs = np.array(group_playspace_visit_probs)

                # placespaces in a group are not mutually exclusive
                group_visit_prob = 1 - np.prod(1 - group_playspace_visit_probs)
                visit_probs_orig.append(group_visit_prob)

            adjusted_visit_probs = np.array(
                ProbabilityCalculator.remove_interactions(visit_probs_orig)
            )
            adjusted_visit_probs_sum = adjusted_visit_probs.sum()
            new_stay_rates = (
                GameConstants.CAT_STAY_TICK_AVG
                / (1 / adjusted_visit_probs_sum - 1 + GameConstants.CAT_STAY_TICK_AVG)
                * adjusted_visit_probs
                / adjusted_visit_probs_sum
            )

            # Note: this is only operating for the entire playspace, not
            # individual. Idk how to update individual cat weight and ive
            # already spent too much time on this. The following code just puts
            # stuff back
            for group, new_stay_rate in zip(constraint.groups, new_stay_rates):
                group_playspace_visit_probs = []
                entries_grouped_by_playspace: Dict[int, List[MinCalculationUnit]] = (
                    defaultdict(list)
                )
                for entry in group.entries:
                    entries_grouped_by_playspace[entry.playspace_id].append(entry)

                playspace_orig_stay_rates = []
                for playspace_id, entries in entries_grouped_by_playspace.items():
                    playspace_data = self.all_data[
                        playspace_id_to_item_id[playspace_id]
                    ][playspace_id]
                    playspace_orig_stay_rates.append(
                        playspace_data["per_cat_stay_rate"].sum()
                    )
                playspace_orig_stay_rates = np.array(playspace_orig_stay_rates)
                if playspace_orig_stay_rates.sum() == 0:
                    continue
                adjusted_playspace_stay_rates = (
                    playspace_orig_stay_rates
                    / playspace_orig_stay_rates.sum()
                    * new_stay_rate
                )
                for (playspace_id, entries), adjusted_playspace_stay_rate in zip(
                    entries_grouped_by_playspace.items(), adjusted_playspace_stay_rates
                ):
                    playspace_data = self.all_data[
                        playspace_id_to_item_id[playspace_id]
                    ][playspace_id]
                    per_cat_visit_prob = playspace_data["per_cat_visit_prob"]
                    if per_cat_visit_prob.sum() == 0:
                        continue
                    playspace_data["per_cat_stay_rate"] = (
                        per_cat_visit_prob
                        / per_cat_visit_prob.sum()
                        * adjusted_playspace_stay_rate
                    )

    def resolve_interactions(self):
        self.calculate_per_cat_stay_rate()
        self.resolve_constraints()
        for _ in range(self.args.num_iterations_for_cat_on_cat):
            self.calculate_cat_on_cat_interactions()
            self.calculate_per_cat_stay_rate()
            self.resolve_constraints()

    # Legacy code, but i don't have a good way to update the logic so it's
    # staying
    def restructure_all_data_to_same_cat_interaction_group(self):
        """Calculate all interactions and populate interaction spaces."""
        for (
            item_id,
            playspace_dict,
        ) in self.all_data.items():
            for playspace_id, data in playspace_dict.items():
                cat_ids = data["cat_ids"]
                per_cat_stay_rate = data["per_cat_stay_rate"]
                per_cat_silver_rate = data["per_cat_silver_rate"]

                for cat_id, w, s in zip(
                    cat_ids, per_cat_stay_rate, per_cat_silver_rate
                ):
                    group_id = self.grouping_strategy.get_corresponding_group(
                        playspace_id
                    )
                    self.same_cat_interaction_term_calc_space[group_id][cat_id].append(
                        [w, s, playspace_id]
                    )

    def calculate_same_cat_interactions(self):
        for group_id, cat_dict in self.same_cat_interaction_term_calc_space.items():
            for cat_id, cat_data in cat_dict.items():
                appear_prob_per_playspace, silver_rate_per_playspace, playspace_ids = (
                    zip(*cat_data)
                )
                appear_prob_per_playspace = np.array(appear_prob_per_playspace)

                if sum(appear_prob_per_playspace) == 0:
                    continue

                mutually_exclusive_appear_prob_per_playspace = np.array(
                    ProbabilityCalculator.remove_interactions(appear_prob_per_playspace)
                )

                for record, p in zip(
                    cat_data, mutually_exclusive_appear_prob_per_playspace
                ):
                    record[0] = p

    def generate_results(self):
        group_expected_values = defaultdict(float)

        for group_id, cat_dict in self.same_cat_interaction_term_calc_space.items():
            for cat_id, cat_data in cat_dict.items():
                (
                    mutually_exclusive_appear_prob_per_playspace,
                    silver_rate_per_playspace,
                    playspace_ids,
                ) = zip(*cat_data)

                mutually_exclusive_appear_prob_per_playspace = np.array(
                    mutually_exclusive_appear_prob_per_playspace
                )
                silver_rate_per_playspace = np.array(silver_rate_per_playspace)
                stay_rate_per_tick = mutually_exclusive_appear_prob_per_playspace.sum()

                if sum(mutually_exclusive_appear_prob_per_playspace) == 0:
                    continue

                # Calculate rates and values
                appear_prob_per_playspace_given_appear = (
                    mutually_exclusive_appear_prob_per_playspace / stay_rate_per_tick
                )
                silver_rate_per_tick_given_stay_and_converted = (
                    appear_prob_per_playspace_given_appear * silver_rate_per_playspace
                ).sum()

                if self.is_custom_grouping:
                    is_indoor = np.array(
                        list(map(self.grouping_strategy.get_is_indoors, playspace_ids))
                    )
                    gold_conversion = np.where(is_indoor, 0.08, 0.04)
                    gold_conversion = (
                        gold_conversion * appear_prob_per_playspace_given_appear
                    ).sum()
                else:
                    gold_conversion = 0.08 if self.args.is_indoor else 0.04

                gold_rate_per_tick_given_stay_and_converted = (
                    0.5 * GameConstants.GOLD_FISH_ROUND_DOWN_FACTOR
                )

                # Calculate final values based on output unit
                total_ticks = (
                    self.args.total_duration_minutes / GameConstants.MINUTES_PER_TICK
                )

                if self.args.output_type == "silver":
                    expected_value = (
                        stay_rate_per_tick
                        * (1 - gold_conversion)
                        * silver_rate_per_tick_given_stay_and_converted
                        * total_ticks
                    )
                elif self.args.output_type == "gold":
                    expected_value = (
                        stay_rate_per_tick
                        * gold_conversion
                        * gold_rate_per_tick_given_stay_and_converted
                        * total_ticks
                    )
                elif self.args.output_type == "silver_equiv":
                    silver_equiv_rate_per_tick = (
                        gold_conversion
                        * gold_rate_per_tick_given_stay_and_converted
                        * GameConstants.SILVER_FISH_PER_GOLD_FISH
                        + (1 - gold_conversion)
                        * silver_rate_per_tick_given_stay_and_converted
                    )
                    expected_value = (
                        stay_rate_per_tick * silver_equiv_rate_per_tick * total_ticks
                    )
                elif self.args.output_type == "gold_equiv":
                    gold_equiv_rate_per_tick = (
                        gold_conversion * gold_rate_per_tick_given_stay_and_converted
                        + (1 - gold_conversion)
                        * silver_rate_per_tick_given_stay_and_converted
                        * GameConstants.GOLD_FISH_PER_SILVER_FISH
                    )
                    expected_value = (
                        stay_rate_per_tick * gold_equiv_rate_per_tick * total_ticks
                    )
                elif self.args.output_type == "cat_probability":
                    if cat_id in self.args.cat_id:
                        expected_value = stay_rate_per_tick
                    else:
                        expected_value = 0
                elif self.args.output_type == "stay_rate":
                    expected_value = stay_rate_per_tick
                else:
                    expected_value = None

                group_expected_values[group_id] += expected_value

        return group_expected_values

    def analyze(self):
        """Main analysis method."""
        self.calculate_non_interactive_variables()
        self.enumerate_constraints()
        self.resolve_interactions()
        self.restructure_all_data_to_same_cat_interaction_group()
        self.calculate_same_cat_interactions()
        if self.is_custom_grouping:
            # Results for the entire yard
            results_overall = self.generate_results()
            self.same_cat_interaction_term_calc_space = (
                self.grouping_strategy.transform_to_item_group(
                    self.same_cat_interaction_term_calc_space
                )
            )
            # Results for each item
            results_per_item = self.generate_results()
            self.grouping_strategy.apply_group_values(
                results_per_item, results_overall, self.items
            )
        else:
            results = self.generate_results()
            self.grouping_strategy.apply_group_values(results, self.items)
        return self.items


def main():
    parser = argparse.ArgumentParser(description="Neko Atsume Analysis")
    parser.add_argument(
        "--food_type",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 99],
        help="Type of food to place: 1=Thrifty Bitz, 2=Frisky Bitz, 3=Ritzy Bitz, 4=Bonito Bitz, 5=Deluxe Tuna Bitz, 6=Sashimi, 7=Sashimi Boat, 99=idk",
    )
    parser.add_argument(
        "--food_type_indoor",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 99],
        help="Type of food to place indoor: 1=Thrifty Bitz, 2=Frisky Bitz, 3=Ritzy Bitz, 4=Bonito Bitz, 5=Deluxe Tuna Bitz, 6=Sashimi, 7=Sashimi Boat, 99=idk",
    )
    parser.add_argument(
        "--food_type_outdoor",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 99],
        help="Type of food to place outdoor: 1=Thrifty Bitz, 2=Frisky Bitz, 3=Ritzy Bitz, 4=Bonito Bitz, 5=Deluxe Tuna Bitz, 6=Sashimi, 7=Sashimi Boat, 99=idk",
    )
    parser.add_argument(
        "--item_damage_state",
        type=int,
        default=0,
        choices=[0, 1, 2],
        help="State of item damage: 0=Good, 1=Broken, 2=Fixed",
    )
    parser.add_argument(
        "--weather",
        type=int,
        default=0,
        choices=[0, 1, 2, 4, 8, 16, 32],
        help="Weather condition (0=None, other values represent different weather types)",
    )
    parser.add_argument(
        "--is_indoor",
        action="store_true",
        help="If set, considers the yard as an indoor space. Ignored when group_def is 'custom'",
    )
    parser.add_argument(
        "--output_type",
        type=str,
        choices=[
            "silver",
            "gold",
            "silver_equiv",
            "gold_equiv",
            "cat_probability",
            "stay_rate",
        ],
        default="gold_equiv",
        help="Type of output to generate. For 'cat_probability', shows the probability (0-1) of a specific cat appearing. Other options show the expected value in the selected unit over the specified total_duration_minutes",
    )
    parser.add_argument(
        "--total_duration_minutes",
        type=int,
        default=24 * 60,
        help="Duration in minutes over which to aggregate the selected output_type. Ignored when output_type is 'cat_probability'",
    )
    parser.add_argument(
        "--cat_id",
        type=int,
        nargs="+",
        help="ID(s) of the specific cat to analyze when output_type is 'cat_probability'",
    )
    parser.add_argument(
        "--group_def",
        type=str,
        choices=["playspace", "item", "custom"],
        default="item",
        help="Defines how to group items where a single cat cannot appear simultaneously. Flawed implementation. 'playspace'=individual seats within items, 'item'=entire goodie, 'custom'=user-defined groups via items_of_interest arguments",
    )
    parser.add_argument(
        "--items_of_interest_indoors",
        type=int,
        nargs="+",
        help="List of goodie IDs to analyze as indoor items. Only used when group_def is 'custom'",
    )
    parser.add_argument(
        "--items_of_interest_outdoors",
        type=int,
        nargs="+",
        help="List of goodie IDs to analyze as outdoor items. Only used when group_def is 'custom'",
    )
    parser.add_argument(
        "--num_iterations_for_cat_on_cat",
        type=int,
        default=10,
        help="Number of iterations to simulate cat-on-cat interactions",
    )
    parser.add_argument(
        "--filter_by_na2",
        action="store_true",
        help="Filter results to only include items that are in the NA2",
    )

    args = parser.parse_args()
    if (
        args.food_type is None
        and args.food_type_indoor is None
        and args.food_type_outdoor is None
    ):
        args.food_type_indoor = 2
        args.food_type_outdoor = 2
    elif (
        args.food_type is not None
        and args.food_type_indoor is None
        and args.food_type_outdoor is None
    ):
        args.food_type_indoor = args.food_type
        args.food_type_outdoor = args.food_type
    elif args.food_type_indoor is not None and args.food_type_outdoor is not None:
        pass
    else:
        raise ValueError(
            "Invalid food type arguments, either provide --food_type OR both --food_type_indoor --food_type_outdoor)"
        )

    analyzer = NekoAtsumeAnalyzer(args)
    results = analyzer.analyze()

    # Output results
    sorted_items = sorted(results.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(sorted_items, columns=["GoodId", "Value"])
    df["Name"] = df["GoodId"].map(lambda x: analyzer.item_to_name.get(str(x), "-"))
    df["Is Large"] = df["GoodId"].map(lambda x: analyzer.item_to_size.get(str(x), "-"))
    df["Is in NA2"] = df["GoodId"].map(
        lambda x: "Yes" if x in analyzer.item_existence_set else "-"
    )
    df.rename(columns={"GoodId": "Goodie Id"}, inplace=True)
    if analyzer.is_custom_grouping:
        df["Is Indoor"] = df["Goodie Id"].map(
            lambda x: (
                analyzer.grouping_strategy.get_is_indoors_item(x)
                if type(x) == int
                else "-"
            )
        )
        df = df[["Goodie Id", "Name", "Is Large", "Is Indoor", "Is in NA2", "Value"]]
    else:
        df = df[["Goodie Id", "Name", "Is Large", "Is in NA2", "Value"]]
    if args.filter_by_na2:
        df = df.loc[df["Is in NA2"] == "Yes"]
        df = df.drop(columns=["Is in NA2"])
    data = df.to_markdown(tablefmt="github", index=False)
    with open("output.md", "w") as f:
        content = args.__repr__()
        f.write("#### Args\n")
        f.write(content)
        f.write("\n\n#### Results\n")
        f.write(data)
    print(data)


if __name__ == "__main__":
    main()
