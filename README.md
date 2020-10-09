# SNACES

SNACES (Social Network Algorithm Contained Experiment System)
is a Python library for downloading and analyze Twitter data, by making
use of the Tweepy library and the Twitter API.

## Setup

### Twitter Developer Account

In order to make use of the Twitter API, and the tweepy package, you will need
credential for the twitter API.

To retrieve these credentials sign up for a developer twitter account [here](https://developer.twitter.com/en/apply-for-access).

Getting access may take several days. Once your application is approved,
you will get four keys: `consumer key`, `consumer secret`, `access token`, and
`access token secret`. Enter these four values into the file
`./conf/credentials.py`.

### Installing

1. Clone Git repository to your workspace
1. Run the install script `./scripts/install.sh`
1. Run `python ./setup.py` to setup the Pipfile
1. Run `pipenv shell` to start a pip environment using the pip file

## Running

1. The main program can be started by running `python ./SNACES.py`.
1. This will trigger the main program to loop, which will then prompt you
to input options for which process to trigger:
   1. `Download` downloads information from twitter
   1. `Raw Tweet Processing` processes raw tweets
   1. `Word Frequency` performs word frequency operations on collected data
   1. `Social Graph` constructs a social graph from downloaded friends
   1. `Clustering` performs clustering algorithms on data
