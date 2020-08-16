# Global-Terrorism-Analytics
This repository contains scripts for Terrorism Predictive Analysis. This can be used to find the trend every type of terrorist attacks which not only saves resources to but can also be used to allocate proper measures before the actual incident by means of visualisation.

## Overview
This app contains three tools
1. Map Tool
It generates a Scatter Geo Map with markers for highlighting the lattitude and logitude where the incident happened based on the filters provided in the sidebar.

2. Chart Tool
It generates a Stacked Line Chart images of the frequncy of terrorist incidenta each year.

3. Infographics Tool 
It is used to identify problems in terrorism. Types of patterns could be selected in the sidebar and main display produces filters with patterns in whole world as default.

## Pre-requisite
To run the app please make sure you have the following installed
1. Python 3
2. Pip

## Dependencies
Complete code is written in Python 3 with major dependencies listed below
- Dash 
- Plotly Express
- Pandas
- Bootstrap

## Project Structure
|File Path  | Web URL  |
|---|---|
|[app.py  ](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/app.py) | -  |
|[index.py](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/index.py)   | -  | 
| [./apps/home](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/home.py)  |  / |
| [./apps/map](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/map.py) | /map  |   |
| [./apps/chart](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/chart.py)  |  /chart |   |
| [./apps/infographics](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/infographics.py)  | /infographics  |
| [./apps/densityGraph](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/densityGraph.py)  | /densityGraph  |
| [./apps/peopleKilled](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/peopleKilled.py)  | /peopleKilled  |
| [./apps/weaponUsed](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/weaponUsed.py)| /weaponUsed   |
| [./apps/attackType](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/attackType.py)| /attackType  | 
| [./apps/compAttack](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/compAttack.py)| /compAttack  | 
| [./apps/deathPattern](https://github.com/VinayakTekade/Global-Terrorism-Analytics/blob/master/apps/deathPattern.py)  | /deathPattern  |




## How to run the App
The following are the steps to run the app
1. Clone the repository
`git clone https://github.com/VinayakTekade/Global-Terrorism-Analytics.git`
2. Place your .csv data in ./apps/data directory
`cp <your data> ./apps/data/gloabal_terror_2.csv`
3. Install all the dependencies
`pip install -r requirements.txt`
4. Start the app using index.py
`py index.py`

## Team
- [**Vineetha Arun**](https://github.com/VineethaArun) 
- [**Abhishek Pandavula**](https://github.com/abhishekpandavula)
- [**Vinayak Tekade**](https://github.com/VinayakTekade)

See the full list of [contributors](https://github.com/VinayakTekade/Global-Terrorism-Analytics/graphs/contributors) who participated in this project and statistics.

## How to report bugs or issues?
Report [here](https://github.com/VinayakTekade/Global-Terrorism-Analytics/issues/new) in detail answering these questions:
-   What steps did you take to make the bug appear?
-   How can the bug be fixed? (In case you know)
-   Which OS and which all packages/software/dependencies are you using?
-   Have you tried any troubleshooting steps such as a reboot for example?