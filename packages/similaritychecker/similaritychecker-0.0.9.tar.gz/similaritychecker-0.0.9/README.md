# SimilarityChecker
A Python similarity checker
V.0.0.9 | Made by: Jekkow

# What does this module:
This module compares strings on similarity and returns the name and a float percentage

# How to use:
	Import the module:
	from similaritychecker import checker
	
    Create the Constructor:
        SC = checker()

    Set Values:
        SC.Set_Difference =
            (Default = 1)
        SC.Length_Difference =
            (Default = 2)
        SC.Minimum_Percentage =
            (Default = 0.75)

    Use the Check method:
        SC.Check("string*", ["List*"])
        String* = string that needs to be compared
        List* =  List that contains the word(s) that the string will be compared with