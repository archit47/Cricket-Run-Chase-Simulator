# Cricket Run-Chase Simulator

> _**Using Weighted Random Numbers**_

There are 2 broad algorithms that I have used for generating the random numbers:
   
* **Random Sampling**
* [Fitness Proportionate Selection](https://en.wikipedia.org/wiki/Fitness_proportionate_selection), also known as, _**Roulette Wheel Selection**_


The Random Generator class can provided at run-time via command line arguments. By default, Random Sampling technique is used for generating the scores. More on this is described below.

## Environment
> Python 3 (preferred)


## Steps for running the code
* Create a virtual environment:
    * virtualenv venv/ --python=python3.6

* Clone or download this repository

* Note: no python dependency is required, so running `requirements.txt` is not required anymore

* _cd_ into the project directory

* Start the virtual environment:
    * source `venv/bin/activate`

* Now lets run this project:
    > __python -m app.main__

* The program optionally takes command line argument: 
    >  __python -m app.main --help__
    
* So, if you wish to choose the random generator class for producing aleatory scores, then:

    * For Random Sampling technique -
    > __python -m app.main -rg 'random sampling'__
    
    * For Roulette Wheel Selection technique -
    > __python -m app.main -rg 'roulette selection'__
    



#### Problem statement provided by [SupplyAI](https://www.supply.ai/)
