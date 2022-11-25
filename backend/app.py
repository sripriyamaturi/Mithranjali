
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from email.message import EmailMessage
import ssl
import smtplib
import requests
import smtplib
from email.message import EmailMessage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from random import randint
from fastapi import FastAPI,Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
import os
import pymongo
from typing import List

from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

class EmailSchema(BaseModel):
    email: List[EmailStr]

app = FastAPI(title="Chaarminar", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/verify')
async def verify(request : Request):
    k = await request.json()
    email_sender = "sripriyamaturi8@gmail.com"
    email_password = "kawsuxixaxjxvtdb"
    email_receiver = k['email']

    subject = "Mithranjali ApnaFood - Email Verification"
    otp=randint(0000,9999)
    body = """
    Your otp for email verification is - 
    """ + str(otp)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject 
    em.set_content(body)
    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465, context = context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    except Exception as e:
        print(e)


@app.post('/register')
async def register(request : Request ):
    k = await request.json()
    uname = k['username']
    password = k['password']
    email = k['email']
    phonenum = k['phonenumber']
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mithranjali"]
    print(mydb)
    mycol = mydb["all_users"]
    # x = mycol.find_one()
    # print(x)
    mydict = { "username": uname, "email": email, "pass":password,"mobile" : phonenum }
    x = mycol.insert_one(mydict)
    print(x)
    pass



if __name__ == "__main__":
    
    uvicorn.run(
        app,
        port=5000,
        host="127.0.0.1",
    )
