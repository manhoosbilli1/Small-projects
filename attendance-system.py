import os
import csv
from firebase import firebase
from datetime import datetime
import PySimpleGUI as sg
######################################




######################################
day = ""
date = ""
salary = 0
SrNo = 0
generation_started = False
pathValid = False
generate = False

# Retrive data form Firebase
firebase = firebase.FirebaseApplication(
    "https://citapp-65efb.firebaseio.com", None)
######################################## 

##########################################

sg.theme('DarkAmber')
sg.set_options(element_size=200)
layout = [[sg.Text("Please type date")],
          [sg.InputText(key='date',
          enable_events=True,
          justification='center',
          size=(30,1)), 
          sg.CalendarButton('Pick a date',close_when_date_chosen=True, 
                                            target='date',
                                            location=(0,0),
                                            no_titlebar=False,
                                            format='%Y-%m-%d',)],
          [sg.Text("Please type salary")], 
          [sg.InputText(key='salary',
          enable_events=True,
          justification='center',
          size=(30,1))],



          [sg.Button(button_text='Generate'),
           sg.Button('Display Report'),sg.Cancel(pad=(60,0))]]
 

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
        total_sal = overtime*float(salary)
        #print("                OverTime = ",ovt)
        #print("        Extratime salary = ",total_sal)
    else:
        ovt = "No OverTime"
        total_sal = "N/A"
    return ovt, total_sal


##########################################

def calculations(readPath,date, mylist, tlist, namee, sal,k):

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
    cre(readPath,k,namee, st, t1, t2, twh, OT, OTS)


##########################################
def cre(readPath,k,namee, st, t1, t2, twh, OT, OTS):
    

    filename = readPath

    with open(filename, 'a+') as f:
        writer= csv.writer(f)
        writer.writerow([
            k,namee,st,date,t1,t2,twh,OT,OTS])
        #f.writelines(f'\n{k},{namee},{st},{t1},{t2},{twh},{OT},{OTS}')


########################################


#file create function for generate button pending...
def Creat1():
    Sr= 'Sr.No'     
    name = 'Employee Name'
    Status = 'Attendance Status'
    Da = 'Date'
    Ti = 'Time In'
    to = 'Time Out'
    wh = 'Working Hours'
    Ot= 'Over Time'
    ots = 'OverTime Salary'
    filename = date+'.csv'
    #if not os.path.exists(filename):
    with open(filename,'w+') as f:
        writer= csv.writer(f)
        writer.writerow([
            Sr,name,Status,Da,Ti,to,wh,Ot,ots])

        
        
#########################################

def generateDateReport(readPath):
    missing = []
    UIP = []  # Unique ID in profile_user
    GnName = []
    tlist = [None]
    k=0
    timelst=[]
    duplicates=[]
    tlist = []
    dlist=[]
    Pro_names=[]
    Emp_names=[]
    absent=[]
    FMT = '%H:%M:%S'
    ymd = '%Y-%m-%d'

    n = 0
    Sr= 1
    print("date's report being generated")
    r2 = firebase.get('/user_profiles', '')
    print('Please wait.....', end="\n")
    if(len(r2) > 0):
        generation_started = True

    if(generation_started == True):
        layout = [[sg.Text('File fetching in progress')],
                  [sg.ProgressBar(max_value = len(r2),orientation='h',size=(20,20), key='progress')],
                    ]
        progressWindow = sg.Window('Progress meter', layout, finalize=True)
        progress_bar = progressWindow['progress']

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
            cre(readPath,Sr,namee, st, t1, t2, twh, OT, OTS)
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
            datee = list_duplicates(dlist, date)
            if datee is not None:
                calculations(readPath,datee, dlist, tlist, GnName[k], salary,Sr)

            else:
                print('absent')
                st = 'Absent'
                namee = GnName[k]
                t1, t2, twh, OT, OTS = 'None', 'None', 'None', 'None', 'None'
                cre(readPath,Sr,namee, st, t1, t2, twh, OT, OTS)

        #n=n+1
        k = k+1
        Sr= Sr+1
        progress_bar.update_bar(k)
    print('.........Report Generated.......')
    generation_started = False
    progressWindow.close()
    sg.popup_ok('Files succesfully fetched')
    return
        


def show_table(date):

    global pathValid
    global generate
    #convert date string to date
    dataDirectory = 'D:/Downloads/test/'
    readPath = dataDirectory + '/' + date + '.csv'
    print('Path is:  ' + readPath)
    if os.path.isfile(readPath) == False:
        sg.popup_error("File does not exist. generate first.")
        pathValid = False

    if os.path.isfile(readPath) == True:
        print("Path Already exists, now opening")
        pathValid = True

    if(pathValid == True):
        filename = readPath
        if filename == '':
            return
        data = []
        header_list = []
        if filename is not None:
            with open(filename, "r") as infile:
                try:
                    reader = csv.reader(infile)
                    if(generate == True):
                        header_list = ['Sr. No', 'Employee Name', 'Attendance Status', 'Date','Time In', 'Time Out', 'Working Hours','Over Time', 'OverTime Salary']
                        
                    else:
                        header_list = next(reader)


                    data = list(reader)  # read everything else into a list of rowsheader_list = ['Sr. No', 'Employee Name', 'Attendance Status', 'Date','Time In', 'Time Out', 'Working Hours','Over Time', 'OverTime Salary']
                except:
                    sg.popup_error("Error reading file, Path doesn't exist")
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
    else:
        print("Path wasn't valid")
        return

def GenerateReport(salary, date,readPath):

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



    # value check
    if len(salary)> 0:
        isValid = True
        print("is Valid true")
    if len(date) > 0:
        print("is date true")
        isDate = True
    if(isDate == True and isValid == True):
        generateDateReport(readPath)

    
    
def GenerateReportExplicit(salary, date):

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
    #Creat1()



        


    # value check
    if len(salary)> 0:
        isValid = True
        print("is Valid true")
    if len(date) > 0:
        print("is date true")
        isDate = True
    path = date + '.csv'
    if(isDate == True and isValid == True):
        dataDirectory = 'D:/Downloads/test/'
        readPath = os.path.join(dataDirectory + date + '.csv')
        createPath = os.path.join(date, '.csv')
        print('Path is:  ' + readPath)
        if os.path.isfile(readPath) == False:
            try:
                with open(createPath,'w+', '', 'utf-8') as f:
                    writer= csv.writer(f)

                #header supplied manually
            except:
                print("Couldn't create file")

            try:
                print("Fetching data")
                GenerateReport(salary, date,readPath)
                pathValid = True
            except:
                print("File generation Failed, check path")
                sg.popup_ok("Error Opening file, Path doesn't exist")
                return

        else:
            print("Path exists, now opening")
            pathValid = True
            print("Path exists now generating data")
            generateDateReport(path)
            return

while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        print("program exitting")
        break
    if event == 'Generate':
        salary = str(values['salary'])
        date = str(values['date'])
        if date == '' or salary == '':
            sg.popup_ok('Please fill the fields correctly')
        else:
            generate = False
            GenerateReportExplicit(salary, date)
        

        
    if event == 'Display Report':
        #the excel data display code goes in here
        salary = str(values['salary'])
        date = str(values['date'])
        if date == '':
            sg.popup_ok("Please fill date and salary")
        else:
            generate = True   #we 
            show_table(date)
    



window.close()


#todo 

# 1- make a single button to display as well as generate the data based on the data providied
# 2- create a popup after every generation asking wether the user wants to display the results or not. will be autoclose
# 3- shrinkify the code by creating seperate functions and calling them from root instead of function inside of a function 
# 4- make the file creation and reading more robust. 
# 5- make the reading from firebase quick 
# 6- make an option so that the user can choose any csv from his computer instead of firebase if he wishes
# 7- abillity to open multiple windows for every file using  OOP
