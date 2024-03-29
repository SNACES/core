# SNACES

SNACES (Social Network Algorithm Contained Experiment System)
is a Python library for downloading and analyze Twitter data, by making
use of the Tweepy library and the Twitter API.

## Update

The last update of this document is completed in Jan 10, 2023.

## Setup

### Twitter Developer Account

In order to make use of the Twitter API, and the tweepy package, you will need
credential for the twitter API.

To retrieve these credentials sign up for a developer twitter account [here](https://developer.twitter.com/en/apply-for-access).

Getting access may take several days. Once your application is approved,
you will get four keys: `consumer key`, `consumer secret`, `access token`, and
`access token secret`. Enter these four values into the file
`./conf/credentials.py`.

### MongoDB

You will need MongoDB for data storage. 

### Installing

1. Clone Git repository to your workspace
2. Run the install script `./scripts/install.sh`
3. Run `python ./setup.py` to setup the Pipfile
4. Run `pipenv shell` to start a pip environment using the pip file
  
Note that you might need to do the following in the pip environment:  
1. pip install python-dateutil
2. pip install matplotlib
3. create /core/log folder

### Configuration

The default path we are using is:
`/src/scripts/config/create_social_graph_and_cluster_config.yaml`

## The Clustering Trial Branch

A lot of work has been done on the clustering trial branch which focuses on core detection.

### Installing

See `clustering_trial_requirements.txt` for the required packages for the clustering trial branch. **Note:** The pygraphviz package may require additional installation steps. See [here](https://stackoverflow.com/questions/15661384/python-does-not-see-pygraphviz/71661788#71661788).

There may be some problems with the pipenv shell above. An alternative is to use a conda environment with Python 3.9. After installing conda and activating your environment, run `pip install -r clustering_trial_requirements.txt` to install the required packages.

If there are some issues with pip conflicting, while in the conda environment, try the following to create a virtual environment and install the required packages: 
```
python -m venv env
source env/bin/activate
pip install -r clustering_trial_requirements.txt
```

### Running

Once the required packages are installed, you can run the core detection algorithm by executing
```
python detect_core_jaccard.py -n "hardmaru" -act "user retweets"
```
`-n` stands for the seed user and `-act` represents the chosen activity set. The available activity sets are `user retweets`, `friends`, and `user retweets ids`.

## Running

1. The main program can be started by running `python ./SNACES.py`.
1. This will trigger the main program to loop, which will then prompt you
to input options for which process to trigger:
   1. `Download` downloads information from twitter
   1. `Raw Tweet Processing` processes raw tweets
   1. `Word Frequency` performs word frequency operations on collected data
   1. `Social Graph` constructs a social graph from downloaded friends
   1. `Clustering` performs clustering algorithms on data
   1. `Community Expansion` performs community expansion on data
   1. `Community Expansion - Create Graph` produce graphs for results in community expansion
   
The only one we are currently using is `Community Expansion`  
For core detection, please checkout branch `clustering_trials` for the latest version of core detection algorithm

## Current Work

### dao module

The dao module includes all the getter and setters that connects the data storage with our program.

### model module

The model module includes the instances such as User and Tweets that are used in our program

### Utility Functions

Utility Functions tell us activities of a user in a community, and they take a huge part in our analysis. We are actively exploring new utility functions.
The implementations of utility rankers are located in 
`/src/process/ranking/consumption_utility_ranker.py`

### Community Expansion

The main code for community expansion is in 
`/src/process/community_expansion/`

You will also use code in the following path for data analysis:
`/src/process/data_analysis/`

### Core Detection

Please checkout branch `clustering_trials` for the latest version of core detection algorithm.
