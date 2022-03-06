THE PROBLEM

We want to create an ideal team of players for fantasy football from a given selection. We have a set budget that cannot be exceeded, and the resulting team must have a certain composition of positions for it to be valid (1 goalkeeper, 4 defenders, etc).
The program should output a csv file in the same format as the data file, but only including the players the algorithm has selected.


SOLUTION

1. Load csv file into dataframe, create a new empty dataframe to store final team selection.
2. Loop through the dataframe. Select the first player in the list with highest points, add them to the teamSelect dataframe. 
Then go through the rest of the top players. Skip players with invalid positions until we reach a valid person.
3. Also keep checking that added team members won't exceed the budget. Deduct cost of selected players from budget.
If the selected player is valid but too expensive, skip them until a cheaper person is found.
4. In the dataset, players with less points aren't necessarily cheaper. Because the list is in descending order according to points, 
we know that performance decreases down the list. We need to keep track of the price of our cheapest selected player, and use that as a 
benchmark to compare the others further down the list to.
5. Write teamSelect dataframe to new .csv file

ASSUMPTIONS

1. Input file is always a .csv file
2. Max team size will always be 11
3. Cost and Points columns will always be int
4. Host computer has pandas installed

POTENTIAL IMPROVEMENTS

1. GUI to allow easier input of filepath and user-input of team size, budget, etc
2. Track time/data complexity of algorithm by comparing time taken to complete vs size of input
3. Limit input size if necessary
4. Remove dependancy on pandas (if possible)
