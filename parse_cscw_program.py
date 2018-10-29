# -*- coding: utf-8 -*-

import csv

# loads the confer DATA sheet
def get_confer_data():

    # list of rows in the DATA sheet
    paper_list = []
    with open('confer_data_with_authors.csv', encoding="utf-8") as r_papers:
        reader = csv.DictReader(r_papers, delimiter=',', quotechar='"')
        for row in reader:
            paper_list.append(row)

        write_people_file(paper_list)
        write_sessions_file(paper_list)
        write_affiliations_file(paper_list)
        write_papers_file(paper_list)

# generate author list ids based on the row entry for this paper
def generate_author_list(row):
    author_list = []

    # through the 16 possible authors and generate list of authors
    for i in range(1, 17):
        if (row["Author " + str(i) + " - last"] != ""):
            new_author = {}
            new_author["First name"] = row["Author " + str(i) + " - first"]
            new_author["Middle initial"] = row["Author " + str(i) + " - middle"]
            new_author["Last name"] = row["Author " + str(i) + " - last"]
            author_list.append(new_author)

    # read the people list from people.csv
    people_list = []
    with open('people.csv', encoding="utf-8") as r_people:
        people_reader = csv.DictReader(r_people, delimiter=',', quotechar='"')
        for row in people_reader:
            people_list.append(row)

    author_ids = ""
    # get the author id from people list
    for item_people in people_list:
        for item_author in author_list:
            if (item_author["First name"] == item_people["First name"] and
                item_author["Middle initial"] == item_people["Middle initial"] and
                item_author["Last name"] == item_people["Last name"]):
                # append author id to the list of author ids
                author_ids = item_people["User Id"] + ";" + author_ids

    # strip the last semicolon
    author_ids = author_ids.strip(";")
    return author_ids


# generates the papers.csv file
def write_papers_file(paper_list):
    with open('papers.csv', 'w', encoding="utf-8") as papers_file:
        fieldnames = [
            "﻿Paper Id",
            "Title",
            "Abstract",
            "Type", # Mauro said:  you can set it all to "paper".
            "Award", #  (BEST_PAPER/HONORABLE_MENTION or leave empty)
            "Author ID", # (Separate authors with semicolon)
        ]

        writer_papers = csv.DictWriter(papers_file, fieldnames=fieldnames)

        # adds the header row to the file
        head_row={}
        for item in fieldnames:
            head_row[item] = item
        writer_papers.writerow(head_row)

        # go through each item in the paper list and create the row for papers.csv
        for row in paper_list:
            new_row = {}

            new_row["﻿Paper Id"] = row["Paper Number"]
            new_row["Title"] = row["Title"]
            new_row["Abstract"] = row["Abstract"]
            new_row["Type"] = "Papers" # Mauro said:  you can set it all to "paper".
            new_row["Award"] = row["Award"]
            new_row["Author ID"] = generate_author_list(row)
            writer_papers.writerow(new_row)

# check if the new author exists in the author list already or # NOTE:
def is_new_entry_in_author_list(new_author, author_list):
    for item in author_list:
        if(new_author["First name"] == item["First name"] and
            new_author["Middle initial"] == item["Middle initial"] and
            new_author["Last name"] == item["Last name"]):
            return False # this author has been found, return false

    # the author was not found in the list
    return True

# get the list of people who are chairs but not authors
def get_chairs_not_authors():
    chairs = []
    with open('chairs_not_authors.csv', encoding="utf-8") as r_chair_not_author:
        reader_chairs_not_author = csv.DictReader(r_chair_not_author, delimiter=',', quotechar='"')
        for row in reader_chairs_not_author:
            chairs.append(row)
    return chairs

# generates the people.csv file
def write_people_file(paper_list):
    with open('people.csv', 'w', encoding="utf-8") as people_file:
        fieldnames = [
            "User Id", # we generate this, it doesn't come from the DATA sheet
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
        author_list = []

        author_index = 0
        # go through each item in the paper list and extract the authors
        for row in paper_list:
            for i in range(1, 17):
                author_index = author_index + 1
                author = {}
                if (row["Author " + str(i) + " - last"] != ""):
                    # new_row will have the values that need to be added in the people file for this row
                    new_row = {}
                    new_row["User Id"] = author_index
                    new_row["First name"] = row["Author " + str(i) + " - first"]
                    new_row["Middle initial"] = row["Author " + str(i) + " - middle"]
                    new_row["Last name"] = row["Author " + str(i) + " - last"]
                    if (is_new_entry_in_author_list(new_row, author_list)):
                        author_list.append(new_row)

        # append all chairs of sessions who are not authors
        chairs = get_chairs_not_authors()

        for row in chairs:
            author_index = author_index + 1
            new_row = {}
            new_row["User Id"] = author_index
            new_row["First name"] = row["First name"]
            new_row["Middle initial"] = ""
            new_row["Last name"] = row["Last name"]
            if (is_new_entry_in_author_list(new_row, author_list)):
                author_list.append(new_row)

        # write all people to file
        for item in author_list:
            writer_people.writerow(item)


# output: a list of affiliations separated by semicolon
# input of the type: Zhicong Lu: University of Toronto; Seongkook Heo: University of Toronto; Daniel J Wigdor: University of Toronto
def parse_affiliations(text, paper_id):
    affiliation_str = ""
    affiliation_list = []
    temp = text.split(";") # separates all author:affiliation
    if(temp):
        for item in temp:
            if (item != "NA"):
                if(item[1] != ""):
                    temp_affiliation = item.split(":")  # separates
                    affiliation = temp_affiliation[1]
                    affiliation_list.append(affiliation)
                    # when the affiliation is not actually listed
                    # if(temp_affiliation[1] == ""):
                    #     print(paper_id + ",")

    # create uniques list of affiliations
    unique_affiliation = []
    for item in affiliation_list:
        if item not in unique_affiliation:
            unique_affiliation.append(item)
            affiliation_str =  item + '; ' + affiliation_str

    # strip the ; at the end
    affiliation_str = affiliation_str.strip(" ").strip(";")
    return(affiliation_str)

# row["ACM Author Affiliations"], new_author["First name"], new_author["Last name"]
def get_author_affiliation(acm_affiliations, first_name, last_name):
    if(acm_affiliations == "NA"):
        return "NA"
    temp = acm_affiliations.split(";") # separates all author:affiliation
    if(temp):
        for item in temp:
            if (item != "NA"):
                if((first_name in item) and (last_name in item)):
                    temp_affiliation = item.split(":")  # separates
                    affiliation = temp_affiliation[1]
                    return affiliation
    return ""

def write_affiliations_file(paper_list):
    with open('affiliations.csv', 'w', encoding="utf-8") as affiliations_file:
        fieldnames = [
            "Paper Id",
            "User Id",
            "Institution",
        ]

        writer_affiliations = csv.DictWriter(affiliations_file, fieldnames=fieldnames)

        # adds the header row to the file
        head_row={}
        for item in fieldnames:
            head_row[item] = item
        writer_affiliations.writerow(head_row)

        # affiliations dictionary by paper id
        affiliations = {}

        # go through each item in the paper list and extract the affiliations
        for row in paper_list:
            new_row = {}
            new_row["Paper Id"] = row["Paper Number"]

            # get the list of authors
            for i in range(1, 17):
                if (row["Author " + str(i) + " - last"] != ""):
                    new_author = {}
                    new_author["First name"] = row["Author " + str(i) + " - first"]
                    new_author["Middle initial"] = row["Author " + str(i) + " - middle"]
                    new_author["Last name"] = row["Author " + str(i) + " - last"]

                    # go through the list of authors in ACM Author Affiliations and extract their affiliation and their user id
                    new_row["User Id"] = get_author_id(new_author["First name"], new_author["Last name"])
                    new_row["Institution"] = get_author_affiliation(row["ACM Author Affiliations"], new_author["First name"], new_author["Last name"])
                    # print(new_row["Institution"])
                    writer_affiliations.writerow(new_row)

# generates the affiliations.csv file
def write_affiliations_file_old(paper_list):
    with open('affiliations.csv', 'w', encoding="utf-8") as affiliations_file:
        fieldnames = [
            "Paper Id",
            "User Id",
            "Institution",
        ]

        writer_affiliations = csv.DictWriter(affiliations_file, fieldnames=fieldnames)

        # adds the header row to the file
        head_row={}
        for item in fieldnames:
            head_row[item] = item
        writer_affiliations.writerow(head_row)

        # affiliations dictionary by paper id
        affiliations = {}

        # go through each item in the paper list and extract the affiliations
        for row in paper_list:
            new_row = {}
            new_row["Paper Id"] = row["Paper Number"]
            new_row["User Id"] = get_first_author_id(row["Paper Number"])
            new_row["Institution"] = parse_affiliations(row["ACM Author Affiliations"], row["Paper Number"])
            print(new_row["Institution"])
            writer_affiliations.writerow(new_row)

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
    if (temp[1] == "AM"):
        new_time = temp[0]
    if (temp[1] == "PM"):
        pm_time = temp[0].split(":")
        # replace the 01, 02, 03 values to numbers
        pm_time[0].replace("07","7").replace("08", "8").replace("09","9")
        if(pm_time[0] != "12"):
            pm_time[0] = int(pm_time[0]) + 12
        new_time = str(pm_time[0]) + ":" + pm_time[1]
    return new_time

# gets people id for this particular chair from first and last neme
def get_chair_id(first_name, last_name):
    # get people list
    # read the people list from people.csv
    people_list = []
    with open('people.csv', encoding="utf-8") as r_people:
        people_reader = csv.DictReader(r_people, delimiter=',', quotechar='"')
        for row in people_reader:
            people_list.append(row)

    for item_people in people_list:
        if (first_name == item_people["First name"] and
            last_name == item_people["Last name"]):
            # append author id to the list of author ids
            return item_people["User Id"]

    # check if this person is in the people list, if it is return the id
    return " "

def get_author_id(first_name, last_name):

    # get people list
    # read the people list from people.csv
    people_list = []
    with open('people.csv', encoding="utf-8") as r_people:
        people_reader = csv.DictReader(r_people, delimiter=',', quotechar='"')
        for row in people_reader:
            people_list.append(row)

    for item_people in people_list:
        if (first_name == item_people["First name"] and
            last_name == item_people["Last name"]):
            # append author id to the list of author ids
            return item_people["User Id"]

    # check if this person is in the people list, if it is return the id
    return " "

# dictionary of sessions with chair names (first and last)
def get_sessions_with_chair_names_dict():
    session_w_chairs_list = []
    chairs_dict = {}
    with open('sessions_with_chair_names.csv', encoding="utf-8") as r_session_w_chair:
        reader_session_w_chair = csv.DictReader(r_session_w_chair, delimiter=',', quotechar='"')
        for row in reader_session_w_chair:
            session_w_chairs_list.append(row)

    for item in session_w_chairs_list:
        chairs_dict[item["Session ID"]] = {}
        chairs_dict[item["Session ID"]]["Session ID"] = item["Session ID"]
        chairs_dict[item["Session ID"]]["Session Chair Ids"] = ""
        chairs_dict[item["Session ID"]]["Type"] = item["Type"]

        # if there are several chairs in the list
        if(item["Session Chair Ids"].strip(";") == "NA"):
            chairs_dict[item["Session ID"]]["Session Chair Ids"] = "NA"
        else:
            chair_list = item["Session Chair Ids"].strip(";").split(";")
            for item_chair in chair_list:
                # if id is NA return
                if(item_chair == "NA"):
                    chairs_dict[item["Session ID"]]["Session Chair Ids"] = "NA"
                else:
                    # each name gets parsed in first and last name
                    chair_name = item_chair.split(" ")
                    chair_id = get_chair_id(chair_name[0], chair_name[1])
                    print(chair_id + " " + chair_name[0] + " " + chair_name[1])
                    chairs_dict[item["Session ID"]]["Session Chair Ids"] = chair_id + ";" + chairs_dict[item["Session ID"]]["Session Chair Ids"]


    return chairs_dict

# generates the sessions.csv file
def write_sessions_file(paper_list):
    with open('sessions.csv', 'w', encoding="utf-8") as sessions_file:

        fieldnames = [
            "Session ID",
            "Name",
            "Type", # Mauro said we can set all to Papers
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

        session = {}
        # initialize the data for all the session
        for row in paper_list:
            # initializes various strings about the session to empty to
            # make it easier to append multiple values to them
            session[row["S #"]] = initialize_session(row["S #"])

        session_chairs_dict = get_sessions_with_chair_names_dict()
        # print(session_chairs_dict)

        # go through each item in the paper list and create
        # a dictionary of sessions, with the key being the session S #
        # go through the list of papers and add each paper that matches this particular session number
        for row in paper_list:
            session[row["S #"]]["Name"] = row["S Name"]
            session[row["S #"]]["Type"] = session_chairs_dict[row["S #"]]["Type"] # TODO this needs to be updated with the appropriate infor
            session[row["S #"]]["Date (yyyy-MM-dd)"] = parse_date(row["Day"])
            session[row["S #"]]["Start time (HH:mm in 24-h format)"] = parse_time(row["Session Start Time"])
            session[row["S #"]]["End time (HH:mm in 24-h format)"] = parse_time(row["S End"])
            session[row["S #"]]["Room"] = row["Room"]
            session[row["S #"]]["Paper Ids"] = str(row["Paper Number"]) + ";" + str(session[row["S #"]]["Paper Ids"])
            session[row["S #"]]["Session Chair Ids"] = str(session_chairs_dict[row["S #"]]["Session Chair Ids"]).strip(";")
            # print(session_chairs_dict[row["S #"]]["Session Chair Ids"])
        for key in session:
            session[key]["Paper Ids"] = session[key]["Paper Ids"].strip(";")
            writer_session.writerow(session[key])


get_confer_data()
