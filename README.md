# Minesweeper Solved By Agent(AI)

In this project, the utility function is implemented to find the optimal policy to find the safest square to uncover by computing each of the adjecent squares' probabilities.
Also, the basic agent and improved agent are implemented, and improved agent is solving the minesweeper with the better peformance than the basic agent.
Performance comparison analysis is indicated in the analysis report, so please check it out if you want to know how they perform differently.

### Basic Agent
There should eﬀectively be two parts to the program, the environment representing the board and where the mines are located, and the agent. When the agent queries a location in the environment, the environment reports whether or not there was a mine there, and if not, how many of the surrounding cells are mines. The agent reports whether or not there was a mine there, and if not, how many of the surrounding cells are mines. The agent should maintain a knowledge base containing the information gained querying the environment, and should not only be able to update its knowledge base based on new information, bus also be able to perform inferences on that information and generate new information. 

### Following list is the instruction to implement the knowledgebase for the basic agent to solve the minesweeper. 

1. The environment should take a dimension d and a number of mines n and generate a random d x d boards containing n mines. The agent will not have direct access to this location information, but will know the size of the board. Note: It may be useful to have a version of the agent that allows for manual input, that can accecpt clues and feed you directions as you play an actual game of minesweeper in a seperate window.

2. In every round, the agent should assess its knowledge base, and decide what cell in the environment to query. 

3. In responding to a query, the environment should specify whether or not there was a mine there, and if not, how many surrounding cells have mines. 

4. The agent should take this clue, add it to its knowledge base, and perform any relevant inference or deductions to learn more about the environment. If the agen is able to determine that a cell has a mine, it should ﬂag or mark it, and never query that cell. If the agent can determine a cell is safe, it’s reasonable to query that cell in the next round.

5. Traditionally, the game ends whenever the agent queries a cell with a mine in it - a ﬁnal score being assessed in terms of number of mines safely identiﬁed. 

6. However, extend your agent in the following way: if it queries a mine cell, the mine goes oﬀ, but the agent can continue, using the fact that a mine was discovered there to update its knowledge base (but not receiving a clue about surrounding cells). In this way the game can continue until the entire board is revealed - a ﬁnal score being assessed in terms of mines safely identiﬁed out of the total number of mines.


### Improved Agent (better performance than basic agent)

1. To find the safest square in terms of discovering the adjecent squares that are inferenced from the discovered square, each of the squares has to be computed by using the probability inference and the risk inference.

2. The probabilitiy inference computes all the possible probabilities by inferencing discovered squares. Each of the discovered squares has up to eight adjecent squares with the number of mines that are surrounded. Hence, the probabilities of the adjacent squares are equal, but each square will sum up the other probabilities that can be computed by the other discovered squares. 

3. The risk inference is the function by using the concept of 'what if' hypothesis. If one of the sequentially selected adjacent squares decides the other squares' identifications by considering the square as mine or clear square, then this situation is considered as risk free stage.
    - i.e) if you have 100 percent certainty to decide unreaveled adjacent squares by identifying one of the adjacent squares as mine or safe, then it is the risk free situation and immediately uncover all the adjacent squares.

### Please check the Minesweeper Analysis for the further details.
