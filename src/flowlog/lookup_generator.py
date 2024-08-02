#!/usr/bin/env python3
from pathlib import Path
from typing import Any, List
from uuid import uuid4

class FlowLogData(object):
    """
    This class contains the flow log data as represented in the csv file.
    """

    port: int
    protocol: str
    tag: str

    UN_TAGGED: str = "Untagged"


    def __init__(self, port: int, protocol: str, tag: str = UN_TAGGED):
        self.port = port
        self.protocol = protocol
        self.tag = tag
    

    def __hash__(self) -> int:
        return hash((frozenset(self.port), frozenset(self.protocol), frozenset(self.tag)))

    def __eq__(self, other) -> bool:
        if not isinstance(other, FlowLogData):
            return False
        return self.port == other.port and self.protocol == other.protocol and self.tag == other.tag
    
    def __repr__(self) -> str:
        return "[" + self.port + "," + self.protocol + "," + self.tag + "]"


class LookupTableGenerator(object):
    """
    This is a helper class that generates data to be parsed by stats writer.
    """

    allowed_tags: List[str]
    allowed_protocols: List[str]
    allowed_ports: List[int]


    def __init__(self):
        self.allowed_tags = ["sv_P1", "SV_P1", "sv_P2", "SV_p2", "SV_P3", "sv_p3", "SV_P4", ""]
        self.allowed_protocols = ['tcp', 'udp']
        self.allowed_ports = [i for i in range(1, 10001)]
    


    def write_data(self) -> str:
        tl = len(self.allowed_tags)
        pl = len(self.allowed_protocols)
        res = []
        for port in self.allowed_ports:
            protocol = self.allowed_protocols[port % pl]
            tag = self.allowed_tags[port % tl]
            res.append((port, protocol, tag))
        rand_str = str(uuid4())
        generated_filedir = Path(__file__).parent.parent.parent / ("test/")
        generated_filedir.mkdir(parents=True, exist_ok=True)
        generated_filepath = generated_filedir / (f"tmp{rand_str}.csv")
        with open(generated_filepath, 'w') as writer:
            writer.write("dstport,protocol,tag\n")
            for e in res:
                writer.write(f"{e[0]},{e[1]},{e[2]}\n")
        return generated_filepath.absolute()
            