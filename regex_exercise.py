import re


def reverse_complement(seq):
    dict = {"A":"T", "T":"A","C":"G", "G":"C"}
    complement = ""
    for letter in seq:
        complement += dict[letter]
    return complement[::-1]


class SequencingRead:

    def __init__(self, read_id, sequence):
        self.read_id = read_id
        self.sequence = sequence

    def matches_mid_pair(self, forward_mid, reverse_mid):
        if re.search("^" + forward_mid + ".+" + reverse_complement(reverse_mid) + "$", self.sequence):
            return True
        else:
            return False

    def describe(self):
        return f"SequencingRead {self.read_id} ({len(self.sequence)} bp)"

    def trim_mid_pair(self, forward_mid, reverse_mid):
        if self.matches_mid_pair(forward_mid, reverse_mid):
            no_for = re.sub(forward_mid, "", self.sequence)
            return re.sub(reverse_complement(reverse_mid), "", no_for)
        else:
            return None


r1 = SequencingRead("demo_1", "AGCTTCGA" + "N" * 20 + reverse_complement("TGCAGGTC"))
print(r1.describe())
print(r1.matches_mid_pair("AGCTTCGA", "TGCAGGTC"))  # True
print(r1.matches_mid_pair("CGATCGAT", "GCTAGCTA"))  # False
print(r1.trim_mid_pair("AGCTTCGA", "TGCAGGTC"))     # 20 x "N"