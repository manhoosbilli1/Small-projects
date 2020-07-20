import os
import csv
from firebase import firebase
from datetime import datetime
import PySimpleGUI as sg


day = ""
date = ""
salary = 0
# Retrive data form Firebase
firebase = firebase.FirebaseApplication(
    "https://citapp-65efb.firebaseio.com", None)
######################################## 

p = '2020-07-15'
##########################################

sg.theme('DarkAmber')
sg.set_options(element_size=200)
layout = [[sg.Text("Please type day")],
          [sg.InputText(key='day',
          enable_events=True,
          justification='center',
          size=(30,1))],

          [sg.Text("Please type salary")], 
          [sg.InputText(key='salary',
          enable_events=True,
          justification='center',
          size=(30,1))],


          [sg.Text("Please type date")],
          [sg.InputText(key='date',
          enable_events=True,
          justification='center',
          size=(30,1)), 
          sg.CalendarButton('Pick a date',close_when_date_chosen=True, 
                                            target='date',
                                            location=(0,0),
                                            no_titlebar=False,
                                            format='%y-%m-%d',)],


          [sg.Button(button_text='Generate'), sg.Button('Display Report')],

          [sg.Cancel()]]
 

window = sg.Window('File Generator', layout)


def list_duplicates(dtlist, p):

    nodup = []

    for name in dtlist:
        if dtlist.count(name) > 1:
            if name not in nodup:
                nodup.append(name)
        elif dtlist.count(name) < 2:
            nodup.append(name)
    if p in nodup:
        return p

#########################################


def convert(ott):
    import datetime
    return str(datetime.timedelta(seconds=ott))

####FUNCTION#####


def overtimeSalary(twh):
    wh = str(twh)
    h, m, s = wh.split(':')
    totalhour = int(h) + int(m) / 60 + int(s)/3600
    overtime = totalhour-7.0
    ott = int(overtime * 60 * 60)
    ovt = convert(ott)
    if overtime > 0:
        total_sal = overtime*float(sal)
        #print("                OverTime = ",ovt)
        #print("        Extratime salary = ",total_sal)
    else:
        ovt = "No OverTime"
        total_sal = "N/A"
    return ovt, total_sal


##########################################

def calculations(date, mylist, tlist, namee, sal):

    duplicates = []
    st = 'Present'

    FMT = '%H:%M:%S'
    overtime = 0.0
    indexlist = [i for i in range(len(mylist)) if mylist[i] == date]
    if len(indexlist) == 1:
        t1 = tlist[indexlist[0]]
        t2 = 'Missing'
        twh, OT, OTS = 'None', 'None', 'None'
        print("         Attendance Date = ", date)
        print("Starting attendance time = ", t1)
        print(" Ending attendance time  = ", t2)
    elif len(indexlist) > 1:
        t1 = (tlist[indexlist[0]])
        t2 = (tlist[indexlist[-1]])
        if t2 > t1:
            twh = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
            print("         Attendance Date = ", date)
            print("Starting attendance time = ", t1)
            print("  Ending attendance time = ", t2)
            print("       Total Woking time = ", twh)
            OT, OTS = overtimeSalary(twh)
            print(" ", sep='\n')

        elif t1 > t2:
            twh = datetime.strptime(t1, FMT) - datetime.strptime(t2, FMT)
            print("         Attendance Date = ", date)
            print("Starting attendance time = ", t1)
            print("  Ending attendance time = ", t2)
            print("       Total Woking time = ", twh)
            OT, OTS = overtimeSalary(twh)
            print(" ", sep='\n')
    cre(namee, st, t1, t2, twh, OT, OTS)


##########################################
def cre(namee, st, t1, t2, twh, OT, OTS):

    filename = p + '.csv'
    if not os.path.exists(filename):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w+'

    with open(filename, 'a+') as f:
        f.writelines(f'\n{namee},{st},{t1},{t2},{twh},{OT},{OTS},{p}')


########################################

def generateDateReport():
    print("date's report being generated")


def generateTodaysReport():
    print("todays report being generated")

print(os.getcwdb())

def show_table():
    #fetch data from firebase
    #generate the csv file 
    
    #####            done     #########
    #open the csv file 
    #seperate header and data
    #print it
    filename = 'D:/Desktop/attendance-gui-test/data.csv'
    if filename == '':
        return
    data = []
    header_list = []
    button = sg.popup_yes_no('Does this file have column names already?')
    if filename is not None:
        with open(filename, "r", newline='',encoding='utf-8') as infile:
            reader = csv.reader(infile)
            if button == 'Yes':
                header_list = next(reader)
            try:
                data = list(reader)  # read everything else into a list of rows
                if button == 'No':   #manual heading creation
                    header_list = ['Name', 'Start Time', 'End Time','Name', 'Start Time', 'End Time','Name', 'Start Time', 'End Time']
            except:
                sg.popup_error('Error reading file')
                return
    sg.set_options(element_padding=(0, 0))

    layout = [[sg.Table(values=data,
                            headings=header_list,
                            col_widths=25,
                            size=(1000,1000),
                            auto_size_columns=True,
                            header_background_color='red',
                            justification='right',
                            
                            # alternating_row_color='lightblue',
                            num_rows=min(len(data), 20))]]


    window = sg.Window('Table', layout, grab_anywhere=False,resizable=False)
    event, values = window.read()
    
    

    window.close()

def GenerateReport(day, salary, date):
    n = 0
    timelst = []
    duplicates = []
    tlist = []
    dlist = []
    Pro_names = []
    Emp_names = []
    absent = []
    FMT = '%H:%M:%S'
    ymd = '%Y-%m-%d'
    isValid = False
    isDate = False
    isToday = False

    missing = []
    UIP = []  # Unique ID in profile_user
    GnName = []
    tlist = [None]
    n = 0
    k = 0

    # value check
    if len(day) > 0:
        isToday = True
        print("is today true")
    if len(salary)> 0:
        isValid = True
        print("is Valid true")
    else:
        sg.Popup("Please fill the salary field")
        return
    if len(date) > 0:
        print("is date true")
        isDate = True

    if isToday == True and isDate == True:
        sg.Popup("Please choose either date or day")
        return

    if(isToday == True and isValid == True):
        sg.PopupAutoClose("Generating todays report")
        generateTodaysReport()
    elif(isDate == True and isValid == True):
        generateDateReport()

    return
    r2 = firebase.get('/user_profiles', '')
    print('Please wait.....', end="\n")

    for z in r2.values():
        GnName.append(z['name'])
    for aa in r2:
        UIP.clear()
        UIP.append(aa)
        for x in UIP:
            r = firebase.get('/Employee Data/' + UIP[n], '')
            mylist = []
        if r is None:
            missing.append(GnName[k])
            st = 'Missing Record'
            namee = GnName[k]
            t1, t2, twh, OT, OTS = 'None', 'None', 'None', 'None', 'None'
            cre(namee, st, t1, t2, twh, OT, OTS)
        else:
            dlist.clear()
            tlist.clear()
            for a in r.values():
                mylist.append(a["dateTime"])
            for dt in mylist:
                dt1 = datetime.strptime(dt, '%Y-%m-%d, %H:%M:%S')
                tlist.append(dt1.strftime(FMT))
                dlist.append(dt1.strftime(ymd))

            print("        Employee Name :", GnName[k])
            print(" ", sep='\n')
            date = list_duplicates(dlist, p)
            if date is not None:
                calculations(date, dlist, tlist, GnName[k], sal)

            else:
                print('absent')
                st = 'Absent'
                namee = GnName[k]
                t1, t2, twh, OT, OTS = 'None', 'None', 'None', 'None', 'None'
                cre(namee, st, t1, t2, twh, OT, OTS)

        # n=n+1
        k = k+1


'''       
p='2020-07-13'

sal=120
GenerateReport()
'''

while True:
    event, values = window.read()
    
    
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        print("program exitting")
        break
    if event == 'Generate':
        day = str(values['day'])
        salary = str(values['salary'])
        date = str(values['date'])
        print('you entered day', day, 'you typed salary',
        salary, 'you type date', date)
        GenerateReport(day, salary, date)

        
    if event == 'Display Report':
        #the excel data display code goes in here
        show_table()
        print("Printing excel data")
    





window.close()
