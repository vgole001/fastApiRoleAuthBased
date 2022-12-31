import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Use load_env to trace the path of .env file:
load_dotenv() 

email = os.environ["EMAIL"]
password = os.environ["PASSWORD"]


def send_mail(to, username, user_id):
    msg = EmailMessage()
    msg.add_alternative(
        f"""\
<html>
  <head>
    <title>Document</title>
  </head>
  <body>
    <div id="box">
      <h2>Hallo {username},</h2> 
        <p> Click here to activate the user </p>
        <a href="http://127.0.0.1:8000/docs#/activate/{user_id}">Click here </a>
      </form>
    </div>
    <footer>
        <div id="container" style="white-space:nowrap">
            <div id="image" style="display:inline;">
                <img src="/static/images/environment_image.jpg" style="width:15px; height:15px; "/>
            </div>
            <div id="texts" style="display:inline; white-space:nowrap;"> 
                Please consider the environment before printing this email
            </div>
        </div>
    </footer>
  </body>
</html>
<style>
  #box {{
    margin: 0 auto;
    max-width: 500px;
    border: 1px solid black;
    height: 200px;
    text-align: center;
    background: lightgray;
  }}
  #emailSignature{{
      color: #00cc00;
  }}
  p {{
    padding: 10px 10px;
    font-size: 18px;
  }}
  .inline {{
    display: inline;
  }}
  .link-button {{
    background: none;
    border: none;
    color: blue;
    font-size: 22px;
    text-decoration: underline;
    cursor: pointer;
    font-family: serif;
  }}
  .link-button:focus {{
    outline: none;
  }}
  .link-button:active {{
    color: red;
  }}
</style>
    """,
        subtype="html",
    )

 

# try:
    msg["Subject"] = "Confirm of Registration"
    msg["From"] = email
    msg["To"] = to
    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(email, password)
    server.send_message(msg)
    server.quit()
# except Exception as exception:
#     print("Error: %s!\n\n" % exception)