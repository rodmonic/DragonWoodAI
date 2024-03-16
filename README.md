# DragonWoodAI

## Introduction

I, like most parents, enjoy playing board games with my kids and one they particularly enjoy is Dragonwood. I have played quite a few games with my kids and started to wonder what the best strategy was and how I can increase my probability of winning. It seems that my kids seem to have an innate understanding of the probabilities involved and have started to beat me more and more.

My approach to understanding this problem is to create a way of playing thousands of games of Dragonwood which should enable me to test out strategies and see which are most successful. Once a suitable system has been developed a stretch goal would be to train an AI to play against a deterministic opponent and see if an AI can find a better approach than I can.

## The Game

The game itself is quite simple and easy to learn but there are a number of decisions the players need to make and lots of scope for elementary strategy even though there is a large probabilistic element to the game. The game is summarised in the rules as:

>*Play cards to earn dice, which you will roll to defeat a fierce array of creatures, or capture magical items that may help you along the way. Whoever earns the most victory points wins.*

The players play Adventurer cards from their hand of up to 9 to capture one of 5 Dragonwood cards. The adventurer cards are numbered 1-12 and are of 5 different colours. A player can attack in 3 ways:

- Strike - play cards that are in order regardless of colour.
- Stomp - play cards that are all the same number.
- Scream - play cards that are all the same colour.

The player gets a dice per card they are attacking with and uses them to defeat Dragonwood cards.

The Dragonwood cards being attacked have different defence values for each type of attack and the player must get that value or higher to beat that card. The Dragonwood cards can be either creatures that give the player victory points when beaten or enhancements which give the user extra abilities or modifiers to their dice roll.

One point to note is that the dice are 6 sided dice but with the values 1, 2, 2, 3, 3, 4. This gives the dice an [Expected Value](https://en.wikipedia.org/wiki/Expected_value) per roll of 2.5.

An example attack is included below to illustrate the decision making process.

|![Dragonwood Example Decision](./docs/Dragonwood%20Example%20Decision.png "An Example Attack") |
| :--: |
| Example attack |

The decision to use which cards in a players hand to try an defeat which Dragonwood cards is the decision we are trying to get an AI to make. I'm hoping to be able to get an AI to identify which cards to use to defeat the Dragonwood cards and also which cards to target to give it the best chance of winning.

## Goals

Given the scope of the problem and the initial wide variety of possibilities, I set out some initial goals to allow me to focus my efforts. As this was an exercise to explore what's possible these are very flexible and will be amended based on the progress I make and research I undertake.

1. Create a model to allow me to play Dragonwood programmatically in Python
1. Develop an rule based algorithm to play Dragonwood deterministically and model how a player selects which cards to attack and when.
1. Develop an AI that can play Dragonwood using reinforcement learning that is as good, or better than the rule based algorithm.
1. Learn some strategies from the AI to improve my chances against my kids.

As a stretch goal for this activity I want to leave as much of the game logic to be determined by the AI. So the AI should be given as little of the games' rules and should learn through its interaction with the game instead of explicit structural learning.

### Goal 1 - Python Model

The first step of the process is to create a model within python to allow me to play dragonwood, based on the [ruleset](https://aadl.org/files/catalog_guides/Dragonwood%20-%20rules.pdf) published online. To do this I created a custom class within python that contained all the objects and methods to complete a game. A simplified version of this model is included below. I have left off the attributes and methods for simplicity

![DragonWoodAI Object Model](./docs/Dragonwood%20Object%20Model.png "Object Model") |
:--: |
Dragonwood model diagram |

I did make a number of simplifying assumptions that shouldn't affect the overall gameplay but will make the model more streamlined.

- I removed certain cards that are only chance based and effect all players with the same probability. These shouldn't affect how the AI plays over a large number of iterations.

- Certain enhancements I did not model and I just focussed on cards that modify a users dice roll. I also only dealt with permanent enhancements not ones that require the AI to decide whether to use them on each attack. This allows the AI to focus on the task of attacking and can be added in later once a successful algorithm and system have been developed.

- As strategy will be slightly different dependant on the number of players, Initially I will play with 4 players; one controlled by AI (I called her Alice) and the other 3 by the deterministic algorithm (Bob, Charles and Dylan).

### Goal 2 - Deterministic algorithm

After the model was created I needed to develop a rule based approach to selecting an attack. This is what I will eventually judge any AI's success or failure against. After trail and error the following algorithm was developed.

1. Find all possible attacks and card combinations from a players current hand.
1. For each card combo work out the expected value of the number of dice. This is the number of cards times by the Expected Value of the dice - 2.5.
1. Add any modifiers from enhancements
1. Take away the score on the card that is trying to be captured.
1. Pick the options with the lowest positive score.

![DragonWoodAI Deterministic Algorithm](./docs/Dragonwood%20Determinsitic%20Algorithm.png "Example Deterministic Decision") |
:--: |
example rule based decision |

#### Sensitivity Analysis

As part of deciding on the best algorithm i performed some analysis on what is the most successful formula for a rule based algorithm. To work out the the values of a and b that are most successful in the below formula:

$$(c \times (Ev_{dice}+a)+b)- score$$

Where:

- $c$ is the number of attacking cards
- $Ev_{dice}$ is expected value of the dice.
- $ score $ is the Dragonwood card's score to beat

To find the best values for a and b I kept 3 players' $a$ and $b$ values constant at 0 and then searched through candidate values running a thousand games for each combination and seeing which  gave the best points per turn. After running 10000 games the results showed the optimum formula was:

$$(c \times (2.50+0.38)-0.13) - score$$

![Sensitivity Analysis](./docs/sentivity%20analysis.png "Sensitivity Analysis") |
:--: |
Search matrix for values of $a$ and $b$ |

### Goal 3 - Dragonwood AI

#### Intro to reinforcement learning

Reinforcement Learning is a paradigm within machine learning where an AI controlled agent learns optimal behaviour within an environment by exploring actions and seeing their impact on a reward function. The main advantage of reinforcement learning is that we do not need a labelled data set on which to train our model, it also works well within games as we have an easily identifiable agent in the form of players.

Reinforcement learning involves the interatiom of the following elements:

- **Environment.** The environment is the entity we are a looking to learn from. In our case this is the Dragonwood game and more specifically the Dragonwood model created in Python. The enviroment provides the agent with information it's state and the impact of the agent's actions.

- **State.** The state of the environment is a set of variables that describe the current game. This is something we have to devise and make sure it includes enough information for the AI to learn from. It could be the cards in the players hands, the players score, which cards have been captured. How this information is encoded is also very important.

- **Action.** The action or decision that the AI has performed. In our case this will be one or more adventurer cards to attack one Dragonwood card.

- **Reward.** This is a function that provides a numerical measure on the suitability of the AI's action within the environment for the given state. This is for us to decide and should reward the AI to prioritise beneficial behaviour. In our case we want to prioritise not only getting points but also winning the game.

- **Agent.** An AI controlled user that can perform actions on the environment given a game state and receives rewards. In our case there will be a single AI agent and a number of rule based users that will perform actions but which we wont refer to as Agents for clarity. We will refer to our AI controlled agent as Alice throughout.

![Learning Diagram](./docs/Learning%20diagram.png "Learning Diagram") |
:--: |
Learning diagram |

There are mutliple different techniques within reinforcement learning, for this specific problem I investigated the below two:

- [Q-Learning](https://en.wikipedia.org/wiki/Q-learning). A reinforcement learning technique where multiple runs of the game would produce a table with the best action for every possible move a player can make.

- [Neuroevolution of augmenting topologies (NEAT)](https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies). A genetic algorithm where a neural network is varied over time to find the best performing architecture.

#### 

#### Q-Learning

Q-learning is a branch of Reinforcement learning where an agent, learns by iterating over the possible actions multiple times to which actions lead to the best outcomes. It does this through the generation and iterative update of what's known as a Q-Learning Table.

The Q-Learning Table is a $N \times M$ matrix Q with:

- $N$ being the number of possible states
- $M$ being the number of possible actions
- $Q_{nm}$ being the Q-value of action $n$ under state $m$

The Q-value is calculated iteratively and updated as the agent takes actions and receives rewards. In simple terms the higher the Q-Value the better the action $m$ under state $n$. As the Q-table is updated the agent will take the action with the highest Q-value for the current state.

The Q-value is updated according to a complex formula that includes a learning rate to allow for exploration of new possibilities as well as learning as from previous experience.

#### State and action space

The first step to implement Q-Learning would be to define the action space and state space to allow me to define the Q-table. As stated in the stretch goal for this task I wanted to try and not abstract away the game rules where possible. This means I want to just and provide the AI Agent with the game and action state and to allow it to learn it's behaviour based on the reward function.

To provide the Agent with the most amount of information to make its decision and without limiting its choices programmatically the state would need to represent:

- Which adventurer cards are in the player's hand out of the possible 62.

- Which Dragonwood cards are in the landscape out of a possible 34.

Given this state the actions would then be:

- Which adventurer cards has the agent selected to attack with.

- Which Dragonwood card has the agent selected to attack.

Given this definition the action-state space does become quite large.

- For a player's hand it could be up to 9 cards chosen without replacement from the deck of 62 which gives us 24,228,029,107 hands.

- For the landscape it could be any combination of 5 cards from the 34 cards available which gives up 331,212.

A very large action-state space means that the model will need to be run longer to make sure all possible combinations are investigated. One way to reduce the action-state space would be to simplify how the state is represented or to use Deep Q-Learning which uses a neural network to represent the Q-table. However, I felt that there might be other algorithms and techniques out there that would allow me to train the AI without simplification.

#### NEAT Intro

NeuroEvolution of Augmenting Topologies (NEAT) is an algorithm developed in 2002 to generate and vary neural networks in a way based on genetic principals. The algorithm varies both the weights, biases and structure of the neural network by mutating and reproducing neural networks to find the best structure to maximise the reward function.

One of the advantages of NEAT is it can handle continuous or multi-dimensional state spaces. This fits our problem quite well from my research into Q-Learning.

I heard about NEAT and it's applicability to my problem through a youtube video that taught an AI to play Monopoly. It's a very interesting watch and is very useful as it shares a lot of the challenges I faced in my problem. Namely, how do I factor in probability in teaching an AI and how do I encode a large and complex state space. It's an interesting watch and includes a link to a github page which was invaluable when I was working through this problem.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/dkvFcYBznPI/0.jpg)](https://www.youtube.com/watch?v=dkvFcYBznPI)

#### NEAT Process

Now we have a technique selected and before we go into the important step of input encoding I thought it would be good to cover at a high level how the environment, agent and reward function are going to be used with this technique. All of the below is implemented using the [Neat-Python](https://neat-python.readthedocs.io/en/latest/index.html) packaage.

1. A network is provided by the NEAT algorithm.
1. This network is then provided to the Dragonwood game and assigned to the Alice player.
1. A game is then played between Alice and the 3 other players.
1. Each time Alice attacks, the environment provides a list of all possible combinations of attacking cards and dragonwood cards to attack. 
1. Each attack combination is then encoded and inputted into the network.
1. The attack combination with the highest score from the network is then enacted.
1. This is repeated until the game ends.
1. The reward is calculated for that network and game.
1. To make sure the networks are given a chance to understand the implications of their weightings and architecture 2000 games are run and the average passed to the NEAT algorithm. 
1. The NEAT algorithm then varies the networks based on the reward gained from the game. 

This process is iterated until a certain number of iterations is passed or the fitness function exceeds a user specified limit.

#### Reward Function

The reward function should be derived to make sure that the correct behaviour is being encouraged through the learning process. The reward function outputs a float number with higher being better. Initially, given our stretch goal of trying to make the AI learn rules instead of imposing rules on it, the AI was provided with a full list of possible attack options including ones that were statistically not possible to attain. I.e. the score of the card was higher than the highest possible dice roll for that option. 

The first iteration of our Reward function was simple:

> The reward would be the amount of points obtained by the network in a game.

Over the process of this I had to change the reward function many times to try and correct the AI's behaviour and improve it's chance of winning.


#### Input Encoding

Now I have a reward function, a learning algorithm and a high level process the final piece of the puzzle is how do I encode the game state to input into the neural network. This step was actually what took the longest time and included much searching of stack overflow and bothering ChatGPT. For the encoding to be successful it must:

- Include all relevant information that the netowrk needs to make a decision.
- Be a 1 dimensional array of floats within the range [0,1]


#### Experiments

#### Updated Encoding

#### Success

#### Results

## initial encoding

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

but all normalised to \[0,1\]

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

got to ~7 max fitness by 70 but then struggled.

### Experiment 5
added a negative 0.25 fitness penalty for drawing a card when it would result in losing a card.
This seemed to confuse the AI and make it select invalid options more and also it didn't increase the score

### Experiment 6
Chnaged fitness function completely so it is

score/number_of_adventure cards discarded + number of invlaid options chose *0.5

This caused the AI to only reload

### Experiments 7
Change everything so only valid options are presented to the AI

quicker to converge but still only managed 7-8

### Experiment 8

Changed how the game state is encoded to:

* length of attacking hand
* score to beat
* number of points
* scream modifier
* strike modifier
* stomp modifier
* player 1 score
* player 2 score
* player 3 score
* player 4 score
* number of game enders

Population's average fitness: 8.94476 stdev: 5.79052
Best fitness: 16.38450 - size: (8, 14) - species 44 - id 22335
Average adjusted fitness: 0.449
Mean genetic distance 3.107, standard deviation 0.750
Population of 150 members in 8 species:
   ID   age  size  fitness  adj fit  stag
  ====  ===  ====  =======  =======  ====
    44   24    27     10.4    0.636     3
    45   20    21      6.9    0.421     6
    47   17     5      1.8    0.113     2
    48    8    32     13.4    0.817     0
    49    5    19      7.9    0.480     1
    50    4    19      7.6    0.461     1
    51    4    18      7.6    0.463     2
    52    1     9      3.3    0.201     0
Total extinctions: 0
Generation time: 362.522 sec (322.047 average)
Saving checkpoint to neat-checkpoint-201

Best genome:
Key: 18633
Fitness: 16.6885
Nodes:
        0 DefaultNodeGene(key=0, bias=-0.7395573638333613, response=1.0, activation=sigmoid, aggregation=sum)
        3645 DefaultNodeGene(key=3645, bias=1.7304809219021717, response=1.0, activation=relu, aggregation=sum)
        4321 DefaultNodeGene(key=4321, bias=1.9033812411004662, response=1.0, activation=relu, aggregation=sum)
        5309 DefaultNodeGene(key=5309, bias=0.5905094695409188, response=1.0, activation=sigmoid, aggregation=sum)
Connections:
        DefaultConnectionGene(key=(-11, 3645), weight=-1.2387335143649874, enabled=False)
        DefaultConnectionGene(key=(-10, 4321), weight=-0.6878208181792393, enabled=True)
        DefaultConnectionGene(key=(-6, 3645), weight=0.7903554632648431, enabled=True)
        DefaultConnectionGene(key=(-5, 3645), weight=-1.7362844731217704, enabled=True)
        DefaultConnectionGene(key=(-5, 5309), weight=0.8831836465948204, enabled=True)
        DefaultConnectionGene(key=(-3, 0), weight=3.060456333297272, enabled=True)
        DefaultConnectionGene(key=(-3, 4321), weight=-0.7731497825441134, enabled=True)
        DefaultConnectionGene(key=(-2, 0), weight=-9.989258211757239, enabled=True)
        DefaultConnectionGene(key=(-1, 0), weight=9.387252634764408, enabled=True)
        DefaultConnectionGene(key=(5309, 3645), weight=0.43687731206410607, enabled=True)
PS C:\Users\DominicMcCaskill\repos\DragonWoodAI> 