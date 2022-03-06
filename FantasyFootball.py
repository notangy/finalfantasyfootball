import pandas as pd
import sys
import time


# Load in the .csv file to a dataframe, sort it in descending order, then return
def loadCSV(fileName):

    # Assign .csv contents to a dataframe
    data = pd.read_csv(fileName)      

    # Remove rows where points column !> 0 
    #data = data.loc[data["Points"] > 0 ]
    # ^ Removed during input testing: a small source file may have 0 point players that are necessary to create a valid team

    # Sort trimmed data frame by Points column in descending order
    data.sort_values(["Points"], axis=0, ascending=[False], inplace=True)

    return data

# Returns true if selected player is valid addition to team, false if not valid
def checkTeamCompValid(validTeamComp, currentTeamComp, position, row):

    # This if-statement should always be true, if not then there is a syntax error in the source csv file
    if position in validTeamComp:
            
            # Max. number of allowed players for current position is taken from reference table
            maxNumber = validTeamComp[position]

            # If the max number of players for the position have already been selected, return false because current player is not valid choice
            if currentTeamComp[position] == maxNumber:
                return False

            # Else, increment # keeping track of how many specific players are on the team and return true
            else:
                currentTeamComp[position] = currentTeamComp[position] + 1
                return True

    print(f"\nWARNING: there is an invalid POSITION cell in the source data file:\n {row.to_string(index=False)}. \nThe produced team may not be the best possible solution. Please make sure all rows contain only GK, DEF, MID or FOR.")
    # Continue program since a valid team can still possibly be created from other rows
    return False

# Contains loops to go through all the players
def selectTeam(sortedList, selectedTeam, budget, columns, maxTeam):

    # this is a 'reference' dictionary for how many players max. for each position there should be on the team
    validTeamComp = {"GK": 1, "DEF": 4, "MID": 4, "FOR": 2}

    # this is to keep track of how many players of different positions have been selected
    currentTeamComp = {"GK": 0, "DEF": 0, "MID": 0, "FOR": 0}

    # Placeholder for no. of points the final team is worth
    totalPoints = 0

    # Use n as our index for inserting rows into the selectedTeam dataframe, and to keep track of no. of players selected
    n = 0

    # Outer loop iterator
    i = 0

    tic = time.perf_counter()

    # Now iterate through the sorted list
    # One row = one player in the list
    
    # We only need to go through the list twice at max to determine if a valid team can be formed from the source file.
    while i < 2:
        i = i + 1

    # Variable to keep track of the cheapest player we've bought throughout the list, and use that as our maximum for selecting 
    # according to performance. Resets to current allowed budget if team size is not valid.
        maxPrice = budget

        for (idx, row) in sortedList.iterrows():

            # Break out of loop if n = max team size
            if n == maxTeam:
                break
            
            # First check that player's cost does not exceed budget and maximum price for player
            if row.loc['Cost'] < budget and row.loc['Cost'] < maxPrice:

                # Then check that the player's position is not full in the open team slots
                if checkTeamCompValid(validTeamComp, currentTeamComp, row.loc['Position'], row) == True:

                    # Once all conditions are met, store player's details in our team selection
                    selectedTeam.loc[n] = row.loc[columns]

                    totalPoints = totalPoints + row.loc['Points']

                    # Set max. price for purchasing another player to the current player's cost
                    maxPrice = row.loc['Cost']

                    # And subtract this cost from the total budget
                    budget = budget - maxPrice

                    # Remove selected player from our player database in case the loop needs to run again for invalid team size
                    sortedList=sortedList.drop(row.name)

                    # Finally, increment count of players selected
                    n = n + 1

    toc = time.perf_counter()
    print(f"\nSelection algorithm completed in {toc - tic:0.4f} seconds\n")
    
    checkTeamSize(n, maxTeam, selectedTeam)

    print(f"\nLeftover budget: {budget:0.2f}m")
    print(f"\nTotal points from team: {totalPoints}")

# Checks if team size = maxTeam, prints an error message if it's not
def checkTeamSize(n, maxTeam, selectedTeam):
    if (n != maxTeam):
        print("WARNING: Selected team size is invalid, possibly due to small input size or source file error. \nHere are the players the algorithm managed to select:")
  
    print(selectedTeam.to_string(index=False))
    writeCSV(selectedTeam)

# Output selected players to separate csv file
def writeCSV(team):
    team.to_csv('selectedTeam.csv', index=False)
    print("\nSelection written to new .csv file")
   
# debug function to print out variables to keep track of value changes
def debugPrint(varName, varValue):
    print(f"DEBUG: value of variable {varName} is {varValue}")

    
## ----- MAIN FUNCTION BELOW HERE -----

# take in filename as the 2nd command line argument
try:
    fileName = sys.argv[1]
except IndexError:
    print("\nERROR: no filename specified.")
    sys.exit(1)

else:

    try:
        # Load .csv contents from file and process them
        sortedList = loadCSV(fileName)

    except FileNotFoundError:
        print("\nERROR: There is no file with that name/filepath present. Please double-check the filename input and try again.") 
        sys.exit(1)
    else:
        
    # Ensure that file has at least points, cost and position columns; this is the minimum amount of data needed for the algorithm
    
    # Specify expected column labels from the source .csv file
        columns= list(sortedList.columns)
        validColumns = list(["Points", "Cost", "Position"])

        # Store number of  rows in the dataframe (minus the column labels)
        rowCount = sortedList[sortedList.columns[0]].count()

        #  The max no. of players there should be on the team in total
        maxTeam = 11

        # Check that source file has necessary data
        if all(item in columns for item in validColumns):
            # Check that file has at least 11 rows
            if (rowCount >= maxTeam):

                # Budget is in millions
                budget = 83.8

                # Reserve empty dataframe to store selected players, with same columns as .csv file
                selectedTeam = pd.DataFrame(columns=columns)

                # Call selection algorithm
                selectTeam(sortedList,selectedTeam, budget, columns, maxTeam)

            else:
                print(f"ERROR: Input file has less than {maxTeam} players. A valid team cannot be formed.")
                sys.exit(1)

        else:
            print("ERROR: source file does not contain a Points, Cost or Position column. This data is needed for the algorithm to function")
            sys.exit(1)