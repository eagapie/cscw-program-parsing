# -*- coding: utf-8 -*-

import csv

# loads the confer DATA sheet
def get_confer_data():
    with open('confer_data.csv', encoding="latin-1") as r_events:
        reader = csv.DictReader(r_events, delimiter=',', quotechar='"')

    # for row in reader:
    #     print(row['Paper Number'], row["Title"], row["S Name"])

        write_people_file(reader)

    return reader



def write_people_file(reader):
    with open('people.csv', 'w', encoding="utf-8") as people_file:
        fieldnames = [
            "User Id",
            "First name",
            "Middle initial",
            "Last name"
        ]

        writer = csv.DictWriter(people_file, fieldnames=fieldnames)

        head_row={}
        for item in fieldnames:
            head_row[item] = item
            print(head_row)
        writer.writerow(head_row)

        # list of authors
        author_list =[]

        # go through each item in the paper list and extract the authors
        for row in reader:
            for i in range(1, 17):
                author = {}
                if (row["Author " + str(i) + " - last"] != ""):
                    author["First name"] = row["Author " + str(i) + " - first"]
                    author["Middle initial"] = row["Author " + str(i) + " - middle"]
                    author["Last name"] = row["Author " + str(i) + " - last"]
                    author_list.append(author)
                    


        for author in author_list:
            new_row = {}
            new_row["User Id"] = "User Id" # TODO this needs to get replaced with whatever value should go here
            new_row["First name"] = author["First name"]
            new_row["Middle initial"] = author["Middle initial"]
            new_row["Last name"] = author["Last name"]
            writer.writerow(new_row)



reader = get_confer_data()


#
#
# def get_activity_details(pid, day_no):
#   with open('client_daily_reasons.csv') as r_reasons:
#     reader = csv.DictReader(r_reasons, delimiter=',', quotechar='"')
#
#
#     return 1
#
#
# def process_client_activity_reports(file_name):
#   with open(file_name, 'w') as csvfile:
#     fieldnames = [
#
#
#     ]
#
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#     head_row={}
#     for item in fieldnames:
#       head_row[item] = item
#
#
#     writer.writerow(head_row)
#
#     for pid in participant_list:
#       new_row = {}
#
#       new_row['pid'] = pid
#
#
#       writer.writerow(new_row)
