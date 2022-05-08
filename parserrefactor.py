# This file contains a parser which takes in SmartSHARK data and performs analyses #

import pymongo
from pycoshark.mongomodels import Commit, CommitChanges, Refactoring

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Database Name
db = client["smartshark_2_2"]

# Collection Names
commits = db["commit"]
commit_changes = db["commit_changes"]
refactorings = db["refactoring"]



y = commits.find({}, {'message': 1, 'committer_id': 1})    # Finds commits with messages & prints them

z = []

count = 0
count2 = 0

projects_byAuthorID = {}  # Commits with same author ID (person who made commit code)
projects_byCommitterID = {}  # Commits with same committer ID (person who made the commit)

for data in y:
    committerID = data['committer_id']
    message = data['message']

    # Committer ID
    if committerID in projects_byCommitterID:
        projects_byCommitterID[committerID].append(message)
    else:
        projects_byCommitterID[committerID] = [message]

totalBugs = 0
totalRefact = 0

for id in projects_byCommitterID:
    bugs = 0
    refactors = 0
    nextC = False
    for message in projects_byCommitterID[id]:
        if "refactor" in message or "Refactor" in message or "REFACTOR" in message or "rearrange" in message or "Rearrange" in message or "REARRANGE" in message or "restructure" in message or "Restructure" in message or "RESTRUCTURE" in message or "streamline" in message or "Streamline" in message or "STREAMLINE" in message or "redesign" in message or "Redesign" in message or "REDESIGN" in message or "alter" in message or "Alter" in message or "ALTER" in message:
            refactors += 1
            totalRefact += 1
            print("This is a refactor commit")
            print(message)
            nextC = True
        elif nextC:
            if "bug" in message or "Bug" in message or "BUG" in message or "fix" in message or "Fix" in message or "FIX" in message:
                bugs += 1
                totalBugs += 1
                print("This is the following bug commit")
                print(message)
            nextC = False
    if refactors > 0:
        print(f"Refactor commits: {refactors}")
        print(f"Bug commits: {bugs}")

print(f"Total refactor commits: {totalRefact}")
print(f"Total bug commits: {totalBugs}")