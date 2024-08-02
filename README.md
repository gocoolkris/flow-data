# Flow Log
This project is in _python_ and it parses a lookup table that is provided in _csv_ format. It also has a generator component that in-turn generates large data (~10MB) to demonstrate the flexibility of the framework.

## Requirements
* _Python3.4_ or above.
* Install the libraries listed in *requirements.txt* using ```pip install -r requirements.txt``` or manually install them.

## Library dependencies
* As it could be gather, the only library outside of common python std libraries used is `tabulate`.

## Installing and running the application
* There are two options (only one to be passed) that can be passed - `['-l', '--lookup_file LOOKUP_FILE']` and `['-g', '--generate_lookup_file']`.
* The `-l` option takes a parameter, which is the path of fully qualified lookup file in csv format, that is to be parsed. All results will be written in `output` folder just under the project root.
* The `-g` option generates a file of 10k entries with limited set of labels and protocols. More details can be found in `src/lookup_generator.py`. This in-turn, can be passed onto `-l` if need be to see the output.


### Sample commands
* As part of the repo, there exists `test/sampledata.csv`. So, if we are to run the stats write functionality, we would execute from the root - `python3 main.py -l test/sampledata.csv`.
* If you want to see the generation of lookup file functionality, you could run `python3 main.py -g` from project root. It would write a sample file to `test` folder. You can then use the generated file to pass to lookup functionality.
* The output file will be usually of the format `<input-name>-stats.txt`, if the lookup file is `<input-name>.csv`.


## Stated Requirements
* Input file as well as the file containing tag mappings are plain text (ascii) files.
* The flow log file size can be up to 10 MB. 
* The lookup file can have up to 10000 mappings. 
* The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample above. 
* The matches should be case insensitive.


## Assumptions
* All entries will have a valid port and protocol (tcp, udp). The tag can be empty. 
* Each entry in the lookup file has atmost one tag.
* There are no other columns or data present.

## Future Improvements
* It is often understood that a solution that works for one scale doesn't work for another. Should the file size or number of mapping increase drastically, we can use chunking to read the file in chunks to avoid loading the entire file in memory.
* Additionally, the data can be queued into a data structure (Queue) and we can process the entry in a multi-threaded fashion.
