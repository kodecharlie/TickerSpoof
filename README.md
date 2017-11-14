# TickerSpoof

This simple `python` script queries online resources for company profiles for randomly determined ticker symbols.
The time between queries is exponentially distributed and determined by a Poisson random variable with a mean
time (between queries) by default of 10s.

Other random factors employed in the script include:

1. The `User-Agent` HTTP header is randomized and chosen arbitrarily from the list of user-agents listed in the file `user-agents.xml`.
1. The ticker symbol queried is randomly chosen from the list of ticker symbols listed in the file `nasdaqtraded.txt`.
1. The online resource or brokerage that supplies company profiles is randomly chosen from a hard-coded list in the script.

## Requirements

Make sure your environment has `Python 2.7` or better.

## Usage

To run `TickerSpoof`, from your command-line shell, execute this command:

    $ python -u TickerSpoof.py

As the script runs, it should indicate progress by periodically listing the number of queries made.
A line of output will look like this:

    ..... Number of queries: 10

Enjoy!