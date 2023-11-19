import random as r


class Logic:
    def __init__(self, adults, children):
        self.adults = adults
        self.children = children

    def match_adults(self):
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
        # unmatched_a = list(self.adults.keys())
        unmatched_a = [a_name for a_name, adult in self.adults.items() if adult.name not in ["Alain", "Fatiha"]]
        unmatched_c = list(self.children.keys())
        matches = {}
        for _ in range(len(unmatched_a)):
            a_name = r.choice(unmatched_a)
            c_name = None
            try:
                c_name = r.choice(unmatched_c)
            except IndexError:
                print(f'Children list is empty')
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
                print(f'Unmatched adults: {unmatched_a}')
            elif unmatched_a:
                print(f'Unmatched children: {unmatched_c}')
            return matches

    @staticmethod
    def merge_matches(m1, m2):
        merge = {k: [] for k, _ in m1.items()}
        for k, _ in merge.items():
            try:
                merge[k].append(m1[k])
            except KeyError:
                print(f'No {k} in adults')
            try:
                merge[k].append(m2[k])
            except KeyError:
                print(f'No {k} in children')
        return merge

    def run(self):
        matches_a = self.match_adults()
        matches_c = self.match_children()
        matches = self.merge_matches(matches_a, matches_c)
        return matches