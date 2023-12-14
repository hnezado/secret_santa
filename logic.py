# ONLY edit this file to implement new logic or change the existing one

import json
import logging as log
import random as r
from collections import OrderedDict
from config import Member


class Logic:
    def __init__(self):
        self.participants_raw = None
        self.participants_names = None
        self.participants = None
        self.adults = None
        self.children = None

        self.read_participants()
        self.parse_participants()

    def read_participants(self):
        """Reads and loads the input file"""
        
        with open("config.json") as f:
            self.participants_raw = json.load(f, object_pairs_hook=OrderedDict)

    def parse_participants(self):
        """Parses the raw input into a dictionary with Member() objects"""

        self.participants = OrderedDict()
        for k, v in self.participants_raw.items():
            instance = "Member("
            for attr in v.keys():
                value = f'"{v[attr]}"' if type(v[attr]) == str else v[attr]
                instance = f'{instance}{attr}={value}, '
            instance = f'{instance[:-2]})'
            self.participants[k] = eval(instance)
        self.adults = {name: member for name, member in self.participants.items()
            if member.age == "adult" and member.enabled}
        self.children = {name: member for name, member in self.participants.items() 
            if member.age == "child" and member.enabled}

    def update_config_file(self):
        """Updates the json file"""
        
        for k, member in self.participants.items():
            attrs = list(member.__dict__.keys())
            for attr in attrs:
                self.participants_raw[k][attr] = eval(f'member.{attr}')

        output = json.dumps(self.participants_raw, indent=2)

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
