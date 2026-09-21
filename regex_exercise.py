import re
import gzip
import Bio.SeqIO
import Bio.SeqRecord
import Bio.Seq
import csv
import os


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


class Demultiplexer:

    def __init__(self, fasta_path, mid_table_path):
        self.SR_list = []
        with gzip.open(fasta_path, 'rt') as handle:
            for record in Bio.SeqIO.parse(handle, "fasta"):
                self.SR_list.append(SequencingRead(record.id, str(record.seq)))
        self.MID_list = []
        with open(mid_table_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                self.MID_list.append((row["SampleID"] + "_" + row["Description"], row["FBarcodeSequence"], row["RBarcodeSequence"]))
        self.assigned = {}
        self.unassigned = []

    def assign_reads(self):
        for read in self.SR_list:
            for MID_pair in self.MID_list:
                if read.matches_mid_pair(MID_pair[1], MID_pair[2]):
                    if MID_pair[0] in self.assigned.keys():
                        self.assigned[MID_pair[0]].append(SequencingRead(read.read_id, read.trim_mid_pair(MID_pair[1], MID_pair[2])))
                    else:
                        self.assigned[MID_pair[0]] = [SequencingRead(read.read_id, read.trim_mid_pair(MID_pair[1], MID_pair[2]))]
                    break
                elif read.matches_mid_pair(MID_pair[2], MID_pair[1]):
                    if MID_pair[0] in self.assigned.keys():
                        self.assigned[MID_pair[0]].append(SequencingRead(read.read_id, read.trim_mid_pair(MID_pair[2], MID_pair[1])))
                    else:
                        self.assigned[MID_pair[0]] = [SequencingRead(read.read_id, read.trim_mid_pair(MID_pair[2], MID_pair[1]))]
                    break
                elif MID_pair == self.MID_list[-1]:
                    self.unassigned.append(read)
    def report(self):
        for sample in self.assigned.keys():
            print(sample + "\t" + str(len(self.assigned[sample])))
        print("unassigned \t" + str(len(self.unassigned)))

    def write_fasta(self, output_dir):
        try:
            os.mkdir(output_dir)
        except:
            pass
        for sample in self.assigned.keys():
            Bio.SeqIO.write((Bio.SeqRecord.SeqRecord(Bio.Seq.Seq(rec.sequence), id=rec.read_id) for rec in self.assigned[sample]), f"{output_dir}/{sample}.fasta", "fasta")


demux = Demultiplexer("fishes.fna.gz", "fishes_MIDs.csv")
demux.assign_reads()
print(demux.report())
demux.write_fasta("demux_output")