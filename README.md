# DragonWoodAI

## Introduction

I, like most parents, enjoy playing board games with my kids and one they particularly enjoy is Dragonwood. I have played quite a few games with my kids and started to wonder what the best strategy was and how I can increase my probability of winning. It seems that my kids seem to have an innate understanding of the probabilities involved and have started to beat me more and more.

My approach to understanding this problem is to create a way of playing thousands of games of Dragonwood which should enable me to test out strategies and see which are most successful. Once a suitable system has been developed a stretch goal would be to train an AI to play against a deterministic opponent and see if an AI can find a better approach than I can.

## The Game

Dragonwood is a fantasy-themed card and dice game designed by Darren Kisgen. Set in the mystical realm of Dragonwood, players embark on an adventurous quest to capture magical creatures and collect valuable items. The game revolves around the strategic use of cards representing adventurers, creatures, and enhancements, as well as dice for resolving conflicts. Players face the dual challenge of building a powerful deck and employing effective dice rolls to defeat various creatures in the dangerous forest. The game combines luck and strategy, offering a dynamic and engaging experience as players strive to accumulate the most victory points by the end of the game. Dragonwood's accessible mechanics make it suitable for players of various ages, providing an enjoyable and immersive gaming experience in a whimsical fantasy setting.

## Python Model

The first step of the process is to create a model within python to allow me to play dragonwood, based on the [ruleset](https://aadl.org/files/catalog_guides/Dragonwood%20-%20rules.pdf) published online.

## exploration

## initial encoding:

62 neurons to model the current hand, 1 if the player has that card and 2 if it's part of the attack option
34 neurons to model the current landscape 1 if the player has that card and 2 if it's part of the attack option
4 neurons for the points for each player
1 neuron for the number of game ender cards still out there 

### series 1

- population 20
- iterations per run 100
- activation function tanh
- score as fitness


Population's average fitness: 2.50200 stdev: 0.78152
Best fitness: 3.97000 - size: (1, 81) - species 1 - id 197
Average adjusted fitness: 0.506
Mean genetic distance 0.533, standard deviation 0.279
Population of 20 members in 1 species:
   ID   age  size  fitness  adj fit  stag
  ====  ===  ====  =======  =======  ====
     1   19    20      4.0    0.506     5

### series 2

- population 20
- iterations per run 1000
- activation function tanh
- score as fitness

 ****** Running generation 12 ******

Population's average fitness: 2.02415 stdev: 0.62575
Best fitness: 3.11800 - size: (1, 82) - species 1 - id 203
Average adjusted fitness: 0.492
Mean genetic distance 0.656, standard deviation 0.287
Population of 20 members in 1 species:
   ID   age  size  fitness  adj fit  stag
  ====  ===  ====  =======  =======  ====
     1   12    20      3.1    0.492     1
Total extinctions: 0
Generation time: 431.918 sec (425.567 average)
 
## next encoding

62 neurons to model the current hand, 1 if the player has that card and 2 if it's part of the attack option
34 neurons to model the current landscape 1 if the player has that card and 2 if it's part of the attack option
4 neurons for the points for each player
1 neuron for the number of game ender cards still out there 

but all normalised to [0,1]

Managed to get around 7 fitness after 60 generations



## adjusted fitness function

Added negative -0.5 for each impossible card and adventurer combination the model chooses.

## adjusted config

Have the mean as the fitness function instead of Max
### Experiment 3
 ****** Running generation 113 ******

Population's average fitness: 3.09993 stdev: 2.53612
Best fitness: 6.70325 - size: (2, 73) - species 1 - id 13201
Average adjusted fitness: 0.742
Mean genetic distance 1.695, standard deviation 0.326
Population of 150 members in 2 species:
   ID   age  size  fitness  adj fit  stag
  ====  ===  ====  =======  =======  ====
     1  113    79      3.6    0.774    43
     4   64    71      2.7    0.710    40
Total extinctions: 0
Generation time: 1231.696 sec (1207.355 average)
Saving checkpoint to neat-checkpoint-113

Noticed that the AI is reloading a lot so may need to adjust the probablity that triggers a reload.

### Experiment 4
changed the cut off for a reload decision to 0.33 as in the logs the AI seemed to be reloading a lot.


### Noticed an error in my encoding 
- that would allow over 1 for a landsacpe with the same card in twice
- order of players scores were shuffled each time so was effectively adding confusion into the network.
- also added in 10 more fitness points if they actaully win.