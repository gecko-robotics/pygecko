# Slam Mapping

# Before Start

You need to run a geckocore before you start this:

    `geckocore.py`

# Description

`pub.py` creates a fake lidar scan, just a ring of open area up to 5 meters out (there is some random noise added to the range).

`map.py` uses matlibplot to plot the results of the slam. Unfortunately matplotlib doesn't like how I usually do multiprocessing and crashes. The only way I have found so far to get the plot window to work is create a new python file and run it.

# Running

Open three windows and run:

- `geckocore.py`
- `pub.py`
- `map.py`
