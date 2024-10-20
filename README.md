# Network science Lab
### Group 18

This repository will contain our work for the Network science lab. We have choosen the subject 30:

### Implement a computer simulation of the SIS model in a given network. Compute the epidemic threshold for lattices, random graphs, BA model networks and minimal model. Discuss the results.

Depending on the time we spend on this subject, it may evolve with a change in the model (SIS &rarr; SIR).


## Code dependancies:

Your need the following python modules installed:

- networkx
- matplotlib
- yaml
- reportlab
- numpy
- os
- datetime
- scipy
- random

Some of these modules are already present by default in python but make sure that you have them all.

To install a module, you must run:

    pip install <module>

note: the module 'hosting' yaml is called pyyaml, so run

    pip install pyyaml

to install it.

The code has been written using python 3.12, I advise running it with the same version.

## Code usage

You can modify the different configuration inside the simulation/config folder. I tried to be explicit to what can be 
and cannot be wrotte inside them but mistakes can happen, if you spot one, please report it by making an issue.

I also tried not to use hard coded path, but I would advise not to change any folders inside simulation. If no out
folder is present, it should generate itself.

To run the code, you can just open a terminal inside the simulation folder and use:
    
    python main.py

The output will be stored in [out](out) within folders named after the date of the execution and file named after the
time of execution. Be aware that the execution can take some time (approx. 3min) mostly for the dynamic running.

Be advice that for an unknown issue, the scale on the contour plot when running dynamically is inverted.

## Documents and IA usage

Some of the code, mostly [utils.py](simulation/utils/utils.py), was generated using chatGPT. Any other sources that may
have been used are in [bibliography](bibliography).