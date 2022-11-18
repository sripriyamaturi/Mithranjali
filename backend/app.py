
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
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



#conf = ConnectionConfig(MAIL_USERNAME="sripriyamaturi8",MAIL_FROM="sripriyamaturi8@gmail.com",MAIL_PASSWORD="917203sp",MAIL_PORT=587,MAIL_SERVER="smtp.gmail.com",MAIL_STARTTLS=True,MAIL_SSL_TLS=False)

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
    otp=randint(0000,9999)
    #req = request.body
    k = await request.json()
    print(k)
    message = Mail(from_email='udaymaturi51@gmail.com',to_emails= k['email'],subject='ApnaFood - Email verification',html_content='<strong>Your otp is - </strong><br>' + str(otp))
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
    return {"otp" : otp}

@app.post('/register')
def register( ):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mith"]
    print(mydb)
    mycol = mydb["register"]
    # x = mycol.find_one()
    # print(x)
    mydict = { "username": "John", "email": "hi@gmail.com", "pass":"hi","mobile" : "9999999999" }
    x = mycol.insert_one(mydict)
    print(x)
    pass

if __name__ == "__main__":
    #register()
    uvicorn.run(
        app,
        port=5000,
        host="127.0.0.1",
    )
