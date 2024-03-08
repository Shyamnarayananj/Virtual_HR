from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera2 import VideoCamera2
import os
import time
import datetime
from random import randint
import cv2
import PIL.Image
from PIL import Image
import imagehash
from flask import send_file
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import docx2txt
import shutil
import subprocess
import gensim
#word to pdf
import aspose.words as aw

import pyttsx3
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="virtual_hr"
)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    act=""
    msg=""

    #now1 = datetime.datetime.now()
    #rtime=now1.strftime("%H:%M")
    #print(rtime)

    return render_template('web/index.html',msg=msg,act=act)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM vh_candidate WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            ff=open("uname.txt","w")
            ff.write(uname)
            ff.close()
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login_company', methods=['GET', 'POST'])
def login_company():
    msg=""
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM vh_job_provider_register WHERE hr_id = %s AND password = %s AND approved_status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('add_vacancy'))
        else:
            msg = 'Incorrect username/password! or Not Approved'
    return render_template('login_company.html',msg=msg)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    msg=""
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM vh_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_admin.html',msg=msg)



@app.route('/register',methods=['POST','GET'])
def register():
    msg=""
    act=""
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        
        uname=request.form['uname']
        pass1=request.form['pass']
      
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM vh_candidate where username=%s",(uname, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM vh_candidate")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO vh_candidate(id,name,mobile, email, username,password,register_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,mobile,email,uname,pass1,rdate)
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "record inserted.")
            msg='success'
            
            #if mycursor.rowcount==1:
            #    result="Registered Success"
            
        else:
            msg="fail"
    return render_template('register.html',msg=msg)

@app.route('/reg_company',methods=['POST','GET'])
def reg_company():
    msg=""
    act=""
    if request.method=='POST':
        company=request.form['company']
        name=request.form['name']
        services=request.form['services']
        
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']
        uname=request.form['uname']
        pass1=request.form['pass']
      
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM vh_job_provider_register where hr_id=%s",(uname, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM vh_job_provider_register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO vh_job_provider_register(id,hr_name,company_name,services,location,mobile, email, hr_id,password,approved_status,register_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
            val = (maxid,name,company,services,location,mobile,email,uname,pass1,'0',rdate)
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "record inserted.")
            msg='success'
            
            #if mycursor.rowcount==1:
            #    result="Registered Success"
            
        else:
            msg="fail"
    return render_template('reg_company.html',msg=msg)

@app.route('/admin',methods=['POST','GET'])
def admin():
    msg=""
    email=""
    mess=""
    act=request.args.get("act")
    uname=""
    data=[]
   
    s1=""
    s2=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_job_provider_register")
    data = mycursor.fetchall()

    if act=="yes":
        cid=request.args.get("cid")
        mycursor.execute("SELECT * FROM vh_job_provider_register where id=%s",(cid,))
        ds = mycursor.fetchone()
        email=ds[6]
        name=ds[1]
        company=ds[2]
        mess="Dear "+name+", Company:"+company+" has Approved for accessing Virtual HR Web App"
        
        mycursor.execute("update vh_job_provider_register set approved_status=1 where id=%s",(cid,))
        mydb.commit()
        msg="ok"

    return render_template('admin.html',msg=msg,act=act,data=data,email=email,mess=mess)

@app.route('/candidate_vacancy',methods=['POST','GET'])
def candidate_vacancy():
    msg=""
    email=""
    mess=""
    act=request.args.get("act")
    uname=""
    data=[]
   
    s1=""
    s2=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM vh_vacancy order by id desc")
    data1 = mycursor.fetchall()



    return render_template('candidate_vacancy.html',msg=msg,act=act,data=data,data1=data1)

@app.route('/admin_vacancy',methods=['POST','GET'])
def admin_vacancy():
    msg=""
    email=""
    mess=""
    act=request.args.get("act")
    uname=""
    data=[]
   
    s1=""
    s2=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_vacancy order by id desc")
    data = mycursor.fetchall()



    return render_template('admin_vacancy.html',msg=msg,act=act,data=data)

@app.route('/add_resume',methods=['POST','GET'])
def add_resume():
    msg=""
    act=request.args.get("act")
    uname=""
    data1=[]
    data2=[]
    s1=""
    s2=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()


    mycursor.execute("SELECT count(*) FROM vh_qualification where username=%s",(uname, ))
    c1 = mycursor.fetchone()[0]
    if c1>0:
        s1="1"
        mycursor.execute("SELECT * FROM vh_qualification where username=%s",(uname, ))
        data1 = mycursor.fetchall()

    mycursor.execute("SELECT count(*) FROM vh_experience where username=%s",(uname, ))
    c2 = mycursor.fetchone()[0]
    if c2>0:
        s2="1"
        mycursor.execute("SELECT * FROM vh_experience where username=%s",(uname, ))
        data2 = mycursor.fetchall()

    
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        city=request.form['city']
        postal_code=request.form['postal_code']
        father_name=request.form['father_name']
        father_occupation=request.form['father_occupation']
        father_jobtype=request.form['father_jobtype']
        father_job_location=request.form['father_job_location']
        father_annual_income=request.form['father_annual_income']
        mother_name=request.form['mother_name']
        mother_occupation=request.form['mother_occupation']
        mother_jobtype=request.form['mother_jobtype']
        mother_job_location=request.form['mother_job_location']
        mother_annual_income=request.form['mother_annual_income']
        
        
        mycursor.execute("update vh_candidate set name=%s,gender=%s,dob=%s,mobile=%s,email=%s,address=%s,city=%s,postal_code=%s where username=%s", (name,gender,dob,mobile,email,address,city,postal_code,uname))
        mydb.commit()
        mycursor.execute("update vh_candidate set father_name=%s,father_occupation=%s,father_jobtype=%s,father_job_location=%s,father_annual_income=%s where username=%s", (father_name,father_occupation,father_jobtype,father_job_location,father_annual_income,uname))
        mydb.commit()
        mycursor.execute("update vh_candidate set mother_name=%s,mother_occupation=%s,mother_jobtype=%s,mother_job_location=%s,mother_annual_income=%s where username=%s", (mother_name,mother_occupation,mother_jobtype,mother_job_location,mother_annual_income,uname))
        mydb.commit()

        msg="success"

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vh_qualification where id=%s",(did,))
        mydb.commit()
        msg="ok"
    if act=="del2":
        did=request.args.get("did")
        mycursor.execute("delete from vh_experience where id=%s",(did,))
        mydb.commit()
        msg="ok2"

        
    return render_template('add_resume.html',data=data,msg=msg,data1=data1,data2=data2,s1=s1,s2=s2)

@app.route('/userhome',methods=['POST','GET'])
def userhome():
    msg=""
    uname=""
    st=""
    data1=[]
    act=request.args.get("act")
    pid=request.args.get("pid")
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()

    ff=open("emotion.txt","w")
    ff.write("")
    ff.close()

    ff=open("img.txt","w")
    ff.write("")
    ff.close()

    ff=open("scount.txt","w")
    ff.write("0")
    ff.close()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    now1 = datetime.datetime.now()
    rtime=now1.strftime("%H:%M")
    #print(rtime)
    
    rtime1=rtime.split(':')
    rh=int(rtime1[0])
    rm=int(rtime1[1])

    mycursor.execute("SELECT count(*) FROM vh_profile_matched where username=%s && interview_status=1",(uname, ))
    cn = mycursor.fetchone()[0]
    if cn>0:
        
        mycursor.execute("SELECT * FROM vh_profile_matched where username=%s && interview_status=1",(uname, ))
        data2 = mycursor.fetchone()
        '''iv_date=data2[4]
        iv_time=data2[5]

        if rdate==iv_date:
            ivt=iv_time.split(":")
            ih=int(ivt[0])
            if ih<=rh:'''
        st="1"
        mycursor.execute("SELECT * FROM vh_profile_matched where username=%s && interview_status=1",(uname, ))
        data1 = mycursor.fetchall()
        
    if act=="no":
        mycursor.execute("update vh_profile_matched set interview_status=2 where id=%s",(pid,))
        mydb.commit()

    return render_template('userhome.html',data=data,act=act,pid=pid,data1=data1,msg=msg,st=st)

@app.route('/add_school',methods=['POST','GET'])
def add_school():
    uname=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()
    

    if request.method=='POST':
        sslc_school=request.form['sslc_school']
        sslc_mark=request.form['sslc_mark']
        hsc_school=request.form['hsc_school']
        hsc_mark=request.form['hsc_mark']
        
        mycursor.execute("update vh_candidate set sslc_school=%s,sslc_mark=%s,hsc_school=%s,hsc_mark=%s where username=%s", (sslc_school,sslc_mark,hsc_school,hsc_mark,uname))
        mydb.commit()

        msg="success2"
    
    return render_template('add_resume.html',data=data)

@app.route('/add_qualification',methods=['POST','GET'])
def add_qualification():
    uname=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        level=request.form['level']
        qualification=request.form['qualification']
        passout_year=request.form['passout_year']
        percentage=request.form['percentage']
        college=request.form['college']
        arrears=request.form['arrears']
        cleared=request.form['cleared']
        
        mycursor.execute("SELECT max(id)+1 FROM vh_qualification")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO vh_qualification(id,username,level,qualification,passout_year,percentage,college,arrears,cleared) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, uname,level,qualification,passout_year,percentage,college,arrears,cleared)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit() 

        msg="success3"
    
    return render_template('add_resume.html',data=data)

@app.route('/add_experience',methods=['POST','GET'])
def add_experience():
    uname=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        designation=request.form['designation']
        experience=request.form['experience']
        year=request.form['year']
        month=request.form['month']
        company_name=request.form['company_name']
        location=request.form['location']
        
        
        mycursor.execute("SELECT max(id)+1 FROM vh_experience")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO vh_experience(id,username,designation,experience,year,month,company_name,location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, uname,designation, experience,year,month,company_name,location)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit() 

        msg="success"
    
    return render_template('add_resume.html',data=data)

@app.route('/upload_resume',methods=['POST','GET'])
def upload_resume():
    msg=""
    uname=""
    filename=""
    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()
    rid=data[0]

    if request.method=='POST':
        file = request.files['file']
        file_type = file.content_type
        
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file:
            fname = "R"+str(rid)+file.filename
            filename = secure_filename(fname)
            file.save(os.path.join("static/upload", filename))

            #docx to pdf
            resume_doc=filename
            rd=resume_doc.split(".")
            resume_pdf=rd[0]+".pdf"
            # Load word document
            doc = aw.Document("static/upload/"+resume_doc)

            # Save as PDF
            doc.save("static/upload/"+resume_pdf)
        
        
        mycursor.execute("update vh_candidate set resume=%s where username=%s", (filename,uname))
        mydb.commit()
        msg="success5"
    
    return render_template('add_resume.html',data=data,msg=msg)

@app.route('/upload_photo',methods=['POST','GET'])
def upload_photo():
    uname=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()
    rid=data[0]

    if request.method=='POST':
        file = request.files['file2']
        fn1="P"+str(rid)+file.filename
        
        print(fn1)
        mycursor.execute("update vh_candidate set photo=%s where username=%s", (fn1,uname))
        mydb.commit()

        file.save(os.path.join("static/upload", fn1))
        
        msg="success6"
    
    return render_template('add_resume.html',data=data)

@app.route('/add_vacancy',methods=['POST','GET'])
def add_vacancy():
    msg=""
    uname=""
    act=request.args.get("act");
    vid=request.args.get("vid")
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()

    #ff=open("static/upload/R1resume_001.docx","r")
    #fdata=ff.read()
    #ff.close()
    #print(fdata.decode(''))

    mycursor.execute("SELECT * FROM vh_job_provider_register where hr_id=%s",(uname,))
    data1 = mycursor.fetchone()
    company=data1[2]

    if request.method=='POST':
        job_title=request.form['job_title']
        gender=request.form['gender']
        mark_10th=request.form['mark_10th']
        mark_12th=request.form['mark_12th']
        level=request.form['level']
        qualification=request.form['qualification']
        mark_degree=request.form['mark_degree']
        arrears=request.form['arrears']
        
        sports=request.form['sports']
        extra_curricular=request.form['extra_curricular']
        skills=request.form['skills']

        inw_start_date=request.form['inw_start_date']
        inw_end_date=request.form['inw_end_date']
        start_time=request.form['start_time']
        total_hours=request.form['total_hours']
        num_apti=request.form['num_apti']
        program=request.form['program']
        #num_program=request.form['num_program']

        sd=inw_start_date.split('-')
        sdate=sd[2]+"-"+sd[1]+"-"+sd[0]

        ed=inw_end_date.split('-')
        edate=ed[2]+"-"+ed[1]+"-"+ed[0]
        
        mycursor.execute("SELECT max(id)+1 FROM vh_vacancy")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        vid=str(maxid)
        sql = "INSERT INTO vh_vacancy(id,job_title,gender,mark_10th,mark_12th,level,qualification,mark_degree,arrears,sports,extra_curricular,skills,inw_start_date,inw_end_date,start_time,total_hours,num_apti,program,hr_id,company) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,job_title,gender,mark_10th,mark_12th,level,qualification,mark_degree,arrears,sports,extra_curricular,skills,sdate,edate,start_time,total_hours,num_apti,program,uname,company)
        
        mycursor.execute(sql, val)
        mydb.commit() 

        msg="success"

    
    mycursor.execute("SELECT * FROM vh_vacancy where hr_id=%s order by id desc",(uname,))
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vh_vacancy where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_vacancy'))
    
    return render_template('add_vacancy.html',msg=msg,act=act,data=data,vid=vid,data1=data1)

@app.route('/add_join',methods=['POST','GET'])
def add_join():
    msg=""
    uname=""
    mess=""
    email=""
    pid=request.args.get("pid")
    
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()



    mycursor.execute("SELECT * FROM vh_job_provider_register where hr_id=%s",(uname,))
    data1 = mycursor.fetchone()
    company=data1[2]

    mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
    data2 = mycursor.fetchone()
    vid=data2[1]
    candidate=data2[2]

    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(candidate,))
    data3 = mycursor.fetchone()
    email=data3[5]
    name=data3[1]

    if request.method=='POST':
        job_position=request.form['job_position']
        training=request.form['training']
        train_days=request.form['train_days']
        join_date=request.form['join_date']
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        salary=request.form['salary']

        jd=join_date.split('-')
        join_date1=jd[2]+"-"+jd[1]+"-"+jd[0]

        
        mycursor.execute("SELECT max(id)+1 FROM vh_joined")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        vid=str(maxid)
        sql = "INSERT INTO vh_joined(id,vid,pid,hr_id,candidate,job_position,training,train_days,join_date,start_time,end_time,salary) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,vid,pid,uname,candidate,job_position,training,train_days,join_date1,start_time,end_time,salary)
        mycursor.execute(sql, val)
        mydb.commit()
        mess="Dear "+name+", You are selected in "+company+", Joining on "+join_date1

        msg="ok"


    return render_template('add_join.html',msg=msg,email=email,mess=mess)



#content filtering
def content_filter():
    find_word = ''
    inpath = inpath + str('*.pdf') 

    list_compare = []

    words = int(input('How many words you want to find: '))

    path = glob.glob(inpath)

    for num in range(words):

        string = input('Please enter the words you want to find: ')
        find_word += "\\b" + string + "\\b" + '|'
        
    find_word = find_word[:-1]


    for file in path:
        PDF_file = Path(fr"{file}")
        print(PDF_file)
        ocr.main(list_compare,find_word,PDF_file)
        all_files.append(file)


    print(list_compare)

    tup1 = zip(list_compare,all_files)

    tup2 = sorted(tup1, key=lambda x: (-x[0], x[1]))

    newpath = r"cv-man\new\\"

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    increment = 0

    for i,j in tup2:
        name = os.path.split(j)
        basename = name[1]
        fn = "{}"
        increment += 1
        fn = fn.format(increment)
        target = str(newpath) + str(f"{fn}") + str("_") + str(basename)
        shutil.copyfile(j, target)



@app.route('/check_resume',methods=['POST','GET'])
def check_resume():
    msg=""
    uname=""
    mess=""
    email=""
    st=""
    vid=request.args.get("vid")
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM vh_candidate")
    d1 = mycursor.fetchall()

    mycursor.execute("SELECT * FROM vh_vacancy where id=%s",(vid,))
    rs1 = mycursor.fetchone()
    dd2=[]

    now1 = datetime.datetime.now()
    rtime=now1.strftime("%H:%M")
    rtime1=rtime.split(':')
    rmin=int(rtime1[1])

    ##
    sk=rs1[11]
    sk1=sk.split(",")

    ##number of profile matched
    vn=0
    ##
    
    f=0
    k=0
    for rs in d1:
        dd1=[]

        s1=""
        s2=""
        s3=""
        s4=""
        s5=""
        s6=""
        ##########
        if rs[25]=="":
            s=1
        else:
            text = docx2txt.process("static/upload/"+rs[25], "/tmp/img_dir") 
            g=0
            for sk2 in sk1:
                
                if sk2 in text:
                    #print(sk2)
                    g+=1
            print("ggg")
            print(g)
        ##########
            
        ##gender
        if rs1[2]=="Any":
            s1="1"
        elif rs1[2]==rs[2]:
            s1="1"
        else:
            s1="2"
        ##mark1
        if rs1[3]<=rs[12]:
            s2="1"
        else:
            s2="2"
        ##mark2
        if rs[14]>0:
            if rs1[4]<=rs[14]:
                s3="1"
            else:
                s3="2"
        else:
            s3="1"
        ##level
        qx=0
        qx2=0
        qx3=0
        d2=0
        mycursor.execute("SELECT count(*) FROM vh_qualification where username=%s",(rs[6],))
        d2 = mycursor.fetchone()[0]
        if d2>0:
            
            mycursor.execute("SELECT count(*) FROM vh_qualification where username=%s && (level=%s || qualification=%s)",(rs[6],rs1[5],rs1[6]))
            qx = mycursor.fetchone()[0]

            mycursor.execute("SELECT sum(percentage) FROM vh_qualification where username=%s",(rs[6],))
            qx2 = mycursor.fetchone()[0]

            mycursor.execute("SELECT sum(arrears) FROM vh_qualification where username=%s",(rs[6],))
            qx3 = mycursor.fetchone()[0]

        qx22=qx2/d2
        qx33=qx3/d2

        
        if rs1[5]=="Any":
            s4="1"
        elif qx>0:
            s4="1"
        else:
            s4="2"
        ##mark
        if qx22>=rs1[7]:
            s5="1"
        else:
            s5="2"

        #arrear
        if qx33<=rs1[8]:
            s6="1"
        else:
            s6="2"
        

        # and s6=="1" and s7=="1"
        if s1=="1" and s2=="1" and s3=="1" and s4=="1" and s5=="1" and s6=="1" and g>0:
            #print(rs[8]+" "+rs1[1])
            #dd1.append(rs[8])
            #dd1.append(rs[1])
            #dd1.append(rs1[1])
            #data4.append(dd1)
            #print(rs1[1])
            
            #dd1.append(rs1[6])
            #dd1.append(rs1[1])
            #dd1.append(rs1[5])
            #data3.append(dd1)
            

            mycursor.execute("SELECT count(*) FROM vh_profile_matched where vacancy_id=%s && username=%s",(rs1[0],rs[6]))
            ucnt = mycursor.fetchone()[0]
            if ucnt==0:

                print(rs[6])
                print(s1)
                print(s2)
                print(s3)
                print(s4)
                print(s5)
                print(s6)

                mycursor.execute("SELECT count(*) FROM vh_candidate where username=%s && status=0",(rs[6],))
                cn = mycursor.fetchone()[0]
                if cn>0:
                    vn+=1
                    mycursor.execute("SELECT max(id)+1 FROM vh_profile_matched")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1

                    '''sdate=rs1[14]
                    stime=rs1[16]

                    hh=int(stime)
                    

                    rrr=[10,20,30]
                    rn=randint(1,3)
                    rn1=rn-1

                    itime=""
                    mm2=0
                    hh2=0
                    mm=rmin+rrr[rn1]
                    if mm>60:
                        hh2=hh+1
                        mm2=mm-60
                        itime=str(hh2)+":"+str(mm2)
                    else:
                        itime=str(hh)+":"+str(mm)'''

                    
                    sql = "INSERT INTO vh_profile_matched(id,vacancy_id,username,interview_date,interview_time,minutes) VALUES (%s, %s, %s,%s,%s,%s)"
                    val = (maxid,rs1[0],rs[6],'','','0')
                    
                    mycursor.execute(sql, val)
                    mydb.commit()

    
    mycursor.execute("SELECT * FROM vh_admin where username='admin'")
    d11 = mycursor.fetchone()
    email=d11[2]

    if vn>0:
        mess="Vacancy ID: "+vid+", "+str(vn)+" profiles matched"
    else:
        mess="Vacancy ID: "+vid+", No profiles matched"

    return render_template('check_resume.html',vid=vid,mess=mess,email=email)

@app.route('/resume_match',methods=['POST','GET'])
def resume_match():
    msg=""
    uname=""
    edata=[]
    s1=""
    vid=request.args.get("vid")
    if 'username' in session:
        uname = session['username']

    now1 = datetime.datetime.now()
    rtime=now1.strftime("%H:%M")
    rtime1=rtime.split(':')
    rmin=int(rtime1[1])

    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM vh_vacancy where id=%s && hr_id=%s",(vid,uname))
    rs1 = mycursor.fetchone()
    n=rs1[18]

    
    mycursor.execute("SELECT * FROM vh_profile_matched p,vh_candidate c where p.username=c.username && p.interview_status=0 && p.vacancy_id=%s",(vid,))
    mdata = mycursor.fetchall()

    if request.method=='POST':
        uu=request.form.getlist('c1[]')
        s1="1"
        for u1 in uu:
            dt=[]

            #######
            sdate=rs1[14]
            stime=rs1[16]
            mins=30

            hh=int(stime)
            

            rrr=[5,10,15]
            rn=randint(1,3)
            rn1=rn-1

            itime=""
            mm2=0
            hh2=0
            mm=rmin+rrr[rn1]
            if mm>60:
                hh2=hh+1
                mm2=mm-60
                itime=str(hh2)+":"+str(mm2)
            else:
                itime=str(hh)+":"+str(mm)
            ########
            
            mycursor.execute("update vh_profile_matched set interview_status=1,interview_date=%s,interview_time=%s,minutes=%s where vacancy_id=%s && username=%s",(sdate,itime,mins,vid,u1))
            mydb.commit()

            #apti question
            mycursor.execute("SELECT * FROM vh_apti_question order by rand()")
            qlist = mycursor.fetchall()
            i=0
            qd=[]
            for qlist1 in qlist:
                if i<n:
                    #print(qlist1[0])
                    qd.append(str(qlist1[0]))

                i+=1
            quest=','.join(qd)

            mycursor.execute("update vh_candidate set question=%s where username=%s",(quest,u1))
            mydb.commit()
            #program
            mycursor.execute("SELECT * FROM vh_program where language=%s order by rand()",(rs1[19],))
            plist = mycursor.fetchall()
            i=0
            pgm=""
            for plist1 in plist:
                if i<1:
                    pgm=str(plist1[0])
                i+=1
                    

            mycursor.execute("update vh_candidate set program=%s where username=%s",(pgm,u1))
            mydb.commit()
            ##
            mycursor.execute("SELECT * FROM vh_candidate where username=%s ",(u1,))
            d2 = mycursor.fetchone()
            email=d2[5]
            name=d2[1]

            mess="Dear "+name+", You are selected for Interview, Date:"+sdate+", Time:"+itime+", "+str(mins)+" minutes"
            dt.append(email)
            dt.append(mess)
            edata.append(dt)
        
  

    return render_template('resume_match.html',vid=vid,mdata=mdata,edata=edata,s1=s1)

@app.route('/add_apti',methods=['POST','GET'])
def add_apti():
    msg=""
    act=request.args.get("act") 
    uname=""
    edata=[]
    s1=""
    fn=""
    
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_apti_question")
    data = mycursor.fetchall()

    if request.method=='POST':
        question=request.form['question']
        option1=request.form['option1']
        option2=request.form['option2']
        option3=request.form['option3']
        option4=request.form['option4']
        answer=request.form['answer']
        
        
        mycursor.execute("SELECT max(id)+1 FROM vh_apti_question")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO vh_apti_question(id,question,option1,option2,option3,option4,answer,entryby) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,question,option1,option2,option3,option4,answer,'admin')
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit() 

        msg="success"
        
    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vh_apti_question where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_apti'))
        
    return render_template('add_apti.html',msg=msg,data=data)

@app.route('/add_skill',methods=['POST','GET'])
def add_skill():
    msg=""
    act=request.args.get("act")    
    uname=""
    edata=[]
    s1=""
    fn=""
    
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_program")
    data = mycursor.fetchall()

    if request.method=='POST':
        language=request.form['language']
        program=request.form['program']
        min_lines=request.form['min_lines']
        max_lines=request.form['max_lines']
        keywords=request.form['keywords']
        
        mycursor.execute("SELECT max(id)+1 FROM vh_program")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        file = request.files['file']
        result="q"+str(maxid)+".txt"
        file.save(os.path.join("static/output", result))
        
        sql = "INSERT INTO vh_program(id,language,program,min_lines,max_lines,keywords,result,hr_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,language,program,min_lines,max_lines,keywords,result,'admin')
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit() 

        msg="success"

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vh_program where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_skill'))
        
        
    return render_template('add_skill.html',msg=msg,data=data)

@app.route('/add_apti1',methods=['POST','GET'])
def add_apti1():
    msg=""
    act=request.args.get("act") 
    uname=""
    edata=[]
    s1=""
    fn=""
    
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_apti_question")
    data = mycursor.fetchall()

    if request.method=='POST':
        question=request.form['question']
        option1=request.form['option1']
        option2=request.form['option2']
        option3=request.form['option3']
        option4=request.form['option4']
        answer=request.form['answer']
        
        
        mycursor.execute("SELECT max(id)+1 FROM vh_apti_question")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO vh_apti_question(id,question,option1,option2,option3,option4,answer,entryby) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,question,option1,option2,option3,option4,answer,uname)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit() 

        msg="success"
        
    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vh_apti_question where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_apti1'))
        
    return render_template('add_apti1.html',msg=msg,data=data)

@app.route('/add_skill1',methods=['POST','GET'])
def add_skill1():
    msg=""
    act=request.args.get("act")    
    uname=""
    edata=[]
    s1=""
    fn=""
    
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_program")
    data = mycursor.fetchall()

    if request.method=='POST':
        language=request.form['language']
        program=request.form['program']
        min_lines=request.form['min_lines']
        max_lines=request.form['max_lines']
        keywords=request.form['keywords']
        
        mycursor.execute("SELECT max(id)+1 FROM vh_program")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        file = request.files['file']
        result="q"+str(maxid)+".txt"
        file.save(os.path.join("static/output", result))
        
        sql = "INSERT INTO vh_program(id,language,program,min_lines,max_lines,keywords,result,hr_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,language,program,min_lines,max_lines,keywords,result,uname)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit() 

        msg="success"

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vh_program where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_skill1'))
        
        
    return render_template('add_skill1.html',msg=msg,data=data)

@app.route('/view_candidate',methods=['POST','GET'])
def view_candidate():
    msg=""
    cid=request.args.get("cid")
    uname=""
    edata=[]
    s1=""
    fn=""
    
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where id=%s ",(cid,))
    data = mycursor.fetchone()

    if data[25]=="":
        s=1
    else:
        s1="1"
        f1=data[25].split(".")
        fn=f1[0]+".pdf"

        
    return render_template('view_candidate.html',cid=cid,data=data,fn=fn,s1=s1)

@app.route('/view_candidate1',methods=['POST','GET'])
def view_candidate1():
    msg=""

    uname=""
    edata=[]
    s1=""
    fn=""
    
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s ",(uname,))
    data = mycursor.fetchone()

    if data[25]=="":
        s=1
    else:
        s1="1"
        f1=data[25].split(".")
        fn=f1[0]+".pdf"

        
    return render_template('view_candidate1.html',cid=cid,data=data,fn=fn,s1=s1)

@app.route('/interview_list',methods=['POST','GET'])
def interview_list():
    msg=""
    uname=""
    edata=[]
    s1=""
    
    if 'username' in session:
        uname = session['username']

    now1 = datetime.datetime.now()
    rtime=now1.strftime("%H:%M")
    rtime1=rtime.split(':')
    rmin=int(rtime1[1])

    
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * FROM vh_vacancy where hr_id=%s order by id desc",(uname,))
    rs1 = mycursor.fetchone()
    vid=rs1[0]
    print(vid)
    
    mycursor.execute("SELECT * FROM vh_profile_matched p,vh_candidate c where p.username=c.username && p.interview_status=1 && p.vacancy_id=%s",(vid,))
    mdata = mycursor.fetchall()


    return render_template('interview_list.html',vid=vid,mdata=mdata,edata=edata,s1=s1)

@app.route('/selected_list',methods=['POST','GET'])
def selected_list():
    msg=""
    uname=""
    edata=[]
    s1=""
    
    if 'username' in session:
        uname = session['username']

    now1 = datetime.datetime.now()
    rtime=now1.strftime("%H:%M")
    rtime1=rtime.split(':')
    rmin=int(rtime1[1])

    
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * FROM vh_vacancy where hr_id=%s order by id desc",(uname,))
    rs1 = mycursor.fetchone()
    vid=rs1[0]
    print(vid)
    #1-inw select,2-inw going,3-select,4-reject,5-joined
    
    mycursor.execute("SELECT * FROM vh_profile_matched p,vh_candidate c where p.username=c.username && p.interview_status=3 && p.vacancy_id=%s",(vid,))
    mdata = mycursor.fetchall()


    return render_template('selected_list.html',vid=vid,mdata=mdata,edata=edata,s1=s1)

@app.route('/admin_selected',methods=['POST','GET'])
def admin_selected():
    msg=""
    uname=""
    edata=[]
    s1=""
    
    if 'username' in session:
        uname = session['username']

    now1 = datetime.datetime.now()
    rtime=now1.strftime("%H:%M")
    rtime1=rtime.split(':')
    rmin=int(rtime1[1])

    
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * FROM vh_vacancy order by id desc")
    rs1 = mycursor.fetchone()
    vid=rs1[0]
    print(vid)
    #1-inw select,2-inw going,3-select,4-reject,5-joined
    
    mycursor.execute("SELECT * FROM vh_profile_matched p,vh_candidate c where p.username=c.username && p.interview_status=3 && p.vacancy_id=%s",(vid,))
    mdata = mycursor.fetchall()


    return render_template('admin_selected.html',vid=vid,mdata=mdata,edata=edata,s1=s1)

@app.route('/rejected_list',methods=['POST','GET'])
def rejected_list():
    msg=""
    uname=""
    edata=[]
    s1=""
    
    if 'username' in session:
        uname = session['username']

    now1 = datetime.datetime.now()
    rtime=now1.strftime("%H:%M")
    rtime1=rtime.split(':')
    rmin=int(rtime1[1])

    
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * FROM vh_vacancy where hr_id=%s order by id desc",(uname,))
    rs1 = mycursor.fetchone()
    vid=rs1[0]
    print(vid)
    #1-inw select,2-inw going,3-select,4-reject,5-joined
    
    mycursor.execute("SELECT * FROM vh_profile_matched p,vh_candidate c where p.username=c.username && p.interview_status=4 && p.vacancy_id=%s",(vid,))
    mdata = mycursor.fetchall()


    return render_template('rejected_list.html',vid=vid,mdata=mdata,edata=edata,s1=s1)

@app.route('/joined_list',methods=['POST','GET'])
def joined_list():
    msg=""
    uname=""
    mdata=[]
    s1=""
    
    if 'username' in session:
        uname = session['username']

    now1 = datetime.datetime.now()
    rtime=now1.strftime("%H:%M")
    rtime1=rtime.split(':')
    rmin=int(rtime1[1])

    
    mycursor = mydb.cursor(buffered=True)

    
    mycursor.execute("SELECT * FROM vh_joined p,vh_candidate c where p.candidate=c.username && p.hr_id=%s",(uname,))
    mdata = mycursor.fetchall()


    return render_template('joined_list.html',mdata=mdata,s1=s1)

@app.route('/job_details',methods=['POST','GET'])
def job_details():
    msg=""
    email=""
    mess=""
    act=request.args.get("act")
    uname=""
    data=[]
    mdata=[]
    s1=""
    s2=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM vh_joined p,vh_candidate c where p.candidate=c.username && p.candidate=%s",(uname,))
    mdat = mycursor.fetchall()

    for mm in mdat:
        dt=[]

        dt.append(mm[0])
        dt.append(mm[1])
        dt.append(mm[2])
        dt.append(mm[3])
        dt.append(mm[4])
        dt.append(mm[5])
        dt.append(mm[6])
        dt.append(mm[7])
        dt.append(mm[8])
        dt.append(mm[9])
        dt.append(mm[10])
        dt.append(mm[11])
        dt.append(mm[13])
        vid=mm[1]
        mycursor.execute("SELECT * FROM vh_vacancy where id=%s",(vid, ))
        dd = mycursor.fetchone()
        company=dd[21]
        dt.append(company)
        mdata.append(dt)

    return render_template('job_details.html',msg=msg,act=act,data=data,mdata=mdata)

@app.route('/testface',methods=['POST','GET'])
def testface():
    msg=""
    res=""
    vid=request.args.get("vid")
    pid=request.args.get("pid")
    uname=""
    s1=""

    act=""
    if 'username' in session:
        uname = session['username']

    ff=open("scount.txt","r")
    sv=ff.read()
    ff.close()

    n=int(sv)+1
    nn=str(n)
    ff=open("img.txt","r")
    fv=ff.read()
    ff.close()
    if n>4:
        res="1"

    if fv=="1":

        ff=open("scount.txt","w")
        ff.write(nn)
        ff.close()
        msg="Face Turned"
        
    if fv=="0":
        msg="Face not Found"

    return render_template('testface.html',msg=msg,res=res,pid=pid,vid=vid)
        
@app.route('/test_apti',methods=['POST','GET'])
def test_apti():
    msg=""
    uname=""
    s1=""
    st=""
    data1=[]
    qid=""
    cans=""
    vid=request.args.get("vid")
    pid=request.args.get("pid")
    act=""
    if 'username' in session:
        uname = session['username']
    ff=open("uname.txt","r")
    uname=ff.read()
    ff.close()
    
    ff=open("img.txt","r")
    fv=ff.read()
    ff.close()
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()

    n=1

    qtn=data[28]
    print(qtn)
    qn=qtn.split(',')
    #qn=[4,2,9,7,1]
    tot=len(qn)

    mycursor.execute("SELECT count(*) FROM vh_temp where username=%s && pid=%s",(uname,pid))
    tcnt = mycursor.fetchone()[0]
    if tcnt==0:
        for qq in qn:
            mycursor.execute("SELECT max(id)+1 FROM vh_temp")
            maxid2 = mycursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql2 = "INSERT INTO vh_temp(id,username,pid,qid,uans) VALUES (%s, %s, %s,%s,%s)"
            val2 = (maxid2,uname,pid,qq,'0')
            mycursor.execute(sql2, val2)
            mydb.commit()
                    
    
    mycursor.execute("SELECT * FROM vh_vacancy where id=%s",(vid,))
    vdata = mycursor.fetchone()
    max_apti=vdata[18]
    
    mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
    adata = mycursor.fetchone()
    act=adata[7]

    #act="5"
    #ff=open("static/apti.txt","r")
    #act=ff.read()
    #ff.close()
    print("dd")
    print(qid)
    if act=="":
        act="1"
        qid=qn[0]
    else:
        
        n=int(act)+1
        act=str(n)
        if n<=tot:
            p=n-1
            qid=qn[p]
    
    #mycursor.execute("SELECT * FROM vh_apti_question where id=%s",(qid,))
    #data1 = mycursor.fetchone()
    #cans=str(data1[6])

    '''print("qid")
    print(qid)
    print("ans")
    print(cans)'''
    x=0
    '''if request.method=='POST':
        
        ans1=request.form['answer']
        qid1=request.form['qid1']
        cans1=request.form['cans1']

        if ans1==cans1:
            x=1
        else:
            x=0

        
        mycursor.execute("update vh_profile_matched set interview_status=2,apti=%s where id=%s",(act,pid))
        mydb.commit()

        mycursor.execute("update vh_temp set uans=%s where username=%s && qid=%s && pid=%s",(x,uname,qid1,pid))
        mydb.commit()

        mycursor.execute("SELECT sum(uans) FROM vh_temp where username=%s && pid=%s",(uname,pid))
        ncorrect = mycursor.fetchone()[0]

        ap=(ncorrect/max_apti)*100
        apti_score=round(ap,2)
        mycursor.execute("update vh_profile_matched set correct=%s,apti_score=%s where id=%s",(ncorrect,apti_score,pid))
        mydb.commit()

        if n==tot:
            msg="done"
            ##emo
            emo_arr=['neutral','happy','angry','sad','fear','surprise']
            ef=open("emotion.txt","r")
            emm=ef.read()
            ef.close()

            em=emm.split(',')
            emlen=len(em)-1
            e1=0
            e2=0
            e3=0
            e4=0
            e5=0
            e6=0
            emotion=""
            i=0
            while i<emlen:
                er=em[i]
                if er=='neutral':
                    e1+=1
                if er=='happy':
                    e2+=1
                if er=='angry':
                    e3+=1
                if er=='sad':
                    e4+=1
                if er=='fear':
                    e5+=1
                if er=='surprise':
                    e6+=1
                i+=1

            if e1>e2 and e1>e3 and e1>e4 and e1>e5 and e1>e6:
                emotion='Neutral'
            elif e2>e3 and e2>e4 and e2>e5 and e2>e6:
                emotion='Happy'
            elif e3>e4 and e3>e5 and e3>e6:
                emotion='Angry'
            elif e4>e5 and e4>e6:
                emotion='Sad'
            elif e5>e6:
                emotion='Fear'
            else:
                emotion='Surprise'
            mycursor.execute("update vh_profile_matched set emotion=%s where id=%s",(emotion,pid))
            mydb.commit()
                
            ##
            if apti_score>=60:
                st="yes"
            else:
                st="no"
        else:
            msg="ok"'''


    return render_template('test_apti.html',msg=msg,act=act,s1=s1,data=data,data1=data1,pid=pid,vid=vid,st=st,qid=qid,cans=cans)

@app.route('/test_apti1',methods=['POST','GET'])
def test_apti1():
    msg=""
    uname=""
    s1=""
    st=""
    data1=[]
    qid=""
    cans=""
    vid=request.args.get("vid")
    pid=request.args.get("pid")
    act=""
    if 'username' in session:
        uname = session['username']

    ff=open("uname.txt","r")
    uname=ff.read()
    ff.close()
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()

    n=1

    qtn=data[28]
    qn=qtn.split(',')
    #qn=[4,2,9,7,1]
    tot=len(qn)

    mycursor.execute("SELECT count(*) FROM vh_temp where username=%s && pid=%s",(uname,pid))
    tcnt = mycursor.fetchone()[0]
    if tcnt==0:
        for qq in qn:
            mycursor.execute("SELECT max(id)+1 FROM vh_temp")
            maxid2 = mycursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql2 = "INSERT INTO vh_temp(id,username,pid,qid,uans) VALUES (%s, %s, %s,%s,%s)"
            val2 = (maxid2,uname,pid,qq,'0')
            mycursor.execute(sql2, val2)
            #mydb.commit()
                    
    
    mycursor.execute("SELECT * FROM vh_vacancy where id=%s",(vid,))
    vdata = mycursor.fetchone()
    max_apti=vdata[18]
    
    mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
    adata = mycursor.fetchone()
    act=adata[7]
    print("actttt")
    print(act)
        
    #ff=open("static/apti.txt","r")
    #act=ff.read()
    #ff.close()
    
    if act=="":
        act="1"
        qid=qn[0]
        print("ccc")
    else:
        print("dddd")
        n=int(act)+1
        act=str(n)
        if n<=tot:
            p=n-1
            qid=qn[p]
    
    mycursor.execute("SELECT * FROM vh_apti_question where id=%s",(qid,))
    data1 = mycursor.fetchone()
    cans=str(data1[6])

    '''print("qid")
    print(qid)
    print("ans")
    print(cans)'''
    x=0
    ncorrect=0
    if request.method=='POST':
        
        ans1=request.form['answer']
        qid1=request.form['qid1']
        cans1=request.form['cans1']

        if ans1==cans1:
            x=1
        else:
            x=0

        
        mycursor.execute("update vh_profile_matched set interview_status=2,apti=%s where id=%s",(act,pid))
        mydb.commit()

        mycursor.execute("update vh_temp set uans=%s where username=%s && qid=%s && pid=%s",(x,uname,qid1,pid))
        mydb.commit()

        mycursor.execute("SELECT sum(uans) FROM vh_temp where username=%s && pid=%s",(uname,pid))
        ncorrect = mycursor.fetchone()[0]

        ap=1
        apti_score=1
        if ncorrect>0:
            ap=(ncorrect/max_apti)*100
            apti_score=round(ap,2)
            mycursor.execute("update vh_profile_matched set correct=%s,apti_score=%s where id=%s",(ncorrect,apti_score,pid))
            mydb.commit()

            if max_apti==0:
                max_apti=1
            if n==tot:
                msg="done"
                ##emo
                emo_arr=['neutral','happy','angry','sad','fear','surprise']
                ef=open("emotion.txt","r")
                emm=ef.read()
                ef.close()

                em=emm.split(',')
                emlen=len(em)-1
                e1=0
                e2=0
                e3=0
                e4=0
                e5=0
                e6=0
                emotion=""
                i=0
                while i<emlen:
                    er=em[i]
                    if er=='neutral':
                        e1+=1
                    if er=='happy':
                        e2+=1
                    if er=='angry':
                        e3+=1
                    if er=='sad':
                        e4+=1
                    if er=='fear':
                        e5+=1
                    if er=='surprise':
                        e6+=1
                    i+=1

                if e1>e2 and e1>e3 and e1>e4 and e1>e5 and e1>e6:
                    emotion='Neutral'
                elif e2>e3 and e2>e4 and e2>e5 and e2>e6:
                    emotion='Happy'
                elif e3>e4 and e3>e5 and e3>e6:
                    emotion='Angry'
                elif e4>e5 and e4>e6:
                    emotion='Sad'
                elif e5>e6:
                    emotion='Fear'
                else:
                    emotion='Surprise'
                mycursor.execute("update vh_profile_matched set emotion=%s where id=%s",(emotion,pid))
                mydb.commit()
                    
                ##
                if apti_score>=60:
                    st="yes"
                else:
                    st="no"
            else:
                msg="ok"


    return render_template('test_apti1.html',msg=msg,act=act,s1=s1,data=data,data1=data1,pid=pid,vid=vid,st=st,qid=qid,cans=cans)

@app.route('/sub_program',methods=['POST','GET'])
def sub_program():

    ff=open("static/path.txt","r")
    path=ff.read()
    ff.close()

    import subprocess
    fname=request.args.get("fname")
    result = subprocess.run(["python", path+"/program/"+fname], capture_output=True, text=True)

    ff=open(path+"/program/output.txt","w")
    ff.write(result.stdout)
    ff.close()
    #print(result.stdout)

    return render_template('sub_program.html')

@app.route('/gettime',methods=['POST','GET'])
def gettime():

    return render_template('gettime.html')

@app.route('/test_program',methods=['POST','GET'])
def test_program():
    msg=""
    act=request.args.get("act")
    pid=request.args.get("pid")
    vid=request.args.get("vid")
    uname=""
    ccode=""
    answer=""
    
    fname=request.args.get("fname")
    if 'username' in session:
        uname = session['username']

    ff=open("uname.txt","r")
    uname=ff.read()
    ff.close()
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()
    prid=data[29]

    mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
    adata = mycursor.fetchone()
    

    mycursor.execute("SELECT * FROM vh_vacancy where id=%s",(vid, ))
    data1 = mycursor.fetchone()
    program=data1[19]
    #program="Python"

    mycursor.execute("SELECT * FROM vh_program where id=%s",(prid, ))
    data2 = mycursor.fetchone()
    keyword=data2[5]
    lin1=data2[3]
    lin2=data2[4]
    outfile=data2[6]

    ff=open("static/output/"+outfile,"r")
    outans=ff.read()
    ff.close()
    
    
    ff=open("static/path.txt","r")
    path=ff.read()
    ff.close()


    ff=open(path+"/program/output.txt","r")
    answer=ff.read()
    ff.close()

    '''if act=="1":

        if outans==answer:
            v3=40
            mycursor.execute("update vh_profile_matched set program_score=program_score+%s where id=%s",(v3,pid))
            mydb.commit()
        
        file1 = open(path+"/program/"+fname, 'r')
        Lines = file1.readlines()
         
        count = 0
        result=""
        # Strips the newline character
        for line in Lines:
            result = "".join(line for line in Lines if not line.isspace())
            count += 1
            #print("Line{}: {}".format(count, line.strip()))
        ccode=result

        ff=open(path+"/program/"+fname,"w")
        ff.write(ccode)
        ff.close()

        ##emo
        emo_arr=['neutral','happy','angry','sad','fear','surprise']
        ef=open("emotion.txt","r")
        emm=ef.read()
        ef.close()

        em=emm.split(',')
        emlen=len(em)-1
        e1=0
        e2=0
        e3=0
        e4=0
        e5=0
        e6=0
        emotion=""
        i=0
        while i<emlen:
            er=em[i]
            if er=='neutral':
                e1+=1
            if er=='happy':
                e2+=1
            if er=='angry':
                e3+=1
            if er=='sad':
                e4+=1
            if er=='fear':
                e5+=1
            if er=='surprise':
                e6+=1
            i+=1

        if e1>e2 and e1>e3 and e1>e4 and e1>e5 and e1>e6:
            emotion='Neutral'
        elif e2>e3 and e2>e4 and e2>e5 and e2>e6:
            emotion='Happy'
        elif e3>e4 and e3>e5 and e3>e6:
            emotion='Angry'
        elif e4>e5 and e4>e6:
            emotion='Sad'
        elif e5>e6:
            emotion='Fear'
        else:
            emotion='Surprise'
        mycursor.execute("update vh_profile_matched set emotion=%s where id=%s",(emotion,pid))
        mydb.commit()
            
        ##
        mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
        ds1 = mycursor.fetchone()
        if ds1[10]>=60:
            msg="yes"
        else:
            msg="no"
    ##
    v1=0
    v2=0
    v3=0
    if request.method=='POST':
       
        ccode=request.form['ccode']
        fname=request.form['fname']

        mycursor.execute("update vh_profile_matched set program_score=0 where id=%s",(pid,))
        mydb.commit()
        ###                
        ff=open(path+"/program/"+fname,"w")
        ff.write(ccode)
        ff.close()
        
        ff=open(path+"/program/"+fname,"r")
        fdata=ff.read()
        ff.close()

        k=0
        ky=keyword.split(",")
        for k1 in ky:
            if k1 in fdata:
                print(k1)
                k+=1

        if k>0:
            v1=30
        ###
        file1 = open(path+"/program/"+fname,"r")
        Lines = file1.readlines()
         
        count = 0
        # Strips the newline character
        for line in Lines:
            count += 1
            #print("Line{}: {}".format(count, line.strip()))
        
        print("lines")
        print(count)
        if lin1<=count:
            v2=30
        ###
        ff=open(path+"/program/"+fname,"r")
        fdata=ff.read()
        ff.close()
        ###
        vv=v1+v2
        mycursor.execute("update vh_profile_matched set program_score=%s where id=%s",(vv,pid))
        mydb.commit()
        ###
        
        
        msg="ok"'''

    return render_template('test_program.html',msg=msg,act=act,pid=pid,vid=vid,ccode=ccode,fname=fname,answer=answer,program=program,data=data,data2=data2)

@app.route('/test_program1',methods=['POST','GET'])
def test_program1():
    msg=""
    act=request.args.get("act")
    pid=request.args.get("pid")
    vid=request.args.get("vid")
    uname=""
    ccode=""
    answer=""
    
    fname=request.args.get("fname")
    if 'username' in session:
        uname = session['username']

    ff=open("uname.txt","r")
    uname=ff.read()
    ff.close()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()
    prid=data[29]

    mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
    adata = mycursor.fetchone()
    

    mycursor.execute("SELECT * FROM vh_vacancy where id=%s",(vid, ))
    data1 = mycursor.fetchone()
    program=data1[19]
    #program="Python"

    mycursor.execute("SELECT * FROM vh_program where id=%s",(prid, ))
    data2 = mycursor.fetchone()
    keyword=data2[5]
    lin1=data2[3]
    lin2=data2[4]
    outfile=data2[6]

    ff=open("static/output/"+outfile,"r")
    outans=ff.read()
    ff.close()
    
    
    ff=open("static/path.txt","r")
    path=ff.read()
    ff.close()


    ff=open(path+"/program/output.txt","r")
    answer=ff.read()
    ff.close()

    if act=="1":

        if outans==answer:
            v3=40
            mycursor.execute("update vh_profile_matched set program_score=program_score+%s where id=%s",(v3,pid))
            mydb.commit()
        
        file1 = open(path+"/program/"+fname, 'r')
        Lines = file1.readlines()
         
        count = 0
        result=""
        # Strips the newline character
        for line in Lines:
            result = "".join(line for line in Lines if not line.isspace())
            count += 1
            #print("Line{}: {}".format(count, line.strip()))
        ccode=result

        ff=open(path+"/program/"+fname,"w")
        ff.write(ccode)
        ff.close()

        ##emo
        emo_arr=['neutral','happy','angry','sad','fear','surprise']
        ef=open("emotion.txt","r")
        emm=ef.read()
        ef.close()

        em=emm.split(',')
        emlen=len(em)-1
        e1=0
        e2=0
        e3=0
        e4=0
        e5=0
        e6=0
        emotion=""
        i=0
        while i<emlen:
            er=em[i]
            if er=='neutral':
                e1+=1
            if er=='happy':
                e2+=1
            if er=='angry':
                e3+=1
            if er=='sad':
                e4+=1
            if er=='fear':
                e5+=1
            if er=='surprise':
                e6+=1
            i+=1

        if e1>e2 and e1>e3 and e1>e4 and e1>e5 and e1>e6:
            emotion='Neutral'
        elif e2>e3 and e2>e4 and e2>e5 and e2>e6:
            emotion='Happy'
        elif e3>e4 and e3>e5 and e3>e6:
            emotion='Angry'
        elif e4>e5 and e4>e6:
            emotion='Sad'
        elif e5>e6:
            emotion='Fear'
        else:
            emotion='Surprise'
        mycursor.execute("update vh_profile_matched set emotion=%s where id=%s",(emotion,pid))
        mydb.commit()
            
        ##
        mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
        ds1 = mycursor.fetchone()
        if ds1[10]>=60:
            msg="yes"
        else:
            msg="no"
    ##
    v1=0
    v2=0
    v3=0
    if request.method=='POST':
       
        ccode=request.form['ccode']
        fname=request.form['fname']

        mycursor.execute("update vh_profile_matched set program_score=0 where id=%s",(pid,))
        mydb.commit()
        ###                
        ff=open(path+"/program/"+fname,"w")
        ff.write(ccode)
        ff.close()
        
        ff=open(path+"/program/"+fname,"r")
        fdata=ff.read()
        ff.close()

        k=0
        ky=keyword.split(",")
        for k1 in ky:
            if k1 in fdata:
                print(k1)
                k+=1

        if k>0:
            v1=30
        ###
        file1 = open(path+"/program/"+fname,"r")
        Lines = file1.readlines()
         
        count = 0
        # Strips the newline character
        for line in Lines:
            count += 1
            #print("Line{}: {}".format(count, line.strip()))
        
        print("lines")
        print(count)
        if lin1<=count:
            v2=30
        ###
        ff=open(path+"/program/"+fname,"r")
        fdata=ff.read()
        ff.close()
        ###
        vv=v1+v2
        mycursor.execute("update vh_profile_matched set program_score=%s where id=%s",(vv,pid))
        mydb.commit()
        ###
        
        
        msg="ok"

    return render_template('test_program1.html',msg=msg,act=act,pid=pid,vid=vid,ccode=ccode,fname=fname,answer=answer,program=program,data=data,data2=data2)

#Speech analysis
##NLP
def tokenizer(text):
    for token in wordpunct_tokenize(text):
        if token not in ENGLISH_STOP_WORDS:
            tag = tagger_mem(frozenset({token}))
            yield lemmatize_mem(token, tags.get(tag[0][1],  wn.NOUN))

    # Pipeline definition
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(
            tokenizer=tokenizer,
            ngram_range=(1, 2),
            stop_words=ENGLISH_STOP_WORDS,
            sublinear_tf=True,
            min_df=0.00009
        )),
        ('classifier', SGDClassifier(
            alpha=1e-4, n_jobs=-1
        )),
    ])

    # Cross validate using k-fold
    y_pred = cross_val_predict(
        pipeline, dataset.get('data'),
        y=dataset.get('target'),
        cv=10, n_jobs=-1, verbose=20
    )

    # Compute precison, recall and f1 scode.
    cr = classification_report(
        dataset.get('target'), y_pred,
        target_names=dataset.get('target_names'),
        digits=3
    )

    # Confusion matrix
    cm = confusion_matrix(dataset.get('target'), y_pred)

    # Get max length of category names for printing
    label_length = len(
        sorted(dataset['target_names'], key=len, reverse=True)[0]
    )

    # Make shortened labels for plotting
    short_labels = []
    for i in dataset['target_names']:
        short_labels.append(
            ' '.join(map(lambda x: x[:3].strip(), i.split(' > ')))
        )

    # Printing Classification Report
    print('{label:>{length}}'.format(
        label='Classification Report',
        length=label_length
    ), cr, sep='\n')

    # Pretty printing confusion matrix
    print('{label:>{length}}\n'.format(
        label='Confusion Matrix',
        length=abs(label_length - 50)
    ))
    for index, val in enumerate(cm):
        print(
            '{label:>{length}} {prediction}'.format(
                length=abs(label_length - 50),
                label=short_labels[index],
                prediction=''.join(map(lambda x: '{:>5}'.format(x), val))
            )
        )
#############

def speak(audio):
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()

@app.route('/test_cam',methods=['POST','GET'])
def test_cam():
    msg=""
    question=""
    act=request.args.get("act")
    pid=request.args.get("pid")
    vid=request.args.get("vid")
    act1=0
    mdata=[]
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("uname.txt","r")
    uname=ff.read()
    ff.close()
    mycursor = mydb.cursor()
    uname="harish"
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()
    gend=data[2]

    mycursor.execute("SELECT count(*) FROM vh_temp2 where username=%s && pid=%s",(uname,pid))
    tcnt = mycursor.fetchone()[0]
    if tcnt==0:
        i=1
        while i<=5:
            mycursor.execute("SELECT max(id)+1 FROM vh_temp2")
            maxid2 = mycursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql2 = "INSERT INTO vh_temp2(id,username,pid,qid,uans) VALUES (%s, %s, %s,%s,%s)"
            val2 = (maxid2,uname,pid,i,'')
            mycursor.execute(sql2, val2)
            mydb.commit()
            i+=1
    
    if act=="no":
        s=1
    else:
        if act is None:
            act=0
        else:
            act=int(act)
            act1=act+1
            
        
        mycursor.execute("SELECT * FROM vh_interview_question limit %s,1",(act,))
        mdata1 = mycursor.fetchone()

        question=mdata1[1]

        act2=act+1
        mycursor.execute("SELECT * FROM vh_interview_question a,vh_temp2 b where a.id=b.qid && b.pid=%s && b.username=%s limit %s",(pid,uname,act2))
        mdata = mycursor.fetchall()
    
        
        if act1<6:
            
            speak(question)
            act=str(act)
            '''if act1==5:
                mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
                rdata = mycursor.fetchone()
                score=rdata[11]
                if score>=50:
                    msg="yes"
                else:
                    msg="no"'''
        else:

            mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
            rdata = mycursor.fetchone()
            score=rdata[11]

            ##emo
            emo_arr=['neutral','happy','angry','sad','fear','surprise']
            ef=open("emotion.txt","r")
            emm=ef.read()
            ef.close()

            em=emm.split(',')
            emlen=len(em)-1
            e1=0
            e2=0
            e3=0
            e4=0
            e5=0
            e6=0
            emotion=""
            i=0
            while i<emlen:
                er=em[i]
                if er=='neutral':
                    e1+=1
                if er=='happy':
                    e2+=1
                if er=='angry':
                    e3+=1
                if er=='sad':
                    e4+=1
                if er=='fear':
                    e5+=1
                if er=='surprise':
                    e6+=1
                i+=1

            if e1>e2 and e1>e3 and e1>e4 and e1>e5 and e1>e6:
                emotion='Neutral'
            elif e2>e3 and e2>e4 and e2>e5 and e2>e6:
                emotion='Happy'
            elif e3>e4 and e3>e5 and e3>e6:
                emotion='Angry'
            elif e4>e5 and e4>e6:
                emotion='Sad'
            elif e5>e6:
                emotion='Fear'
            else:
                emotion='Surprise'
            mycursor.execute("update vh_profile_matched set emotion=%s where id=%s",(emotion,pid))
            mydb.commit()
                
            ##
            if score>=50:
                msg="yes"
                mycursor.execute("update vh_profile_matched set interview_status=3 where id=%s",(pid,))
                mydb.commit()
            else:
                msg="no"
                mycursor.execute("update vh_profile_matched set interview_status=4 where id=%s",(pid,))
                mydb.commit()

    if request.method=='POST':
        
        res=request.form['res']

        mycursor.execute("update vh_temp2 set uans=%s where username=%s && pid=%s && qid=%s",(res,uname,pid,act))
        mydb.commit()

        ff=open("static/data.txt","r")
        dd=ff.read()
        ff.close()

        d1=dd.split(",")
        v1=0
        v2=0
        x=0
      
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=1",(uname,pid))
        m1 = mycursor.fetchone()
        if m1[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m1[4]:
                    x+=1
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=2",(uname,pid))
        m2 = mycursor.fetchone()
        if m2[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m2[4]:
                    x+=1
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=3",(uname,pid))
        m3 = mycursor.fetchone()
        if m3[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m3[4]:
                    x+=1
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=4",(uname,pid))
        m4 = mycursor.fetchone()
        if m4[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m4[4]:
                    x+=1
            
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=5",(uname,pid))
        m5 = mycursor.fetchone()
        if m5[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m5[4]:
                    x+=1
        print("words")
        print(x)
        if x>=3:
            v2=40
        elif x>=2:
            v2=30
        elif x>=1:
            v2=20

        score=v1+v2
        mycursor.execute("update vh_profile_matched set test_score=%s where id=%s",(score,pid))
        mydb.commit()

        

    return render_template('test_cam.html',msg=msg,act=act1,question=question,data=data,mdata=mdata,pid=pid,vid=vid,gend=gend)


@app.route('/test_cam1',methods=['POST','GET'])
def test_cam1():
    msg=""
    question=""
    act=request.args.get("act")
    pid=request.args.get("pid")
    vid=request.args.get("vid")
    act1=0
    mdata=[]
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("uname.txt","r")
    uname=ff.read()
    ff.close()
    mycursor = mydb.cursor()
    uname="harish"
    mycursor.execute("SELECT * FROM vh_candidate where username=%s",(uname, ))
    data = mycursor.fetchone()
    gend=data[2]

    mycursor.execute("SELECT count(*) FROM vh_temp2 where username=%s && pid=%s",(uname,pid))
    tcnt = mycursor.fetchone()[0]
    if tcnt==0:
        i=1
        while i<=5:
            mycursor.execute("SELECT max(id)+1 FROM vh_temp2")
            maxid2 = mycursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql2 = "INSERT INTO vh_temp2(id,username,pid,qid,uans) VALUES (%s, %s, %s,%s,%s)"
            val2 = (maxid2,uname,pid,i,'')
            mycursor.execute(sql2, val2)
            mydb.commit()
            i+=1
    
    if act=="no":
        s=1
    else:
        if act is None:
            act=0
        else:
            act=int(act)
            act1=act+1
            
        
        mycursor.execute("SELECT * FROM vh_interview_question limit %s,1",(act,))
        mdata1 = mycursor.fetchone()

        question=mdata1[1]

        act2=act+1
        mycursor.execute("SELECT * FROM vh_interview_question a,vh_temp2 b where a.id=b.qid && b.pid=%s && b.username=%s limit %s",(pid,uname,act2))
        mdata = mycursor.fetchall()
    
        
        if act1<6:
            
            speak(question)
            act=str(act)
            '''if act1==5:
                mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
                rdata = mycursor.fetchone()
                score=rdata[11]
                if score>=50:
                    msg="yes"
                else:
                    msg="no"'''
        else:

            mycursor.execute("SELECT * FROM vh_profile_matched where id=%s",(pid,))
            rdata = mycursor.fetchone()
            score=rdata[11]

            ##emo
            emo_arr=['neutral','happy','angry','sad','fear','surprise']
            ef=open("emotion.txt","r")
            emm=ef.read()
            ef.close()

            em=emm.split(',')
            emlen=len(em)-1
            e1=0
            e2=0
            e3=0
            e4=0
            e5=0
            e6=0
            emotion=""
            i=0
            while i<emlen:
                er=em[i]
                if er=='neutral':
                    e1+=1
                if er=='happy':
                    e2+=1
                if er=='angry':
                    e3+=1
                if er=='sad':
                    e4+=1
                if er=='fear':
                    e5+=1
                if er=='surprise':
                    e6+=1
                i+=1

            if e1>e2 and e1>e3 and e1>e4 and e1>e5 and e1>e6:
                emotion='Neutral'
            elif e2>e3 and e2>e4 and e2>e5 and e2>e6:
                emotion='Happy'
            elif e3>e4 and e3>e5 and e3>e6:
                emotion='Angry'
            elif e4>e5 and e4>e6:
                emotion='Sad'
            elif e5>e6:
                emotion='Fear'
            else:
                emotion='Surprise'
            mycursor.execute("update vh_profile_matched set emotion=%s where id=%s",(emotion,pid))
            mydb.commit()
                
            ##
            if score>=50:
                msg="yes"
                mycursor.execute("update vh_profile_matched set interview_status=3 where id=%s",(pid,))
                mydb.commit()
            else:
                msg="no"
                mycursor.execute("update vh_profile_matched set interview_status=4 where id=%s",(pid,))
                mydb.commit()

    if request.method=='POST':
        
        res=request.form['res']

        mycursor.execute("update vh_temp2 set uans=%s where username=%s && pid=%s && qid=%s",(res,uname,pid,act))
        mydb.commit()

        ff=open("static/data.txt","r")
        dd=ff.read()
        ff.close()

        d1=dd.split(",")
        v1=0
        v2=0
        x=0
      
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=1",(uname,pid))
        m1 = mycursor.fetchone()
        if m1[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m1[4]:
                    x+=1
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=2",(uname,pid))
        m2 = mycursor.fetchone()
        if m2[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m2[4]:
                    x+=1
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=3",(uname,pid))
        m3 = mycursor.fetchone()
        if m3[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m3[4]:
                    x+=1
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=4",(uname,pid))
        m4 = mycursor.fetchone()
        if m4[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m4[4]:
                    x+=1
            
        mycursor.execute("SELECT * FROM vh_temp2 where username=%s && pid=%s && qid=5",(uname,pid))
        m5 = mycursor.fetchone()
        if m5[4]=="":
            s=1
        else:
            v1+=10
            for d2 in d1:
                if d2 in m5[4]:
                    x+=1
        print("words")
        print(x)
        if x>=3:
            v2=40
        elif x>=2:
            v2=30
        elif x>=1:
            v2=20

        score=v1+v2
        mycursor.execute("update vh_profile_matched set test_score=%s where id=%s",(score,pid))
        mydb.commit()

        

    return render_template('test_cam1.html',msg=msg,act=act1,question=question,data=data,mdata=mdata,pid=pid,vid=vid,gend=gend)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))

def gen2(camera):
    
    while True:
        frame = camera.get_frame()


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed2')
def video_feed2():

    return Response(gen2(VideoCamera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
