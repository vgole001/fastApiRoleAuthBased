import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Use load_env to trace the path of .env file:
load_dotenv() 

email = os.environ["EMAIL"]
password = os.environ["PASSWORD"]

def send_mail(to, first_name, last_name, role, user_id):
    msg = EmailMessage()
    msg.add_alternative(
        f"""\
<html>
  <head>
    <title>Document</title>
  </head>
  <body>
    <div id="box">
      <h2>{first_name} {last_name} has been registered as {role}</h2> 
        <p> Click the link below to activate the account </p>
        <a href="http://127.0.0.1:8000/docs#/activate/{user_id}">Click here </a>
      </form>
    </div>
    <footer>
        <div id="container" style="white-space:nowrap">
            <br>
            <div id="texts" style="display:inline; white-space:nowrap;"> 
                The content of this email is intended for the person or entity to which it is addressed only.
            </div>
            <br>
            <div>
                If you are not the person to whom this message is addressed, you can just ignore it.
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
    msg["Subject"] = "User Confirmation Email"
    msg["From"] = email
    msg["To"] = to
    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(email, password)
    server.send_message(msg)
    server.quit()
# except Exception as exception:
#     print("Error: %s!\n\n" % exception)