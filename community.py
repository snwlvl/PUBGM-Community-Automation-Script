!pip install pygsheets
!pip install pandas
import pygsheets
import time
import datetime
import pandas as pd

''' ---------------------------------------------------------------------------------------------------------- '''
def dublicated(teamNames, sheet_data):
    DoneRowsIndexes = []
    for i, currRow in enumerate(sheet_data):
        if currRow == []:
            continue
        indexes = [];
        for j, teamName in enumerate(teamNames):
            if currRow[2] == teamName:
                indexes.append(j + 1)
        indexes.sort(reverse=True)
        if len(indexes) > 1:
            for i in indexes:
                if i == max(indexes) or i in DoneRowsIndexes:
                    continue
                DoneRowsIndexes.append(i)
            update_or_create_worksheet(Spreedsheet, 'Duplicated', currRow)
            time.sleep(1)
            sheet_data = RegSheet.get_all_values(returnas='matrix', include_tailing_empty=False)
    DoneRowsIndexes.sort(reverse=True)
    for i in DoneRowsIndexes:
        RegSheet.delete_rows(i)
        del sheet_data[i - 1]
        time.sleep(1)
    return sheet_data


# Check if string is numeric
def is_numeric_string(s):
    try:
        int(s)  # Try to convert to an integer
        return True
    except ValueError:
        return False


# Update or create worksheet:
def update_or_create_worksheet(spreadsheet, title, row_data):
    if title in datas.keys():
        datas[title].append(row_data)
    else:
        placeholder = [row_data]
        datas[title] = placeholder

def write_in_worksheets(rows_data, row_title):
    if sheet_exists(Spreedsheet, row_title):
        worksheet = Spreedsheet.worksheet_by_title(row_title)
    else:
        worksheet = Spreedsheet.add_worksheet(title=row_title)

    worksheet = Spreedsheet.worksheet_by_title(row_title)
    df = pd.DataFrame(rows_data)
   
    df = df.fillna('')
    worksheet.set_dataframe(df, (1, 1), copy_head=False, fit=True)


# Check if a team played last week
def team_PLW(row):
    # pids = [row[11], row[11], row[15], row[19], row[23], row[27]]
    # pids = [pid for pid in pids if pid != ""]
    tName = row[2].upper()
    tDiscords = row[4]
    if tName in teams_played_last_week_Names and tDiscords in teams_played_last_week_Discords:
        update_or_create_worksheet(Spreedsheet, 'PlayedPW', row)
        return True

    #   tDiscords = [row[4],row[5]]
    #   for tDiscord in tDiscords:
    #     #pid = ''.join(char for char in pid if char.isdigit())
    #     if tDiscord in teams_played_last_week_Discords:
    #       update_or_create_worksheet(Spreedsheet, 'PlayedPW', [row])
    #       time.sleep(1)
    #       return True
    #   #print('PlayedPW.')
    return False


# Check if sheet exists:
def sheet_exists(spreadsheet, sheet_name):
    # Check if a sheet with the specified name exists in the given spreadsheet.
    # List all sheet titles in the spreadsheet
    sheet_titles = [sheet.title for sheet in spreadsheet.worksheets()]
    # Check if sheet_name is among the sheet titles
    return sheet_name in sheet_titles


# Check if player is banned:
def player_BL(row, BL_PIDs):
    pids = [row[11], row[30], row[15], row[19], row[23], row[27]]
    pids = [pid for pid in pids if pid != ""]
    for pid in pids:
        pid = ''.join(char for char in pid if char.isdigit())
        if pid in BL_PIDs:
            update_or_create_worksheet(Spreedsheet, 'BlackListed', row)
            return True
            # print(BL_PIDs)
    # print('No banned players found.')
    return False


# Check if someone has a Korean account:
# def isKoreanAcc(row):
#     pids = [row[11], row[31], row[15], row[19], row[23], row[27]]
#     pids = [pid for pid in pids if pid != ""]
#     for pid in pids:
#         if not is_numeric_string(pid) or not pid.startswith('5'):
#             update_or_create_worksheet(Spreedsheet, 'Korean Accounts', row)
#             time.sleep(1)
#             return True
#     return False

# Check if someone is younger than 18:
# def isYoungerThan18(row):
#     youngCount = 0
#     bDays = [row[33], row[29], row[13], row[17], row[21], row[25]]
#     bDays = [bDay for bDay in bDays if bDay != ""]
#     today = datetime.date.today()
#     for bDay in bDays:
#         try:
#             birthdate = datetime.datetime.strptime(bDay, '%m/%d/%Y').date()
#             age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
#             if age < 18:
#                 youngCount = youngCount +1
#         except ValueError:
#             continue
#     if youngCount > 0:
#         if youngCount != int(row[35]):
#             update_or_create_worksheet(Spreedsheet, 'YoungerThan18', row)
#             time.sleep(1)
#             return True
#         update_or_create_worksheet(Spreedsheet, 'YoungerThan18', row)
#         time.sleep(1)
#         return False
#     return False

def isYoungerThan18(row):
    youngCount = 0
    bDays = [row[33], row[29], row[13], row[17], row[21], row[25]]
    bDays = [bDay for bDay in bDays if bDay != ""]
    today = datetime.date.today()
    for bDay in bDays:
        try:
            birthdate = datetime.datetime.strptime(bDay, '%m/%d/%Y').date()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if age < 18:
                youngCount = youngCount + 1
        except ValueError:
            continue


    if youngCount > 0:
        underage_count = int(row[35])
        if youngCount > underage_count:
            update_or_create_worksheet(Spreedsheet, 'YoungerThan18', row)
            return True
        update_or_create_worksheet(Spreedsheet, 'YoungerThan18', row)
        return False
    return False


# # Calculate age:
# def calculate_age(birthdate):
#     today = datetime.date.today()
#     try:
#         birthdate = datetime.datetime.strptime(birthdate, '%m/%d/%Y').date()
#         age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
#         return age
#     except ValueError:
#         return -1

# # Check if someone is younger than 18:
# def isYongerThan18(row):
#     bDays = [row[33], row[29], row[13], row[17], row[21], row[25]]
#     bDays = [bDay for bDay in bDays if bDay != ""]
#     for bDay in bDays:
#         if calculate_age(bDay) < 18:
#             update_or_create_worksheet(Spreedsheet, 'YongerThan18', [row])
#             time.sleep(1)
#             return True
#     return False



# Check if tag dublicated:
def tagDublicated(tags, sheet_data, worksheet):
    DoneRowsIndexes = []
    for i, currRow in enumerate(sheet_data):
        if currRow == []:
            continue
        indexes = [];
        for j, tag in enumerate(tags):
            if currRow[3] == tag:
                indexes.append(j + 1)
        indexes.sort(reverse=True)
        if len(indexes) > 1:
            for i in indexes:
                if i == min(indexes) or i in DoneRowsIndexes:
                    continue
                DoneRowsIndexes.append(i)
            update_or_create_worksheet(Spreedsheet, 'TagsDuplic', currRow)
            sheet_data = RegSheet.get_all_values(returnas='matrix', include_tailing_empty=False)
    for i in DoneRowsIndexes:
        row_to_update = sheet_data[i - 1]
        if row_to_update == []:
            print (row_to_update)
            continue
        print (row_to_update)
        row_to_update[3] = row_to_update[3] + str(i)
        startRow = 'A' + str(i)
        worksheet.update_values(crange=startRow, values=[row_to_update], majordim='ROWS')
        sheet_data = RegSheet.get_all_values(returnas='matrix', include_tailing_empty=False)
        time.sleep(1)
    return sheet_data


# Check if in AMB or Clans
def check_amb_clans(row,names):
    print(row[2])
    if row[2].lower() in names:
        update_or_create_worksheet(Spreedsheet, 'In clans/amb', row)
        return True
    return False


''' ---------------------------------------------------------------------------------------------------------- '''
# Read all data from sheets:
# Create Regestration Sheet:
gc = pygsheets.authorize(service_file='pubgmcommunity-REDACTED.json')
Spreedsheet = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/REDACTED/edit#gid=350330230')
RegSheet = Spreedsheet[0]
sheet_data = RegSheet.get_all_values(returnas='matrix', include_tailing_empty=False)

# Create AMB Sheet:
AMB_Sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/REDACTED/edit')[
    0]
AMB_Sheet_data = AMB_Sheet.get_all_values(returnas='matrix', include_tailing_empty=False)
AMB_Sheet_data = [team for team in AMB_Sheet_data if team != []]
clans_sheet = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/REDACTED/edit#gid=920999062')[0]
clans_sheet_data = clans_sheet.get_all_values(returnas='matrix', include_tailing_empty=False)
clans_sheet_data = [team for team in clans_sheet_data if team != []]

# Create Black List and remove empty cells from it:
BL_Sheet = \
gc.open_by_url('https://docs.google.com/spreadsheets/d/REDACTED/edit?gid=0#gid=0')[0]
BL_Names = BL_Sheet.get_col(1, include_tailing_empty=False)
BL_Names = [name for name in BL_Names if name != ""]
BL_Tags = BL_Sheet.get_col(2, include_tailing_empty=False)
BL_Tags = [Tag for Tag in BL_Tags if Tag != ""]
BL_Discord = BL_Sheet.get_col(4, include_tailing_empty=False)
BL_Discord = [Discord for Discord in BL_Discord if Discord != ""]
BL_PIDs = BL_Sheet.get_col(9, include_tailing_empty=False) + BL_Sheet.get_col(11,
                                                                              include_tailing_empty=False) + BL_Sheet.get_col(
    13, include_tailing_empty=False) + BL_Sheet.get_col(15, include_tailing_empty=False) + BL_Sheet.get_col(17,
                                                                                                            include_tailing_empty=False) + BL_Sheet.get_col(
    19, include_tailing_empty=False)
BL_PIDs = [PID for PID in BL_PIDs if PID != ""]
# print(BL_PIDs)

# Create Last Week Sheet:
last_week_sheet = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/REDACTED/edit#gid=1445156396')[4]
teams_played_last_week_Names = last_week_sheet.get_col(1, include_tailing_empty=False)
teams_played_last_week_Names = [name for name in teams_played_last_week_Names if name != ""]
teams_played_last_week_Names = [name.upper() for name in teams_played_last_week_Names]
print(teams_played_last_week_Names)
teams_played_last_week_Tags = last_week_sheet.get_col(2, include_tailing_empty=False)
teams_played_last_week_Tags = [Tag for Tag in teams_played_last_week_Tags if Tag != ""]
teams_played_last_week_Discords = last_week_sheet.get_col(3, include_tailing_empty=False) + last_week_sheet.get_col(4,
                                                                                                                    include_tailing_empty=False)
teams_played_last_week_Discords = [Discord for Discord in teams_played_last_week_Discords
                                   if (isinstance(Discord, (int, float)) or (
                isinstance(Discord, str) and is_numeric_string(Discord))) and Discord != ""]
# print(teams_played_last_week_Discords)
''' ---------------------------------------------------------------------------------------------------------- '''

# Main function to call the functions
accesptedTeams = []
datas = {}
def reminder():
    reminder_input = input('Did you change the previous teams? ')
    if reminder_input.lower() in ['y', 'yes']:
        return
    else:
        print('Please make sure you did change the previous week list.')
        reminder()

reminder()

timestart = datetime.datetime.now()
# Create from AMB and Clans
clanNames = []
for team in AMB_Sheet_data:
    clanNames.append(team[2].lower())
for team in clans_sheet_data: 
    clanNames.append(team[2].lower())
print(clanNames)
teamNames = RegSheet.get_col(3, include_tailing_empty=False)
# Remove duplicates
sheet_data = dublicated(teamNames, sheet_data)
# Update Tag Dublicates
# Get the team names and tags

tags = RegSheet.get_col(4, include_tailing_empty=False)
sheet_data = tagDublicated(tags,sheet_data, RegSheet)

# Loop through the rows
for currRow in (sheet_data):
    if currRow == [] or len(currRow)<10:
        continue
    #Black list checking
    isBL = player_BL(currRow, BL_PIDs)
    #Last week checking
    didPlay = team_PLW(currRow)
    #Korean checking
    # isKorean = isKoreanAcc(currRow)
    #Younger than 18
    isYoung = isYoungerThan18(currRow)
    #Check if in AMB or Clans
    isClansOrAmb = check_amb_clans(currRow,clanNames)
    # Add accepted teams
    if isBL or didPlay or isYoung:
        continue
    accesptedTeams.append(currRow)
# Push all accepted teams at once
for row in accesptedTeams:
    update_or_create_worksheet(Spreedsheet, 'Accepted Teams', row)
for key in datas.keys():
    write_in_worksheets(datas[key], key)
endtime = datetime.datetime.now()
print("it took me " + str(endtime- timestart))