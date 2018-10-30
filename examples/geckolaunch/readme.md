# GeckoLauncher


# Before Start

You still need to run `geckocore.py` so the published messages reach
the subscribers!

# Description

Running `geckolaunch.py` with a launch file, allows you to quickly setup a
complex web of nodes with one command.

# Launch Files

Your launch file can be either yaml or json. Each process to run line is:
`["file", "function_in_file", {dictionary_of_args_to_pass}]`. The args can be
anything your process needs to know.

We also need to tell `geckolaunch` if we are not using the default addresses
for `geckocore`.

## json

The file extension must be `*.json`

```bash
{
  "processes":
  [
    ["process", "publish", {"topic": "hello"}],
    ["process", "publish", {"topic": "hey there"}],
    ["process", "subscribe2", {"topic": "hello"}],
    ["process", "subscribe2", {"topic": "hello"}],
    ["process", "subscribe2", {"topic": "hey there"}],
    ["process", "subscribe2", {"topic": "hey there"}],
    ["process", "subscribe2", {"topic": "cv"}],
    ["process", "subscribe2", {"topic": "cv"}],
    ["process", "pcv", {"topic": "cv"}]
  ],
  "geckocore": {
      "host": "localhost"
  }
}
```



## Usage

Open two windows, in one, run `geckocore.py` and the other run `./run.sh`.
You should see the performance and log messages printing to the two windows.
