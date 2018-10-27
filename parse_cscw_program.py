# -*- coding: utf-8 -*-

import csv

# loads the confer DATA sheet
def get_confer_data():

    # list of rows in the DATA sheet
    paper_list = []
    with open('confer_data.csv', encoding="latin-1") as r_events:
        reader = csv.DictReader(r_events, delimiter=',', quotechar='"')
        for row in reader:
            paper_list.append(row)
    # for row in paper_list:
    #     print(row['Paper Number'], row["Title"], row["S Name"])

        write_people_file(paper_list)
        write_sessions_file(paper_list)



# generates the people.csv file
def write_people_file(paper_list):
    with open('people.csv', 'w', encoding="utf-8") as people_file:
        fieldnames = [
            "User Id",
            "First name",
            "Middle initial",
            "Last name"
        ]

        writer_people = csv.DictWriter(people_file, fieldnames=fieldnames)

        # adds the header row to the file
        head_row={}
        for item in fieldnames:
            head_row[item] = item
        writer_people.writerow(head_row)

        # list of authors
        author_list =[]

        # go through each item in the paper list and extract the authors
        for row in paper_list:
            for i in range(1, 17):
                author = {}
                if (row["Author " + str(i) + " - last"] != ""):
                    # new_row will have the values that need to be added in the people file for this row
                    new_row = {}
                    new_row["User Id"] = "TODO User Id" # TODO this needs to get replaced with whatever value should go here
                    new_row["First name"] = row["Author " + str(i) + " - first"]
                    new_row["Middle initial"] = row["Author " + str(i) + " - middle"]
                    new_row["Last name"] = row["Author " + str(i) + " - last"]
                    writer_people.writerow(new_row)

def initialize_session(session_id):
    session = {}
    session["Session ID"] = session_id
    session["Name"] = ""
    session["Type"] = ""
    session["Date (yyyy-MM-dd)"] = ""
    session["Start time (HH:mm in 24-h format)"]  = ""
    session["End time (HH:mm in 24-h format)"] = ""
    session["Room"] = ""
    session["Paper Ids"] = ""
    session["Session Chair Ids"] = ""

    return(session)

# output needs to be in the format: (yyyy-MM-dd)
# input is in the format 11/06
def parse_date(mydate):
    temp = mydate.split("/")
    new_date = "2018-11-" + temp[1]
    return new_date

# output needs to be in the format (HH:mm in 24-h format)
# the input is in the format "11:00 AM"
def parse_time(time):
    temp = time.split(" ")
    print(temp)
    if (temp[1] == "AM"):
        new_time = temp[0]
    if (temp[1] == "PM"):
        pm_time = temp[0].split(":")
        # replace the 01, 02, 03 values to numbers
        pm_time[0].replace("07","7").replace("08", "8").replace("09","9")
        if(pm_time[0] != "12"):
            pm_time[0] = int(pm_time[0]) + 12
        new_time = str(pm_time[0]) + ":" + pm_time[1]
    print(time, new_time)
    return new_time


# generates the sessions.csv file
def write_sessions_file(paper_list):
    with open('sessions.csv', 'w', encoding="utf-8") as sessions_file:

        fieldnames = [
            "Session ID",
            "Name",
            "Type",
            "Date (yyyy-MM-dd)",
            "Start time (HH:mm in 24-h format)",
            "End time (HH:mm in 24-h format)",
            "Room",
            "Paper Ids", # (Separate papers with semicolon),
            "Session Chair Ids" # (Separate chairs with semicolon)
        ]

        writer_session = csv.DictWriter(sessions_file, fieldnames=fieldnames)

        head_row={}
        for item in fieldnames:
            head_row[item] = item
        writer_session.writerow(head_row)

        # list of session
        session_list = []

        session = {}
        # initialize the data for all the session
        for row in paper_list:
            # initializes various strings about the session to empty to
            # make it easier to append multiple values to them
            session[row["S #"]] = initialize_session(row["S #"])

        # go through each item in the paper list and create
        # a dictionary of sessions, with the key being the session S #
        # go through the list of papers and add each paper that matches this particular session number
        for row in paper_list:
            session[row["S #"]]["Name"] = row["S Name"]
            session[row["S #"]]["Type"] = "TODO_Type" # TODO this needs to be updated with the appropriate infor
            session[row["S #"]]["Date (yyyy-MM-dd)"] = parse_date(row["Day"])
            session[row["S #"]]["Start time (HH:mm in 24-h format)"] = parse_time(row["Session Start Time"])
            session[row["S #"]]["End time (HH:mm in 24-h format)"] = parse_time(row["S End"])
            session[row["S #"]]["Room"] = row["Room"]
            session[row["S #"]]["Paper Ids"] = str(row["Paper Number"]) + ";" + str(session[row["S #"]]["Paper Ids"])   # TODO (Separate papers with semicolon),
            session[row["S #"]]["Session Chair Ids"] = "TODO_chair" # TODO (Separate chairs with semicolon)

        for key in session:
            writer_session.writerow(session[key])


get_confer_data()
