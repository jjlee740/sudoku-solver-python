# Sudoku Solver in Python

Solves the classic game of sudoku by using either the classic backtracking approach or a more efficient approach using the algorithm outlined by Donald Knuth. 
Read more about Knuth's Algorithm X here: https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X#:~:text=Algorithm%20X%20is%20an%20algorithm,uses%20the%20dancing%20links%20technique.

## Installation

To install the required packages: 

On macOS/Linux:
```
python -m pip install -r requirements.txt
```
On Windows:
```
py -m pip install -r requirements.txt
```

Run the python file in your favorite editor or by this command: 
```
python3 sudoku-solver.py
```


## Exact Cover & Dancing Links

The theory behind exact cover and dancing links can be difficult to grasp but extremely intuitive once you wrap your head around them. 
Below is a quick recap of what an exact cover problem is and how dancing links may help solve these problems. 

Sudoku problems belong in the class of Exact Cover problems which have a defined deterministic solution. 
Exact cover problems can be represented by a matrix with the rows representing the possible solutions and the columns representing the constraints. We say that we have found a solution to the exact cover problem when there is a matrix when the set of rows has exactly 1 for each column.  
In the case of Sudoku, we have found that there are 9x9x9 = 729 possible solutions and 9x9x4 = 324 contraints, as such there is a possible solution in the matrix size of 729 x 324. 

In order to efficiently find this solution within these possibilities, we use a technique called Dancing Links which simply states that we can find the last state of a deleted node in a circular doubly linked list. As such, if we encounter a solution space that is a dead end in our matrix, we have a method to reverse to the previous state such that we can backtrack efficient to this previous state. 
