from datetime import datetime
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

def get_unique_list(l):
    return list(set(l))

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)   

def cosine_sim(counter1, counter2):
        """An implementation of cosine similarity based on word counters rather than vectors"""
        norm_c1 = sum([x**2 for x in counter1.values()])**0.5
        norm_c2 = sum([x**2 for x in counter2.values()])**0.5
        dot_product = 0
        for key in set.intersection(set(counter1.keys()), set(counter2.keys())):
            dot_product += counter1[key]*counter2[key]

        return dot_product/(norm_c1*norm_c2) if norm_c1 != 0 and norm_c2 != 0 else -1

def word_overlap(counter1, counter2):
    """Find the number of overlapping words between two counters"""
    set1 = set(counter1.keys())
    set2 = set(counter2.keys())
    return len(set.intersection(set1, set2))