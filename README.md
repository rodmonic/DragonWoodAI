# DragonWoodAI

## Introduction

I, like most parents, enjoy playing board games with my kids and one they particularly enjoy is Dragonwood. I have played quite a few games with my kids and started to wonder what the best strategy was and how I can increase my probability of winning. It seems that my kids seem to have an innate understanding of the probabilities involved and have started to beat me more and more.

My approach to understanding this problem is to create a way of playing thousands of games of Dragonwood which should enable me to test out strategies and see which are most successful. Once a suitable system has been developed a stretch goal would be to train an AI to play against a deterministic opponent and see if an AI can find a better approach than I can.

### The Game

Dragonwood is a fantasy-themed card and dice game designed by Darren Kisgen. Set in the mystical realm of Dragonwood, players embark on an adventurous quest to capture magical creatures and collect valuable items. The game revolves around the strategic use of cards representing adventurers, creatures, and enhancements, as well as dice for resolving conflicts. Players face the dual challenge of building a powerful deck and employing effective dice rolls to defeat various creatures in the dangerous forest. The game combines luck and strategy, offering a dynamic and engaging experience as players strive to accumulate the most victory points by the end of the game. Dragonwood's accessible mechanics make it suitable for players of various ages, providing an enjoyable and immersive gaming experience in a whimsical fantasy setting.

### Rules

The game itself is quite simple and easy to learn but there are a number of decisions the players need to make and lots of scope for elementary strategy even though there is a large probabilistic element to the game. The game is summarised in the rules as:

>*Play cards to earn dice, which you will roll to defeat a ferce array of creatures, or capture magical items that may help you along the way. Whoever earns the most victory points wins.*

The players play Adventurer cards to capture Dragonwood cards. The adventurer cards are numbered 1-12 and are of 5 diffrerent colours. A player can attack in 3 ways:

- Strike - play cards that are in a row regardless of colour.
- Stomp - play cards that are all the same number.
- Scream - play cards that are all the same colour.

The player gets a dice per card and then uses them to defeat dragonwood cards to earn either that cards points value or enhancement.

The deicision to use which cards in a players hand to try an defeat which dragonwood cards is the issue we're looking to solve. I'm hoping to be able to get an AI  to identify which cards to use to defeat the dragonwood cards and also which cards to target to give it the bet chance of winning.

One point to note is that the dice are 6 sided dice but with the values 1, 2, 2, 3, 3, 4. This gives the dice an [Expected Value](https://en.wikipedia.org/wiki/Expected_value) per roll of 2.5.

An example attack is included below to illustrate the decision making process.
![Dragonwood Example Decision](./docs/Dragonwood%20Example%20Decision.png "An Example Attack")

## Goals

Given the scope of the problem and the initial wide variety of possibilities, I set out some initial goals to allow me to focus my efforts. As this was an exercise to explore what's possible these are very flexible and will be amended based on the progress I make and research I undertake.

1. Create a model to allow me to play dragonwood programatically in Python
1. Develop an rule based algortihm to play dragonwood deterministically and model how a player selects which cards to attack and when.
1. Develop an AI that can play dragonwood as good, or better than the rule based algorithm.

As a stretch goal for this activity I want to leave as much of the game logic to be determined by the AI. So the AI should be given as little of the games' rules and should learn through its interation with the game instead of explicit sturctural learning.

### Goal 1 - Python Model

The first step of the process is to create a model within python to allow me to play dragonwood, based on the [ruleset](https://aadl.org/files/catalog_guides/Dragonwood%20-%20rules.pdf) published online. To do this I created a custom class within python that contained all the objects and methods to complete a game. A simplified version of this model is included below. I have left off the attributes and methods for simpicity

![DragonWoodAI Object Model](./docs/Dragonwood%20Object%20Model.png "Object Model")

I did make a number of simplifying assumptions that shouldn't affect the overall gameplay but will make the model more streamlined. 

* I removed certain cards that are only chance based and effect all players with the same probability. These shouldn't affect how the AI plays over a large number of iterations.

* Certain enhancements I did not model and I just focussed on the cards that modify a users score. I also only dealt with permanent enhancements not ones that require the AI to decide whether to use them on each attack. This allows the AI to focus on the task of attacking and can be added in later once a sucessful algorithm and system have been developed.

* As strategy will be slightly different dependant on the number of players, Initially I will play with 4 players; one controlled by AI and the other 3 by the determinsitic algorithm.

### Goal 2 - Determinsitic algorithm

After the model was created I needed to develop a rule based approach to selecting an attack.

1. Find all possible attacks and card combinations from a players current hand.
1. For each card combo work out the expected value of the number of dice. This is the number of cards times by 2.5.
1. Add any modifiers from enhancements
1. Take away the score on the card that is trying to be captured.
1. Select the optons with the lowest positive score.

![DragonWoodAI Deterministic Algorithm](./docs/Dragonwood%20Determinsitic%20Algorithm.png "Example Deterministic Decision")


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

got to ~7 max fitness by 70 but then stryggled.

### Experiment 5
added a negative 0.25 fitness penalty for drawing a card when it would result in losing a card.
This seemed to confuse the AI and make it select invalid options more and also it didn't increase the score

### Experiment 6
Chnaged fitness function completely so it is

score/number_of_adventure cards discarded + number of invlaid options chose *0.5