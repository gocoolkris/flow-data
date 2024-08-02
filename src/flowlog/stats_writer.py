#!/usr/bin/env python3
import os
from io import TextIOWrapper
from typing import Any, Dict, List
from pathlib import Path
from tabulate import tabulate

class FileReader(object):
    """
    This class is mainly concerned with reading the lookup table that is provided in csv format. 
    """

    filepath: str
    file_obj: TextIOWrapper
    num_lines: int

    def __init__(self, filepath: str):
        """
        The constructor ensures that the filepath is valid and is in csv extension. 
        """
        assert Path(filepath).is_file() and filepath.endswith(".csv"), "File is missing or has invalid format."
        self.filepath = filepath
        self.file_obj = open(filepath, 'r')
        self.num_lines = self._get_lines()
    

    def _get_lines(self) -> int:
        """
        Returns the total number of lines in the file.
        """
        try:
            cmd_output = os.popen(f"wc -l {self.filepath}").read().strip()
            total_lines  = int(cmd_output.split(" ")[0])
            return total_lines
        except: 
            return 0
    
    def read_all(self) -> str:
        """
        :return: the entire file as list of strings including newline characters.
        """
        return self.file_obj.readlines()


    def read_chunks(self, file_obj) -> Any:
        """
        reads the file in chunks of 100kb.
        """
        while True:
            data = file_obj.read(102400)
            if not data:
                break
            yield data


class StatsWriter(object):
    """
    This class writes to the output file the expected data.
    """

    file_content: List[str]
    tag_count: Dict[str, int] = {}
    port_protocol_count: Dict[str, int] = {}
    UN_TAGGED: str = "Untagged"

    def __init__(self, file_content: List[str]):
        self.file_content = file_content
        self.file_content.pop(0)  # ignore the first line as it has column names.

    def _build_data(self) -> None:
        for line in self.file_content:
            lookup_entry = line.strip().split(",")
            port, protocol = int(lookup_entry[0]), lookup_entry[1].strip().lower()
            if len(lookup_entry) < 3 or lookup_entry[2] == "":
                tag = self.UN_TAGGED
            else:
                tag = lookup_entry[2].strip().lower()
            # populate tag_count
            if tag in self.tag_count:
                self.tag_count[tag] += 1
            else:
                self.tag_count[tag] = 1
            # populate port_protocol_count
            ckey = str(port) + "-" + protocol
            if ckey in self.port_protocol_count:
                self.port_protocol_count[ckey] += 1
            else:
                self.port_protocol_count[ckey] = 1
    

    def write_data(self, output_file: str = "stats.txt") -> None:
        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / ("output/")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / (output_file)
        self._build_data()
        with open(output_path, 'w') as writer:
            writer.write("Tag Counts:\n")
            writer.write(tabulate(self.tag_count.items(), headers=["Tag", "Count"]))
            writer.write("\n\n")
            writer.write("Port/Protocol Combination Counts: \n")
            port_protocol_count_lst = []
            for ckey, value in self.port_protocol_count.items():
                port, protocol = ckey.split("-")
                port_protocol_count_lst.append((port, protocol, value))
            writer.write(tabulate(port_protocol_count_lst, headers=["Port", "Protocol", "Count"]))
            writer.write("\n")



class FlowDataMain(object):
    """
    Wrapper class that reads the lookup csv file, parses, builds data and writes it to an output file.
    """

    def write_stats(self, filepath: str) -> None:
        """
        Parses the lookup file, builds and writes the stats to output directory.
        """
        freader = FileReader(filepath=filepath)
        stats_writer = StatsWriter(file_content=freader.read_all())
        output_file = Path(filepath).stem + "-stats.txt"
        stats_writer.write_data(output_file=output_file)
