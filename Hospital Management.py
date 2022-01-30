from tabulate import tabulate

import mysql.connector as sqltor

from datetime import date

mycon=sqltor.connect(host="127.0.0.1",user="root",passwd="sajal",database="hospitalmanagement")        

if mycon.is_connected():
    print("Successful connection with HOSPITAL MANAGEMENT DATABASE established!!!")

else:
    print("Error!!! Connection not established!!!")

cursor=mycon.cursor()

cursor.execute('create table if not exists DOCTOR (DocId int(4) primary key not null,FirstName varchar(30),LastName varchar(30),Address varchar(50),PhNo bigint(12),Qualification varchar(20),Gender varchar(15),Department varchar(25))')
            
cursor.execute('create table if not exists PATIENT (PatientId int(4) primary key not null, DocId int(4),FirstName varchar(30), LastName varchar(30),Age int(3),Gender varchar (15),BloodGroup varchar(10),DiagnosedWith varchar(50),Address varchar(50),DateofAdmission date,PhNo bigint(12),RoomNo int(4),Department varchar(25))')    
cursor.execute('create table if not exists RoomDetails (RoomNo int(4) primary key not null,RoomType varchar(15))')     
cursor.execute('create table if not exists BillDetails(BillNo varchar(12) primary key not null,Date date,PatientId int(4),DateofAdmission date,DateofDischarge date,Roomcharges int(5),PathologyFees int(5),DoctorFees int(5),MiscCharges int(5),TotalAmount int(6))')

cursor.execute('Alter table patient add foreign key (DocId) references doctor(DocId)')

cursor.execute('Alter table patient add foreign key (RoomNo) references roomdetails (RoomNo)')

def AddDoctorDetails():
    L=[]
    DocId=input("Enter the Doctor ID : ")
    L.append(DocId)
    FirstName=input("Enter First Name : ")
    L.append(FirstName)
    LastName=input("Enter Last Name : ")
    L.append(LastName)
    Address=input("Enter Address : ")
    L.append(Address)
    PhNo=input("Enter Phone Number : ")
    L.append(PhNo)
    Qualification=input("Enter Qualification : ")
    L.append(Qualification)
    Gender=input("Enter Gender : ")
    L.append(Gender)
    Department=input("Enter Department : ")
    L.append(Department)
    doctor=(L)
    sql=("Insert into doctor(DocId,Firstname,Lastname,Address,PhNo,Qualification,Gender,Department) Values (%s,%s,%s,%s,%s,%s,%s,%s)")              
    cursor.execute(sql,doctor)
    mycon.commit()
    print("Record successfully entered!!!")



def DocView():
    print("Select the search criteria to view records:") 
    print("1. Doctor Id")
    print("2. First Name")
    print("3. Department")
    print("4. View all records")
    print("5. Exit")
    ch=int(input("Enter the choice : "))
    if ch==1:
        s=int(input("Enter Doctor Id: "))
        rl=(s,)
        sql="select * from doctor where DocId=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered Doctor Id!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print("The details of the doctor with Doctor Id",s,"are as follows:")
            print(tabulate(data,headers=['Doctor Id','First Name','Last Name','Address','Phone Number','Qualification','Gender','Department'],tablefmt='fancy_grid'))
     
    elif ch==2:
        s=input("Enter First Name : ")
        rl=(s,)
        sql="select * from doctor where FirstName=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered First Name!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print("The details of the doctor with First Name",s,"are as follows:")
            print(tabulate(data,headers=['Doctor Id','First Name','Last Name','Address','Phone Number','Qualification','Gender','Department'],tablefmt='fancy_grid'))
            print("The total number of records retrieved is",count)

    elif ch==3:
        s=input("Enter Department : ")
        rl=(s,)
        sql="select * from doctor where department=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No doctors in entered department!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print("The details of the doctors in the department",s,"are as follows:")
            print(tabulate(data,headers=['Doctor Id','First Name','Last Name','Address','Phone Number','Qualification','Gender','Department'],tablefmt='fancy_grid'))
            print("The total number of records retrieved is",count)

    elif ch==4:
        sql="select * from doctor"
        cursor.execute(sql)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("Doctor table has no records to display!!!")
        else:
            print("Details of all doctors are as follows:")
            print(tabulate(data,headers=['Doctor Id','First Name','Last Name','Address','Phone Number','Qualification','Gender','Department'],tablefmt='fancy_grid'))
            print("The total number of records retrieved is",count)
    elif ch==5:
        print("")
        run = input("Do you want to run program again? Yes/No: ")
        print("")
        while(run.lower() == 'y' or run.lower()=='yes'):
              Menu()
              run = input("\nDo you want to run program again? Yes/No: ")

def UpdateDoctor():
    DocId=(input("Enter Doctor Id to update details :"))
    sql="select * from doctor where DocId=%s"
    p=(DocId,)
    cursor.execute(sql,p)
    data=cursor.fetchall()
    print("")
    print("The current details of doctor with Doctor Id",DocId,"are as follows:")
    print("")
    print(tabulate(data,headers=['Doctor Id','First Name','Last Name','Address','Phone Number','Qualification','Gender','Department'],tablefmt='fancy_grid'))
    print("")
    field=input("Enter the field which you want to update : ")
    value=input("Enter the value you want to set : ")
    sql="Update doctor set " + field +"='" + value + "'where DocId='" + DocId + "'"
    cursor.execute(sql)
    print("Record Updated!! ")
    print("The revised details are as follows : ")
    sql="select * from doctor where DocId=%s"
    p=(DocId,)
    cursor.execute(sql,p)
    data=cursor.fetchall()
    print(tabulate(data,headers=['Doctor Id',
                  'First Name','Last Name','Address','Phone Number','Qualification','Gender','Department'],tablefmt='fancy_grid')
                  )
    mycon.commit()

def DelDoctor():
    DocId=(input("Enter the Doctor Id to delete details: "))
    sql="select * from doctor where DocId=%s"
    p=(DocId,)
    cursor.execute(sql,p)
    data=cursor.fetchall()
    count=cursor.rowcount
    if count==0:
        print("No such record exists.Can't delete!!!")
    else:
        print("")
        print("The details of doctor with Doctor Id",DocId,"are as follows:")
        print("")
        print(tabulate(data,headers=['Doctor Id','First Name','Last Name','Address','Phone Number','Qualification','Gender','Department'],tablefmt='fancy_grid'))
        print("")
        delete = input("Are you sure you want to delete the above record? Y/n: ")
        if(delete.lower() == 'y'or delete.lower()=='yes'
           ):
            sql="delete from doctor where DocId=%s"
            p=(DocId,)
            cursor.execute(sql,p)
            mycon.commit()
            print("The required record has been deleted")
        else:
            print("Record not deleted.")

def AddPatientDetails():
    L=[]
    PatientId=input("Enter the patient Id : ")
    L.append(PatientId)
    DocId=input("Enter the Doctor ID : ")
    L.append(DocId)
    FirstName=input("Enter First Name : ")
    L.append(FirstName)
    LastName=input("Enter Last Name : ")
    L.append(LastName)
    Age=input("Enter age : ")
    L.append(Age)
    Gender=input("Enter gender : ")
    L.append(Gender)
    BloodGroup=input("Enter blood group :")
    L.append(BloodGroup)
    DiagnosedWith=input("Enter disease/disorder patient has been diagnosed with :")
    L.append(DiagnosedWith)
    Address=input("Enter address : ")
    L.append(Address)
    DateofAdmission=input("Enter date of admission : ")
    L.append(DateofAdmission)
    PhNo=input("Enter phone number : ")
    L.append(PhNo)
    RoomNo=input("Enter room number : ")
    L.append(RoomNo)
    Department=input("Enter department : ")
    L.append(Department)
    patient=(L)
    sql=("Insert into Patient (PatientId,DocId,FirstName,LastName,Age,Gender,BloodGroup,DiagnosedWith,Address,DateofAdmission,PhNo,RoomNo,Department)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    cursor.execute(sql,patient)
    mycon.commit()
    print("Record successfully entered!!!")

def PatientHistory():
    print("Select the search criteria : ")
    print("1. Patient Id")
    print("2. First Name")
    print("3. View records of all patients")
    print("4.Exit")
    ch=int(input("Enter the choice : "))
    if ch==1:
        s=int(input("Enter Patient Id: "))
        rl=(s,)
        sql="select * from patient where PatientId=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered Patient Id!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print("The details of the patient with Patient Id",s,"are as follows:")
            print(tabulate(data,headers=['Patient Id','Doctor Id','First Name','Last Name','Age','Gender','Blood Group','Diagnosed With','Address','Date of Admission','Phone Number','RoomNumber','Department','Bill Number'],tablefmt='fancy_grid'))

    elif ch==2:
        s=input("Enter First Name : ")
        rl=(s,)
        sql="select * from patient where FirstName=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered First Name!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print("The details of the patients with First Name",s,"are as follows:")
            print(tabulate(data,headers=['Patient Id','Doctor Id','First Name','Last Name','Age','Gender','Blood Group','Diagnosed With','Address','Date of Admission','Phone Number','RoomNumber','Department','Bill Number'],tablefmt='fancy_grid'))
            print("The number of records retrieved is",count)
    elif ch==3:
        sql="select PatientId,DocId,FirstName,LastName,Age,Gender,BloodGroup,DiagnosedWith,Address,DATEOFADMISSION,PhNo,RoomNo,Department from patient"
        cursor.execute(sql)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("Patient table has no records to display!!!")
        else:
            print("Details of all patients are as follows : ")
            print(tabulate(data,headers=['Patient Id','Doctor Id','First Name','Last Name','Age','Gender','Blood Group','Diagnosed With','Address','Date of Admission','Phone Number','RoomNumber','Department'],tablefmt='fancy_grid'))
            print("The total number of records retrieved is",count)
    elif ch==4:
        print("")
        run = input("Do you want to run program again? Yes/No: ")
        print("")
        while(runAgain.lower() == 'y' or runAgain.lower()=='yes'):
              Menu()
              runAgain = input("\nDo you want to run program again? Yes/No: ")

def PatientDoctorDetails():
    print("Select the search criteria : ")
    print("1. Patient Id")
    print("2. First Name")
    print("3. View doctor details of all patients")
    ch=int(input("Enter the choice : "))
    if ch==1:
        s=int(input("Enter Patient Id: "))
        rl=(s,)
        sql="select patient.PatientId,patient.FirstName,patient.LastName,doctor.DocId,doctor.FirstName as DocName,doctor.department from patient,doctor where patient.DocId=doctor.DocId and PatientId=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered Patient Id!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print("The details of the patient's doctor with Patient Id",s,"are as follows:")
            print(tabulate(data,headers=['Patient Id','First Name','Last Name','Doctor Id','Doctor Name','Department'],tablefmt='fancy_grid'))

    elif ch==2:
        s=input("Enter First Name : ")
        rl=(s,)
        sql="select patient.PatientId,patient.FirstName,patient.LastName,doctor.DocId,doctor.FirstName as DocName,doctor.department from patient,doctor where patient.DocId=doctor.DocId and patient.FirstName =%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered First Name!!! ")
        else:
            print("")
            print("Search criteria matched!!!")
            print("The details of the patient's doctor with First Name",s,"are as follows:")
            print(tabulate(data,headers=['Patient Id','First Name','Last Name','Doctor Id','Doctor Name','Department'],tablefmt='fancy_grid'))

        
    elif ch==3:
        sql="select patient.PatientId,patient.FirstName as Patientname,patient.LastName,doctor.DocId,doctor.FirstName as DocName,doctor.department from patient,doctor where patient.DocId=doctor.DocId"
        cursor.execute(sql)
        data=cursor.fetchall()
        count=cursor.rowcount
        print("The total number of records retrieved is",count)
        if count==0:
            print("")
            print("No records exist!!!")
        else:
            print("")
            print("Details about patients with respective doctors are as follows :")
            print(tabulate(data,headers=['Patient Id','First Name','Last Name','Doctor Id','Doctor Name','Department'], tablefmt='fancy_grid'))
            print("The total number of records retrieved is",count)

def PatientRoom():
    print("Select the search criteria : ")
    print("1. Patient Id")
    print("2. First Name")
    print("3. View room details of all patients")
    ch=int(input("Enter the choice : "))
    if ch==1:
        s=int(input("Enter Patient Id: "))
        rl=(s,)
        sql="select patient.PatientId,patient.FirstName,patient.LastName,roomdetails.RoomNo,roomdetails.RoomType from patient,RoomDetails where patient.RoomNo=Roomdetails.RoomNo and PatientId=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered Patient Id!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print("Room details of patient with Patient Id",s,"are as follows:")
            print(tabulate(data,headers=['Patient Id','First Name','Last Name','Room No.','Room Type'],tablefmt='fancy_grid'))
    elif ch==2:
        s=input("Enter First Name : ")
        rl=(s,)
        sql="select patient.PatientId,patient.FirstName,patient.LastName,roomdetails.RoomNo,roomdetails.RoomType from patient,RoomDetails where patient.RoomNo=Roomdetails.RoomNo and FirstName=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered First Name!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print("Room details of patient with First Name",s,"are as follows:")
            print(tabulate(data,headers=['Patient Id','First Name','Last Name','Room No.','Room Type'], tablefmt='fancy_grid'))
    elif ch==3:
        sql="select patient.PatientId,patient.FirstName,patient.LastName,roomdetails.RoomNo,roomdetails.RoomType from patient,RoomDetails where patient.RoomNo=Roomdetails.RoomNo"
        cursor.execute(sql)
        data=cursor.fetchall()
        count=cursor.rowcount
        print("The total number of records retrieved is",count)
        if count==0:
            print("No records exist!!!")
        else:
            print("")
            print("Details about patients with respective room details are as follows:")
            print(tabulate(data,headers=['Patient Id','First Name','Last Name','Room No.','Room Type'],tablefmt='fancy_grid'))
            print("The total number of records retrieved is",count)
def PatientBill():
    print("Select the search criteria : ")
    print("1. Patient Id")
    print("2. First Name")
    print("3. View bill details of all patients")
    ch=int(input("Enter the choice : "))
    if ch==1:
        s=int(input("Enter Patient Id: "))
        rl=(s,)
        sql="select * from BillDetails where Patientid=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered Patient Id!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print("Bill details of patient with Patient Id",s,"are as follows:")
            print(tabulate(data,headers=['Bill No.','Date of Issue','Patient Id','Date of Admission','Date of Discharge','Room Charges','Pathology Fees','Doctor Fees','Misc Charges','Total amount'],tablefmt='fancy_grid'))
    elif ch==2:
        s=input("Enter First Name : ")
        rl=(s,)
        sql="select patient.PatientId,patient.FirstName,patient.LastName,Billdetails.BillNo,Billdetails.Roomcharges,Billdetails.PathologyFees,Billdetails.DoctorFees,Billdetails.MiscCharges,BillDetails.TotalAmount from patient,BillDetails where patient.BillNo=Billdetails.BillNo and FirstName=%s"
        cursor.execute(sql,rl)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No record found with entered First Name!!!")
        else:
            print("")
            print("Search criteria matched!!!")
            print(tabulate(data,headers=['Patient Id','First Name','Last Name','Bill No.','Room Charges','Pathology Fees','Doctor Fees','Misc Charges','Total amount'],tablefmt='fancy_grid'))
    elif ch==3:
        sql="select * from BillDetails"
        cursor.execute(sql)
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print("")
            print("No records exist!!!")
        else:
            print("")
            print("Details about patients with respective bill details are as follows : ")
            print(tabulate(data,headers=['Bill No.','Date of Issue','Patient Id','Date of Admission','Date of Discharge','Room Charges','Pathology Fees','Doctor Fees','Misc Charges','Total amount'],tablefmt='fancy_grid'))
            print("The total number of records retrieved is",count)
def PatientView():
    print("1.View patient history")
    print("2.View patient's doctor's details")
    print("3.View patients room details")
    print("4.View patient's bill details")
    ch=int(input("Enter your choice: "))
    if ch==1:
        PatientHistory()
    elif ch==2:
        PatientDoctorDetails()
    elif ch==3:
        PatientRoom()
    elif ch==4:
        PatientBill()
    else:
        print("Enter correct choice. . . ")

def UpdatePatient():
    PatientId=(input("Enter Patient Id to update details: "))
    sql="select * from patient where PatientId=%s"
    p=(PatientId,)
    cursor.execute(sql,p)
    data=cursor.fetchall()
    print("")
    print(tabulate(data,headers=['Patient Id','Doctor Id','First Name','Last Name','Age','Gender','Blood Group','Diagnosed with','Address','Date of Admission','Phone Number','Room Number','Department','Bill Number'],tablefmt='fancy_grid'))
    print("")
    field=input("Enter the field which you want to update : ")
    value=input("Enter the value you want to set : ")
    sql="Update patient set " + field +"='" + value + "'where PatientId='" + PatientId + "'"
    cursor.execute(sql)
    print("Record Updated!! ")
    print("The revised details are as follows : ")
    sql="select * from patient where PatientId=%s"
    p=(PatientId,)
    cursor.execute(sql,p)
    data=cursor.fetchall()
    print(tabulate(data,headers=['Patient Id','Doctor Id','First Name','Last Name','Age','Gender','Blood Group','Diagnosed with','Address','Date of Admission','Phone Number','Room Number','Department','Bill Number'],tablefmt='fancy_grid'))    

def DelPatient():
    PatientId=(input("Enter the Patient Id to delete details : "))
    sql="select * from patient where PatientId=%s"
    p=(PatientId,)
    cursor.execute(sql,p)
    data=cursor.fetchall()
    count=cursor.rowcount
    if count==0:
        print("No such record exists.Can't delete!!!")
    else:
        print("")
        print("The details of patient with Patient Id",PatientId,"are as follows:")
        print("")
    print(tabulate(data,headers=['Patient Id','Doctor Id','First Name','Last Name','Age','Gender','Blood Group','Diagnosed with','Address','Date of Admission','Phone Number','Room Number','Department','Bill Number'],tablefmt='fancy_grid'))
    print("")
    delete = input("Are you sure you want to delete the above record? Y/n: ")
    if(delete.lower() == 'y'or delete.lower()=='yes'):
        sql="delete from PATIENT where PatientId=%s"
        p=(PatientId,)
        cursor.execute(sql,p)
        mycon.commit()
        print("The required record has been deleted")
    else:
        print("Record not deleted.")

def AddBillDetails():
    L=[]
    BillNo=input("Enter the Bill Number : ")
    L.append(BillNo)
    Date=date.today()
    L.append(Date)
    PatientId=(input("Enter the patient Id : "))
    L.append(PatientId)
    DateofAdmission=input("Enter date of admission : ")
    L.append(DateofAdmission)
    DateofDischarge=input("Enter date of discharge : ")
    L.append(DateofDischarge)
    RoomCharges=int(input("Enter room charges :"))
    L.append(RoomCharges)
    PathologyFees=int(input("Enter pathology fees :"))
    L.append(PathologyFees)
    DoctorFees=int(input("Enter doctor fees :"))
    L.append(DoctorFees)
    MiscCharges=int(input("Enter miscellaneous charges:"))
    L.append(MiscCharges)
    TotalAmount=RoomCharges+PathologyFees+DoctorFees+MiscCharges
    L.append(TotalAmount)
    bill=(L)
    sql=("Insert into BillDetails(BillNo,Date,PatientId,DateofAdmission,DateofDischarge,Roomcharges,PathologyFees,DoctorFees,MiscCharges,TotalAmount)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    cursor.execute(sql,bill)
    value=BillNo;
    field="BillNo";
    sql="Update patient set " + field +"='" + value + "'where PatientId='" + PatientId + "'"
    cursor.execute(sql)
    mycon.commit()
    print("Record successfully entered!!!")
    
def Menu():
    print("Using this system you can:")
    data=[
    (1,"Add doctor details"),
    (2,"View doctor details"),
    (3,"Update doctor details"),
    (4,"Delete doctor details"),
    (5,"Add patient details"),
    (6,"View patient details"),
    (7,"Update patient details"),
    (8,"Delete patient details"),
    (9,"Generate new bill")
    ]
    print(tabulate(data,headers=['Choice No.','Function'],tablefmt='fancy_grid'))
    print("")
    ch=int(input("Enter your choice: "))
    if ch==1:
        AddDoctorDetails()
    elif ch==2:
        DocView()
    elif ch==3:
        UpdateDoctor()
    elif ch==4:
        DelDoctor()
    elif ch==5:
        AddPatientDetails()
    elif ch==6:
        PatientView()
    elif ch==7:
        UpdatePatient()
    elif ch==8:
        DelPatient()
    elif ch==9:
        AddBillDetails()
    else:
        print("Enter correct choice. . . ")
print("*"*80)
print("                 HOSPITAL MANAGEMENT SYSTEM            ")
print("* * * * Computer Project Developed by: SAJAL AGGARWAL * * * * ")
print("*"*80)
print("")
Menu()
def runAgain():
    print("")
    runAgain = input("Do you want to run program again? Yes/No: ")
    print("")
    while(runAgain.lower() == 'y' or runAgain.lower()=='yes'):
        Menu()
        runAgain = input("\nDo you want to run program again? Yes/No: ")
runAgain()
        
                                                                        


