# DragonWoodAI

## Introduction

I, like most parents, enjoy playing board games with my kids and one they particularly enjoy is a dice and card game called Dragonwood. We have played it a lot and it seems that my kids have an innate understanding of the probabilities involved and started to beat me more and more. This lead me to wonder what the best strategy was and how I could increase my chances of winning.

I searched online for any strategies or an explanation of the probabilities involved but couldn't find anything so I decided I would attack the problem like I would a problem at work using Python and MAchine Learning. So as an excuse to get better at Dragonwood, learn a new AI technique and to write some python I decided to see if I could teach an AI to play the game better than me and try and understand what strategies it uses.

## The Game

The game itself is quite simple and easy to learn but there are a number of decisions the players need to make and lots of scope for elementary strategy even though there is a large probabilistic element to the game. The game is summarised in the rules as:

>*Play cards to earn dice, which you will roll to defeat a fierce array of creatures, or capture magical items that may help you along the way. Whoever earns the most victory points wins.*

The below video sums up the rules pretty well and shows the basic structure of the game.

[![](https://img.youtube.com/vi/OL9VgIW8pV8/0.jpg)](https://www.youtube.com/watch?v=OL9VgIW8pV8)

The players play Adventurer cards from their hand of up to 9 to capture one of 5 available Dragonwood cards. The adventurer cards are numbered 1-12 and are of 5 different colours. A player can make the following 4 decisions:

- Strike - attack with cards that are in order regardless of colour.
- Stomp - attack with cards that are all the same number.
- Scream - attack with cards that are all the same colour.
- Reload - Draw a card

The decision to use which cards in a player's hand to try an defeat which Dragonwood cards is the decision we are trying to get an AI to make. I'm hoping to be able to get an AI to identify which cards to use to defeat the Dragonwood cards and also which cards to target to give it the best chance of winning.

## Goals

Given the scope of the problem and the initial wide variety of possibilities, I set out some initial goals to allow me to focus my efforts.

1. Create a model to allow me to play Dragonwood programmatically in Python
1. Develop a rule based algorithm to play Dragonwood deterministically and model how a player selects which cards to attack and when.
1. Develop an AI that can play Dragonwood using reinforcement learning that is as good, or better than the rule based algorithm.
1. Learn some strategies from the AI to improve my chances against my kids.

As a stretch goal for this activity I want the AI to be given as little of the game's rules as possible and should learn through its interaction with the environment instead of having the game structure imposed on it.

### Goal 1 - Python Model

The first step of the process is to create a model within python to allow me to play Dragonwood, based on the [rule-set](https://aadl.org/files/catalog_guides/Dragonwood%20-%20rules.pdf) published online. To do this I created a custom class within python that contained all the objects and methods to complete a game. A simplified version of this model is included below. I have left off the attributes and methods for simplicity

| ![DragonWoodAI Object Model](./docs/Dragonwood%20Object%20Model.png "Object Model") |
| :--: |
| Dragonwood model diagram |

### Goal 2 - Deterministic algorithm

After the model was created I needed to develop a rule based approach to selecting an attack. This is what I will eventually judge any AI's success or failure against. After trail and error the following algorithm was developed:

1. Find all possible attacks and card combinations from a player's current hand.
1. For each attack option, work out the Expected Value of the number of dice for that attack. This is the number of cards times by the Expected Value of the dice - 2.5.
1. Take away the score on the card that is trying to be captured.
1. Pick the options with the lowest positive score.

| ![DragonWoodAI Deterministic Algorithm](./docs/Dragonwood%20Determinsitic%20Algorithm.png "Example Deterministic Decision") |
| :--: |
| example rule based decision |

#### Sensitivity Analysis

As part of deciding on the best algorithm I performed some analysis on what is the most successful formula for a rule based algorithm. This boils down to the best values of $a$ and $b$ in the below formula:

$$(c \times (Ev_{dice}+a)+b)- {card\ defence\ score}$$

Where:

- $c$ is the number of attacking cards
- $Ev_{dice}$ is expected value of the dice.
- $card\ defence\ score$ is the Dragonwood card's score to beat for that attack type.

To find the best values for $a$ and $b$ I kept 3 players' $a$ and $b$ values constant at 0 and then searched through candidate values running a thousand games for each combination and seeing which  gave the best points per turn. After running 10,000 games  the optimum formula was:

$$(c \times (2.50+0.38)-0.13) - {card\ defence\ score}$$

| ![Sensitivity Analysis](https://github.com/rodmonic/DragonWoodAI/blob/cb04a135d0b5841cf91336857bccf0b6db3221c4/docs/sentivity%20analysis.png "Sensitivity Analysis") |
| :--: |
| Search matrix for values of $a$ and $b$ |

### Goal 3 - Dragonwood AI - Introduction to reinforcement learning

Reinforcement Learning is a paradigm within machine learning where an AI controlled agent learns optimal behaviour within an environment by exploring actions and seeing their impact on a reward function. The main advantage of reinforcement learning is that it does not require a in-depth understanding of the system involved and can explore the system as part of the learning process. This advantage is especially potent as systems become more complex, as finding humans with the necessary knowledge can become increasingly difficult (if not impossible).  

The diagram and definition below shows how the various elements within a Reinforcement Learning problem interact. 

| ![Learning Diagram](./docs/Learning%20diagram.png "Learning Diagram") |
| :--: |
| Learning diagram |

- **Environment.** The environment is the entity we are a looking to learn from. In our case this is the Dragonwood game and more specifically the Dragonwood model created in Python. The environment provides the agent with information on it's state and the impact of the agent's actions.

- **State.** The state of the environment is a set of variables that describe the current game. This is something we have to devise and make sure it includes enough information for the AI to learn from. It could be the cards in the players hands, the players score and/or which cards have been captured. How this information is encoded is also very important.

- **Action.** The action or decision that the AI has performed. In our case this will be one or more adventurer cards to attack one Dragonwood card.

- **Reward.** This is a function that provides a numerical measure on the suitability of the AI's action within the environment for the given state. This is for us to define and should reward the AI to prioritise beneficial behaviour. In our case we want to prioritise not only getting points but also winning the game.

- **Agent.** An AI controlled user that can perform actions on the environment given a game state and receive a reward for those actions. In our case there will be a single AI agent and a number of rule based users that will perform actions but which we won't refer to as Agents for clarity. We will refer to our AI controlled agent as Alice throughout.

There are multiple different techniques within reinforcement learning, for this specific problem I investigated [Neuroevolution of augmenting topologies (NEAT)](https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies). A genetic algorithm where a neural network is varied over time to find the best performing architecture against a reward function.

#### Introduction to NEAT

NeuroEvolution of Augmenting Topologies (NEAT) is an algorithm developed in 2002 to generate and vary neural networks in a way based on genetic principals. The algorithm varies both the weights, biases and structure of the neural network by mutating and reproducing neural networks to find the best structure to maximise the reward function.

So instead of having a fixed network architecture where the best solution is found by varying the weights and biases, NEAT varies both the actual network structure as well as the weights. In practice this means that the optimal solution can be found quicker as the network itself has a lot of impact on its utility.

#### NEAT Algorithm

The algorithm works by starting with a user defined number of inputs and output. In our case it will be our attack option encoded as an input and our output will be a number in \[0,1\] to show how good the network thinks that move is.

The input and output structure will stay constant through the evolution but nodes and connections between nodes  will be added to the network through a process known as **mutation**.

| ![Generation of networks](./docs/NEAT%20Networks.png "NEAT Networks") |
| :--: |
| Base Networks |

To decide which networks are the most successful we use a measure known as fitness and once networks have been generated/mutated and their fitness calculated, new networks are generated by reproduction between 2 high performing networks. This reproduction ensures beneficial traits of the weights and network are combined to hopefully improve the performance of the network.

| ![Reproduction](./docs/Reproduction.png "Reproduction") |
| :--: |
| Reproduction |

The process is repeated for multiple generations with mutation, variation in the weights and reproduction all happening according to various hyperparameters within the algorithm. Luckily all this is handled by a brilliant implementation of the algorithm in the [Neat-Python](https://neat-python.readthedocs.io/en/latest/index.html) library. The library also tracks a measure of the genetic diversity within the population and maintains a record of the best performing networks and whether a species has become stagnant i.e. has stopped improving.

|![NEAT Process](./docs/NEAT%20Process.png "NEAT Process") |
| :--: |
| NEAT Process |

#### Fitness Function

The fitness function should be derived to make sure that the correct behaviour is being encouraged throughout the learning process. The function outputs a decimal number with higher being better. Initially, given the stretch goal of trying to make the AI learn rules instead of imposing rules on it, the AI was provided with a full list of possible attack options including ones that were statistically not possible to attain. i.e. the defence score of the card was higher than the highest possible dice roll for that option.

The first iteration of the fitness function was simple, it would be the average score received by that network:

$$\frac{\sum {score}}{number\ of\ iterations}$$

#### Input Encoding

Now I have a fitness function, a learning algorithm and a high level process, the final piece of the puzzle is how do I encode the game state to input into the neural network.

For the encoding to be successful it must:

- Include all relevant information that the network needs to make a decision.
- Be a $n \times 1$ array of floats within the range \[0, 1\]
- Be as simple as possible to allow the Neural Network to recognise the relationships between the state, actions and fitness function.

This step was actually what took the longest time and included much searching of stack overflow and bothering ChatGPT. My initial encoding included a neuron per card within the Adventurer and Dragonwood desks as well as some contextual information, this resulted in a input layer with 86 neurons.

## Experiments

The aim with all of these networks is to beat the rule based approach. To give me a number to aim for I ran the algorithm but only used the rule based approach, this gave me an average score of around 14 per game. For all of our experiments we need for the AI to be able to get more than this to say we have been successful.

My initial experiments were pretty unsuccessful only managing about a score of 7 per game. This was far below what was needed and so resulted in multiple changes to the parameters used in the NEAT algorithm, the fitness function and the dragon wood model to try and unlock the issue but to no avail.

### Revising the input parameter

At this point I had been working on getting the network right for a month and had changed quite a few variables with minimal change in the resultant fitness function. I felt therefore it was time to review the input encoding. Simplification of the encoding would mean that more of the games logic would be abstracted away from the network but the current approach was not yielding results.

So I decided to simplify the encoding trying to put the least amount of information needed, not worrying about abstracting away information. I ended up with the following encoding:

- length of attacking hand
- score to beat on selected Dragonwood card
- number of points of selected Dragonwood card
- scream modifier if the card is an enhancement
- strike modifier if the card is an enhancement
- stomp modifier if the card is an enhancement
- player 1 score
- player 2 score
- player 3 score
- player 4 score
- game length context

This encoding reduces the number of input nodes from 86 to 11.

When the process is running it can take hours to complete so I usually ran it in the evening or over the weekend. So I started it running on a Friday evening and went to bed.

## Success

So after over 300 generations I ended up with a network with a score of 16.6885. I now have a network that could compete with, and hopefully beat, my rule based algorithm. This really proves how important the input encoding is and how it must include only relevant information. In my first attempt at an encoding I was providing the network with a lot of information, some of which wasn't useful to learn from. This meant the network was not able to deduce this information from the encoding and so was struggling to learn. There was also a lot of other information which was confusing the network that was largely unrelated to selecting a card.

This below chart shows us how the network approaches it's best result with the max fitness in red staying pretty stable after 50 generations with the average and the $\pm$ 1 standard deviation taking a little longer to reach optimum at around generation 200.

|![Average Fitness by Generation](<./docs/Average Fitness by Generation.svg> "Average Fitness by Generation") |
| :--: |
| Average Fitness by Generation |

Finally to check the networks performance against my rule based approach I ran 100,000 games with Alice using the best network from the NEAT algorithm and the other players using the rule based approach with the best formula I derived based on our scenario analysis above.

|![Final Results](<./docs/Final Winners.png> "Final Results") |
| :--: |
| Final Results |

While the advantage Alice has isn't massive, there is a 7% increase in chance of winning over the deterministic algorithm. We can see that Alice has managed to not only learn the right moves to make but she also has a slight advantage over the rule based algorithm.

To try and understand why this might be, and some of the decision making process behind the algorithm, I decided to investigate the weights and structure of the network. The Neat-python library has a simple tool that visualises the winning network. The first output of the tool provides us with the below network.

|![Final Network Full](<./docs/Final Network Full.png> "Final Network") |
| :--: |
| Final Network Full |

Within the network we have the following elements:

- Grey nodes are the input nodes
- The blue node is the output node
- Yellow nodes are hidden nodes connected to the input or output nodes.
- Red nodes are hidden nodes unconnected to the inout or putput nodes.

This may look confusing and messy at first glance but this is a result of how the network is evolved. Nodes and connections are added and deleted to the network by the NEAT algorithm at random. This means nodes may become disconnected from the input nodes or output nodes but are not deleted automatically but have no impact on our output. Therefore, any node that is not connected to the input or output node can be deleted. A "pruned" version is shown below.

|![Final Network Pruned](<./docs/Final Network Pruned.png> "Final Network Pruned") |
| :--: |
| Final Network Pruned |

I have recoloured the input nodes yellow that weren't affecting the output and formatted the lines between the nodes according to their weight. What we can clearly see now is that the most important input nodes are the length of attacking hand and score to beat as we would expect. The remaining nodes are of minimal importance.

This broadly aligns with my initial intuition on how to select a card. It should be based on how many dice are available and the score that is needed to be beaten. It is interesting however that the amount of points or the reward from the enhancement are not important to the overall output. One possible explanation for this is that the game developers did a good job of balancing the score to beat with the card's points,  meaning the score to beat alone is enough to capture any cost-benefit trade-offs when deciding on whether to attack.

I think the slight advantage that Alice had over the rule based agents was probably down to the network calculating a slightly better formula for prioritising when to attack.

## Results & Summary

So, have I been successful? Well, if I refer back to my initial goals for the project they were:

1. Create a model to allow me to play Dragonwood programmatically in Python
1. Develop an rule based algorithm to play Dragonwood deterministically and model how a player selects which cards to attack and when.
1. Develop an AI that can play Dragonwood using reinforcement learning that is as good, or better than the rule based algorithm.
1. Learn some strategies from the AI to improve my chances against my kids.

I would say I have achieved the first 3 goals and while I didn't get any specific strategies to use from the AI, it did effectively confirm that the rule based approach gives a very good strategy to use against my kids and the AI generated network provides a 7% improvement over the rule based algorithm I generated.

Overall it has been a really interesting and rewarding process and I have learnt a lot about Reinforcement Learning, Neural Networks and how to model systems in using Object Oriented principals in Python. However, by the time I have got to a point where I could apply the strategies I had learnt, my kids had moved on and didn't want to play Dragonwood any more.

The three lessons I have learnt from the process are:

- Be very careful when generating the input encoding.

- Sometimes a rule based approach will give good enough results.

- Be quicker as children get bored easily.
