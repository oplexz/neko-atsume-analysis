from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, Any


class GroupingStrategy(ABC):
    """Abstract base class defining the interface for grouping strategies."""

    playspace_to_group: Dict = None

    def __init__(self, playspace_to_item_id: Dict):
        self.playspace_to_item_id = playspace_to_item_id
        self.create_group_mapping()

    @abstractmethod
    def create_group_mapping(self) -> Dict:
        """Creates mapping from playspace IDs to group IDs."""
        pass

    def get_corresponding_group(self, playspace_id) -> Dict:
        """Creates mapping from playspace IDs to group IDs."""
        return self.playspace_to_group.get(playspace_id)

    @abstractmethod
    def apply_group_values(self, group_expected_values: Dict, items: Dict) -> None:
        """Applies group values to individual items."""
        pass


class PlayspaceGrouping(GroupingStrategy):
    """Strategy for grouping by playspace where each playspace is its own group."""

    def create_group_mapping(self) -> Dict:
        self.playspace_to_group = dict(
            zip(self.playspace_to_item_id.keys(), self.playspace_to_item_id.keys())
        )

    def apply_group_values(self, group_expected_values: Dict, items: Dict) -> None:
        for group_id, value in group_expected_values.items():
            items[self.playspace_to_item_id[group_id]] += value


class ItemGrouping(GroupingStrategy):
    """Strategy for grouping by item where items are grouped directly."""

    def create_group_mapping(self) -> Dict:
        self.playspace_to_group = self.playspace_to_item_id

    def apply_group_values(self, group_expected_values: Dict, items: Dict) -> None:
        for group_id, value in group_expected_values.items():
            # items[group_id] += value
            items[group_id] = value


class CustomGrouping(GroupingStrategy):
    """Strategy for custom binary grouping based on items of interest."""

    def __init__(
        self,
        playspace_to_item_id: Dict,
        items_of_interest_indoors,
        items_of_interest_outdoors,
    ):
        if items_of_interest_indoors is None:
            items_of_interest_indoors = []
        if items_of_interest_outdoors is None:
            items_of_interest_outdoors = []
        self.items_of_interest_indoors = items_of_interest_indoors
        self.items_of_interest_outdoors = items_of_interest_outdoors
        super().__init__(playspace_to_item_id)

    def create_group_mapping(self) -> Dict:
        mapping = {}
        for id in self.playspace_to_item_id.keys():
            item_id = self.playspace_to_item_id[id]
            if (
                item_id in self.items_of_interest_indoors
                or item_id in self.items_of_interest_outdoors
            ):
                mapping[id] = "Your Yard Total"
        self.playspace_to_group = mapping

    def get_is_indoors(self, playspace_id: int) -> bool:
        return self.playspace_to_item_id[playspace_id] in self.items_of_interest_indoors

    def get_is_indoors_item(self, item_id: int) -> bool:
        return item_id in self.items_of_interest_indoors

    def transform_to_item_group(self, same_cat_interaction_term_calc_space):
        new_same_cat_interaction_term_calc_space = defaultdict(
            lambda: defaultdict(list)
        )
        assert len(same_cat_interaction_term_calc_space) == 1
        for group_id, cat_dict in same_cat_interaction_term_calc_space.items():
            for cat_id, cat_data in cat_dict.items():
                appear_prob_per_playspace, silver_rate_per_playspace, playspace_ids = (
                    zip(*cat_data)
                )
                for p, s, playspace_id in zip(
                    appear_prob_per_playspace, silver_rate_per_playspace, playspace_ids
                ):
                    new_same_cat_interaction_term_calc_space[
                        self.playspace_to_item_id[playspace_id]
                    ][cat_id].append((p, s, playspace_id))

        return new_same_cat_interaction_term_calc_space

    def apply_group_values(
        self,
        group_expected_values_items: Dict,
        group_expected_values_overall: Dict,
        items: Dict,
    ) -> None:
        for group_id, value in group_expected_values_items.items():
            items[group_id] += value
        for group_id, value in group_expected_values_overall.items():
            items[group_id] += value


class GroupingFactory:
    """Factory class for creating appropriate grouping strategy."""

    @staticmethod
    def create_strategy(
        group_def: str,
        playspace_to_item_id: Dict = None,
        items_of_interest_indoors=None,
        items_of_interest_outdoors=None,
    ) -> GroupingStrategy:
        if group_def == "playspace":
            return PlayspaceGrouping(playspace_to_item_id)
        elif group_def == "item":
            return ItemGrouping(playspace_to_item_id)
        elif group_def == "custom":
            return CustomGrouping(
                playspace_to_item_id,
                items_of_interest_indoors,
                items_of_interest_outdoors,
            )
        else:
            raise ValueError(f"Unknown grouping strategy: {group_def}")
