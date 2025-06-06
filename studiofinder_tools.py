from datetime import datetime
import json
from typing import Any, List

from agno.tools import Toolkit


class StudioFinderTools(Toolkit):
    """
    StudioFinderTools is a toolkit for searching StudioFinder easily.
    Args:
        search (bool): Enable StudioFinder search function.
    """

    def __init__(
        self,
        search: bool = True,
        **kwargs,
    ):
        tools: List[Any] = []
        if search:
            tools.append(self.studiofinder_get_locations)
            # tools.append(self.studiofinder_get_availability)
            tools.append(self.studiofinder_get_availability_in_range)

        super().__init__(name="studiofinder", tools=tools, **kwargs)

    def studiofinder_get_locations(self) -> str:
        """Use this function to get the locations from StudioFinder.

        Returns:
            A list of all place IDs found in the StudioFinder universe.
        """ 
        def get_place_ids(place: dict) -> List[str]:
            ids = [place["id"]]
            for subplace in place.get("places", []):
                ids.extend(get_place_ids(subplace))
            return ids

        all_ids = get_place_ids(self.get_universe())
        return json.dumps(all_ids, indent=2)

    def studiofinder_get_availability(self, id: str) -> str:
        """Use this function to get availability for a location.

        Args:
            id (str): The place ID to get availability for.

        Returns:
            A list of all available slots (start, end times) for the given place ID.
        """
        def get_slots(place: dict) -> List[dict]:
            slots = []
            # Add slots for current place if ID matches
            if place["id"] == id:
                slots.extend(place.get("slots", []))
            # Recursively check subplaces
            for subplace in place.get("places", []):
                slots.extend(get_slots(subplace))
            return slots

        universe = self.get_universe()
        all_slots = get_slots(universe)
        return json.dumps(all_slots, indent=2)


    def studiofinder_get_availability_in_range(self, id: str, start_date: str, end_date: str) -> str:
        """Use this function to get availability for a location.

        Args:
            id (str): The place ID to get availability for.
            start_date (str): The start date (ISO 8601) to get availability for. e.g. 2025-06-01T00:00:00Z
            end_date (str): The end date (ISO 8601) to get availability for. e.g. 2025-06-02T00:00:00Z

        Returns:
            A list of all available slots (start, end times) for the given place ID.
        """
        print("start_date", start_date)
        print("end_date", end_date)

        def get_slots(place: dict) -> List[dict]:
            slots = []
            # Add slots for current place if ID matches
            if place["id"] == id:
                for slot in place.get("slots", []):
                    slot_start = datetime.fromisoformat(slot["start"].replace('Z', '+00:00'))
                    start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    # print()
                    # print("slot_start", slot_start)
                    # print("start", start)
                    # print("end", end)
                    print()
                    if start <= slot_start <= end:
                        # print()
                        # print("slot_start is in range", slot_start)
                        # print()
                        slots.append(slot)
            # Recursively check subplaces
            for subplace in place.get("places", []):
                slots.extend(get_slots(subplace))
            return slots

        universe = self.get_universe()
        all_slots = get_slots(universe)
        return json.dumps(all_slots, indent=2)

    def get_universe(self):
        with open('./universe.json') as f:
            return json.load(f)
