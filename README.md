Python3 tool for Advent of Code
===============================

[![works badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.2.0/badge.svg)](https://github.com/nikku/works-on-my-machine)

 - prepare the files with solution and tests - jinja templates!
 - date sanity checks, defaults to today
 - automatically fetch the input given the AoC year and day (you'd need the token, see [here](https://github.com/wimglenn/advent-of-code-wim/issues/1)).
 - logging and custom lib organization
 - autosubmit found answers
 - built-in profiler


Install
-------

    git clone https://github.com/ArcHound/advent_of_code
    cd advent_of_code
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ./advent_of_code.py --help


CLI
---

### Commands

    Usage: advent_of_code.py [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      prepare  Prepare the template and the test for a given day
      solve    Solve for the input of a given day
    

### Solve command

    Usage: advent_of_code.py solve [OPTIONS]
    
      Solve for the input of a given day
    
    Options:
      --aoc-token TEXT                Token for aoc API  [required]
      --aoc-url TEXT                  Base URL for aoc
      --proxy                         Whether to use the proxy
      --proxy-address TEXT            Proxy address
      --profiling                     Profile the program - get performance data
      --profiling-file FILE           Profiling output file  [default:
                                      /tmp/advent_of_code_profile.log]
      --profiling-sort-key [calls|cumulative|cumtime|file|filename|module|ncalls|pcalls|line|name|nfl|stdname|time|tottime]
                                      Profiling sort key  [default: cumulative]
      -y, --year INTEGER              Year of the event  [default: 2023]
      -d, --day INTEGER               Day of the event  [default: 1]
      -s, --autosubmit                Submit the solution right away?
      --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                      Set logging level.  [default: WARNING]
      --help                          Show this message and exit.
    
### Prepare command

    Usage: advent_of_code.py prepare [OPTIONS]

      Prepare the template and the test for a given day
    
    Options:
      -y, --year INTEGER              Year of the event  [default: 2024]
      -d, --day INTEGER               Day of the event  [default: 9]
      -w, --workspace DIRECTORY       Target dir  [default:
                                      /home/milo/TotallyWorkStuff/advent_of_code]
      -t, --templates DIRECTORY       Template dir  [default: /home/milo/TotallyWo
                                      rkStuff/advent_of_code/templates]
      --solution-template TEXT        Solution template filename  [default:
                                      solution.py.jinja]
      --test-template TEXT            Test template filename  [default:
                                      test.py.jinja]
      --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                      Set logging level.  [default: WARNING]
      --help                          Show this message and exit.
    
