# ONLY edit this file to implement new logic or change the existing one

import json
import logging as log
import random as r
from collections import OrderedDict
from config import Member


class Logic:
    def __init__(self):
        self.member_attrs = ["enabled", "family_id", "name", "adult", "exceptions"]
        self.members_raw = None
        self.members_names = None
        self.members = None
        self.adults = None
        self.children = None

        self.read_members()
        self.parse_members()

    def read_members(self):
        """Reads and loads the config file"""
        
        with open("config.json") as f:
            self.members_raw = json.load(f, object_pairs_hook=OrderedDict)

    def add_member(self, member):
        """Adds a new member to the config file"""
        
        for attr in vars(member):
            self.members[attr] = member[attr]
        self.update_config_file()
        
    def del_member(self, member):
        """Deletes an existing member from the config file"""
        
        print(1, self.members)
        del self.members[member.name.lower()]
        self.update_config_file()
        print(2, self.members)

    def parse_members(self):
        """Parses the raw input into a dictionary with Member() objects"""

        self.members = OrderedDict()
        
        for name, attrs in self.members_raw.items():
            instance = "Member("
            for attr in attrs.keys():
                value = f'"{attrs[attr]}"' if type(attrs[attr]) == str else attrs[attr]
                instance = f'{instance}{value}, '
            instance = f'{instance[:-2]})'
            self.members[name] = eval(instance)
            
        self.adults = {name: member for name, member in self.members.items()
            if member.age == "adult" and member.enabled}
        self.children = {name: member for name, member in self.members.items() 
            if member.age == "child" and member.enabled}

    def update_config_file(self):
        """Updates the json file"""
        
        self.members_raw = OrderedDict()
        for k, member in self.members.items():
            self.members_raw[k] = OrderedDict()
            for attr in list(vars(member).keys()):
                self.members_raw[k][attr] = eval(f'member.{attr}')

        output = json.dumps(self.members_raw, indent=2)

        with open("config.json", "w") as f:
            f.write(output)

    def match_adults(self):
        """Matches randomly each adult with another adult avoiding exceptions (adult-adult)"""
        
        unmatched_a = list(self.adults.keys())
        matches = {}
        for a1 in list(self.adults.keys()):
            a2 = r.choice(unmatched_a)
            if a1 != a2:
                if a2 not in self.adults[a1].exceptions:
                    if self.adults[a1].family_id != self.adults[a2].family_id:
                        if a2 in matches.keys():
                            if matches[a2] != a1:
                                a2 = unmatched_a.pop(unmatched_a.index(a2))
                                matches[a1] = self.adults[a2]
                        else:
                            a2 = unmatched_a.pop(unmatched_a.index(a2))
                            matches[a1] = self.adults[a2]
        if unmatched_a:
            return self.match_adults()
        else:
            return matches

    def match_children(self):
        """Matches randomly each child with an adult (adult-child(ren))"""
        
        # Exception ("Alain" & "Fatiha" no related to any children)
        unmatched_a = [a_name for a_name, adult in self.adults.items() if adult.name not in ["Alain", "Fatiha"]]
        
        # unmatched_a = [a_name for a_name, adult in self.adults.items()]
        unmatched_c = list(self.children.keys())
        matches = {}
        for _ in range(len(unmatched_a)):
            a_name = r.choice(unmatched_a)
            c_name = None
            try:
                c_name = r.choice(unmatched_c)
            except IndexError:
                log.info(f'Children list is empty')
            if c_name:
                if c_name not in self.adults[a_name].exceptions:
                    if self.children[c_name].family_id != self.adults[a_name].family_id:
                        adult = unmatched_a.pop(unmatched_a.index(a_name))
                        child = unmatched_c.pop(unmatched_c.index(c_name))
                        matches[adult] = self.children[child]
        if unmatched_a and unmatched_c:
            return self.match_children()
        else:
            if unmatched_a:
                log.warning(f'Unmatched adults: {unmatched_a}')
            elif unmatched_c:
                log.warning(f'Unmatched children: {unmatched_c}')
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
        
        matches_a = self.match_adults()
        matches_c = self.match_children()
        matches = self.merge_matches(matches_a, matches_c)
        return matches
