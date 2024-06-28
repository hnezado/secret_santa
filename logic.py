# ONLY edit this file to implement new logic or change the existing one

import json
import logging as log
import random as r
from collections import OrderedDict


class Logic:
    def __init__(self):
        self.member_attrs = ["enabled", "name", "family_id", "adult", "exceptions"]
        self.members = []
        self.adults = {}
        self.children = {}

        self.read_members()
        self.parse_members()

    def read_members(self):
        """Reads and loads the data file"""
        
        with open("data/data.json") as f:
            self.members = json.load(f, object_pairs_hook=OrderedDict)

    def add_member(self, member):
        """Adds a new member to the data file"""
        
        self.members.append(member)
        self.save_data()

    def update_member(self, updated_member: object) -> None:
        """Edits an existing member data from the data file"""

        for i, member in enumerate(self.members):
            if member["name"] == updated_member.name:
                self.members[i] = updated_member
                break
        self.save_data()

    def del_member(self, member):
        """Deletes an existing member from the data file"""

        for i, m in enumerate(self.members):
            if m["name"] == member.name:
                del self.members[i]
                break
        self.save_data()

    def parse_members(self):
        """Parse the data into dictionaries of members"""

        self.adults = [member for member in self.members if member["age"] == "adult" and member["enabled"]]
        self.children = [member for member in self.members if member["age"] == "child" and member["enabled"]]

    def save_data(self):
        """Updates the json file"""

        with (open("data/data.json", "w") as f):
            json.dump(self.members, f, indent=2)

    def get_member(self, member_name):
        """Returns the full member dict by its name"""

        for member in self.members:
            if member["name"] == member_name:
                return member
        print(f"No member found by name {member_name}")

    def match_adults(self):
        """Matches randomly each adult with another adult avoiding exceptions (adult-adult)"""

        unmatched_adults = [m["name"] for m in self.adults]
        matches = {}
        for adult_name_1 in unmatched_adults[:]:
            adult_name_2 = r.choice(unmatched_adults)
            if adult_name_1 != adult_name_2:
                adult_1 = self.get_member(adult_name_1)
                adult_2 = self.get_member(adult_name_2)
                if adult_name_2 not in adult_1["exceptions"]:
                    if adult_1["family_id"] != adult_2["family_id"]:
                        if adult_name_2 in matches.keys():
                            if matches[adult_name_2] != adult_name_1:
                                unmatched_adults.remove(adult_name_2)
                                matches[adult_name_1] = adult_name_2
                        else:
                            unmatched_adults.remove(adult_name_2)
                            matches[adult_name_1] = adult_name_2
        if unmatched_adults:
            return self.match_adults()
        else:
            return matches

    def match_children(self):
        """Matches randomly each child with an adult (adult-child(ren))"""
        
        # Exception ("Alain" & "Fatiha" no related to any children)
        unmatched_adults = [m["name"] for m in self.adults if m["name"] not in ["Alain", "Fatiha"]]
        
        # unmatched_a = [a_name for a_name, adult in self.adults.items()]
        unmatched_children = [m["name"] for m in self.children]
        matches = {}
        for _ in range(len(unmatched_adults)):
            adult_name = r.choice(unmatched_adults)
            child_name = None
            try:
                child_name = r.choice(unmatched_children)
            except IndexError:
                log.warning(f'Children list is empty')
            if child_name:
                adult = self.get_member(adult_name)
                child = self.get_member(child_name)
                if child_name not in adult["exceptions"]:
                    if child["family_id"] != adult["family_id"]:
                        unmatched_adults.remove(adult_name)
                        unmatched_children.remove(child_name)
                        matches[adult_name] = child_name
        if unmatched_adults and unmatched_children:
            return self.match_children()
        else:
            if unmatched_adults:
                log.warning(f'Unmatched adults: {unmatched_adults}')
            elif unmatched_children:
                log.warning(f'Unmatched children: {unmatched_children}')
            return matches

    @staticmethod
    def merge_matches(m1, m2):
        """Merges both matches adults-adults and adults-children"""
        
        merge = {k: [] for k, _ in m1.items()}
        for k, _ in merge.items():
            try:
                merge[k].append(m1[k])
            except KeyError:
                log.info(f'No {k} in adults')
            try:
                merge[k].append(m2[k])
            except KeyError:
                log.info(f'No {k} in children')
        return merge

    def run(self):
        """Main logic"""
        
        matches_adults = self.match_adults()
        matches_children = self.match_children()
        matches = self.merge_matches(matches_adults, matches_children)
        return matches
