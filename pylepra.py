import random
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import os
import json

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Maillepra:

    def __init__(self, email, password):
        self.email = str(email).strip()  # <---- write your email
        self.password = str(password).strip()  # <---- write password

    def preparationforsendemail(self):

        # <--- receiver email : salimalsulaimi204@gmail.com
        self.receiver_email = input(
            "@ - Type receiver email and press enter : ")
        # <---- messsage subject
        self.subject = input(
            "@ - Type message subject and press enter : ").strip()
        # <---- message content (Html)
        self.content = input(
            "@ - Type message content and press enter : \n").strip()

        # check for emails and password :
        if not re.match("[^@]+@[^@]+\.[^@]+", self.receiver_email) and not re.match("[^@]+@[^@]+\.[^@]+", self.email) and self.password != "":
            print(" - Invalid email .!")
            return False
        else:
            return True

    def sendemail(self):
        #
        if self.preparationforsendemail():
            try:
                # manages a connection to an SMTP or ESMTP server
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    # Puts the connection to the SMTP server into TLS mode :
                    server.starttls()

                    #
                    if not server.login(self.email, self.password):
                        print(" - Failed to login .!")
                    else:

                        message = MIMEMultipart("alternative")
                        message["From"] = self.email
                        message["To"] = self.receiver_email
                        message["Subject"] = self.subject

                        # <---- Class for generating text/* type MIME documents
                        htmlPart = MIMEText(self.content, 'html')

                        # <---- Add the given payload to the current payload
                        message.attach(htmlPart)

                        print(" - Loading ...")

                        #
                        if server.sendmail(self.email, self.receiver_email, message.as_string()):
                            print(" - The email has been sent successfully .")

                    # Terminate the SMTP session :
                    server.quit()
            except:
                print(" - Something is wrong .!")

    def getinbox(self, emailindex):

        print(" - GET EMIAL ...")

        imap = imaplib.IMAP4_SSL("imap.gmail.com")

        imap.login(self.email, self.password)

        # select inbox
        print(" - Select inbox ...")
        statustext, messagesb = imap.select("INBOX")

        # number of top emails to fetch
        # numberemailfetch = 1
        # numberemailfetch = int(input("@ - Type email index : ").strip())
        numberemailfetch = int(emailindex)

        # total number of emails
        messagescount = int(messagesb[0])

        numberemailfetch = messagescount - numberemailfetch

        print(" - Index for email : " + str(numberemailfetch))

        emaildatadict = {}

        response, message = imap.fetch(str(numberemailfetch), '(RFC822)')

        mscontent = message[0][1]

        emailmessage = email.message_from_bytes(mscontent)

        print("\n\n\n")

        headerdict = dict(emailmessage)
        headerdict["subject"] = emailmessage["subject"]

        print(" - Header data : \n\n" + str(headerdict))

        emaildatadict["header"] = headerdict

        for mspart in emailmessage.walk():

            if mspart.get_default_type() == "text/plain" or mspart.get_content_type() == "text/html":

                msbody = mspart.get_payload(decode=True)

                # msbody = (str(msbody)[:str(msbody).find(">", str(msbody).find("<body"))] + "><pre>" + str(headerdict) + "</pre>" + str(
                #     msbody)[str(msbody).find(">", str(msbody).find("<body")):]).encode('utf8')

                print("\n\n\n")

                msbody = msbody.decode()

                emaildatadict["body"] = msbody

                print(" - Body data : \n\n" + str(msbody))

        self.getinboxemaildata = emaildatadict

        return emaildatadict

    def saveemail(self):

        print(" - SAVE EMAIL ...")

        foldername = self.getinboxemaildata["header"]["subject"]

        print(" - Folder name to save email is : " + foldername)

        if not os.path.isdir(foldername):
            os.mkdir(foldername)

        with open(foldername+"/"+"index.html", "w+") as f:
            f.write(self.getinboxemaildata["body"])
            print(" - Write body in index.html file . done")
            f.close()

        with open(foldername+"/"+"header.json", "w+") as f:
            f.write(json.dumps(self.getinboxemaildata["header"]))
            print(" - Write header data in hedaer.json file . done")
            f.close()


mail = Maillepra("example@gmail.com",  # your account
                 "password")  # password

# - For Send Email :
# mail.preparationforsendemail()
# mail.sendemail()

#  - For Save Email :
mail.getinbox(0)
mail.saveemail()


class instabot:
    def __init__(self, executable_path, hidebrowser=False):

        browser_options = Options()

        if hidebrowser:
            browser_options.add_argument('--headless')

        self.browser = webdriver.Firefox(
            executable_path=executable_path, options=browser_options)

    # def signup(self, email, epassword, fullname, username, password):

    #     mail = Maillepra(email, epassword)

    #     self.signupemailornumphone = email
    #     self.signupfullname = fullname
    #     self.signupusername = username
    #     self.signuppassword = password

    #     self.instasignupurl = "https://www.instagram.com/accounts/emailsignup/"

    #     print(" - Start Bot ...")

    #     print(" - Getting login page | Loading ...")

    #     try:
    #         self.browser.get(self.instasignupurl)

    #         print(" - The post has been fetched successfully")
    #     except:
    #         print(" - The post was not successfully fetched")

    #     sleep(2)

    #     emailornumphone_input = self.browser.find_element_by_css_selector(
    #         "input[name='emailOrPhone']")
    #     fullname_input = self.browser.find_element_by_css_selector(
    #         "input[name='fullName']")
    #     username_input = self.browser.find_element_by_css_selector(
    #         "input[name='username']")
    #     password_input = self.browser.find_element_by_css_selector(
    #         "input[name='password']")
    #     submit_button = self.browser.find_element_by_xpath(
    #         "//button[@type='submit']")

    #     emailornumphone_input.send_keys(email)
    #     fullname_input.send_keys(fullname)
    #     username_input.send_keys(username)
    #     password_input.send_keys(password)
    #     submit_button.click()

    #     sleep(6)

    #     months_input = self.browser.find_element_by_css_selector(
    #         "select[title='Month:']")
    #     month_input = self.browser.find_element_by_css_selector(
    #         "select[title='Month:'] option[value='8']")
    #     days_input = self.browser.find_element_by_css_selector(
    #         "select[title='Day:']")
    #     day_input = self.browser.find_element_by_css_selector(
    #         "select[title='Day:'] option[value='5']")
    #     years_input = self.browser.find_element_by_css_selector(
    #         "select[title='Year:']")
    #     year_input = self.browser.find_element_by_css_selector(
    #         "select[title='Year:'] option[value='2000']")

    #     months_input.click()
    #     month_input.click()
    #     days_input.click()
    #     day_input.click()
    #     years_input.click()
    #     year_input.click()

    #     sleep(0.5)

    #     next_button = self.browser.find_element_by_css_selector(
    #         "button.sqdOP.L3NKy._4pI4F.y3zKF[type='button']")
    #     next_button.click()

    #     print(" - Wite email confirmation code ...")

    #     sleep(20)

    #     confirmationcode_input = self.browser.find_element_by_css_selector(
    #         "input[name='email_confirmation_code']")
    #     submit_button_2 = self.browser.find_element_by_xpath(
    #         "//button[@type='submit']")

    #     print(" - Get confirmation code ...")

    #     sleep(6)

    #     confirmationcode_input.send_keys(mail.getinbox(
    #         0)["header"]["subject"][:6])
    #     submit_button_2.click()

    #     print(" - You have sign up successfully")

    #     sleep(15)

    # def connecttomysql(self, user, password, host):

    #     configsqlconnect = {
    #         "user": user,
    #         "password": password,
    #         "host": host
    #     }

    #     self.sqlconnect = mysql.connector.connect(**configsqlconnect)
    #     self.sqlcursor = self.sqlconnect.cursor()

    #     return self.sqlconnect

    # def savesignupinsqldb(self):

    #     print(" - Create insta database if not exists")

    #     self.sqlcursor.execute("CREATE DATABASE IF NOT EXISTS insta")

    #     print(" - Select insta database")
    #     self.sqlconnect.database = "insta"

    #     print(" - Create userssignup tablse in insta database if not exists")
    #     self.sqlcursor.execute("CREATE TABLE IF NOT EXISTS `insta`.`userssignup` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `email-or-phone` CHAR(255) NOT NULL , `fullname` CHAR(255) NOT NULL , `username` CHAR(255) NOT NULL , `password` CHAR(255) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB CHARSET=utf8 COLLATE utf8_general_ci;")

    #     print(" - Make id and username columns * UNIQUE")
    #     self.sqlcursor.execute("ALTER TABLE `userssignup` ADD UNIQUE(`id`);")
    #     self.sqlcursor.execute(
    #         "ALTER TABLE `userssignup` ADD UNIQUE(`username`);")

    #     print(" - Insert data ...")
    #     self.sqlcursor.execute(
    #         f"""INSERT INTO `userssignup` (`id`, `email-or-phone`, `fullname`, `username`, `password`) VALUES ('', '{self.signupemailornumphone}', '{self.signupfullname}', '{self.signupusername}', '{self.signuppassword}');""")

    #     print(" - Fetchall all rows")
    #     self.sqlcursor.execute("SELECT * FROM `userssignup`")
    #     result = self.sqlcursor.fetchall()
    #     print(" - Result : ", result, "\n\n")

    #     print(" - Commiting ..")
    #     self.sqlconnect.commit()

    #     return result

    # def getuserssignupinsqldb(self):

    #     print(" - Fetchall all rows")
    #     self.sqlcursor.execute("SELECT * FROM `userssignup`")
    #     result = self.sqlcursor.fetchall()
    #     print(" - Result : ", result, "\n\n")

    #     print(" - Commiting ..")
    #     self.sqlconnect.commit()

    #     return result

    def login(self, username, password):

        self.loginusername = username
        self.loginpassword = password

        self.instaloginurl = "https://www.instagram.com/accounts/login/"

        print(" - Start Bot ...")

        print(" - Getting login page | Loading ...")

        self.browser.get(self.instaloginurl)

        sleep(2)

        username_input = self.browser.find_element_by_css_selector(
            "input[name='username']")
        password_input = self.browser.find_element_by_css_selector(
            "input[name='password']")
        submit_button = self.browser.find_element_by_xpath(
            "//button[@type='submit']")

        username_input.send_keys(username)
        password_input.send_keys(password)
        submit_button.click()

        print(" - You have logged in successfully")

        sleep(15)
        # self.browser.get("https://www.instagram.com/accounts/onetap/")

    def getuserpage(self, user):

        print(" - Getting user page | loading ...")

        self.targetusername = user

        self.userpageurl = "https://www.instagram.com/{}/".format(user)

        try:
            self.browser.get(self.userpageurl)

            print(" - The user page has been fetched successfully")

        except:

            print(" - The user page was not successfully fetched")

    def getpost(self, posturl):

        print(" - Getting post | loading ...")

        try:
            self.browser.get(posturl)

            print(" - The post has been fetched successfully")
        except:
            print(" - The post was not successfully fetched")

    def getpostowner(self):

        try:
            post_owner = self.browser.find_element_by_css_selector(
                ".sqdOP.yWX7d._8A5w5.ZIAjV").text
            return f" - This is posted under the username {post_owner}"
        except:
            return " - Can't find username .!"

    def getlikepostbool(self):

        sleep(2)

        likestatus = None

        # "span.fr66n button.wpO6b[type='button'] .QBdPU .FY9nT svg"

        # "span.fr66n button.wpO6b[type='button']"
        try:
            likertext = self.browser.find_element_by_css_selector(
                "span.fr66n button.wpO6b[type='button'] .QBdPU span svg").get_attribute("aria-label").lower()

            if likertext == "like":
                likestatus = False
            elif likertext == "unlike":
                likestatus = True
            return likestatus

        except:
            return "stop"

    def likepost(self, boollike):

        print(" - Liking ...")

        like_button = self.browser.find_element_by_css_selector(
            "span.fr66n button.wpO6b[type='button']")

        if self.getlikepostbool() == True:

            if not boollike:
                like_button.click()
                print(" - Removing like sign")
        else:
            if boollike:
                like_button.click()
                print(" - Adding like sign")

    def commentpost(self, commentlist, countforrepeatcomment=1):

        print(" - Commenting ...")

        comment_count = 0

        post_owner = self.getpostowner()

        print(f" - This is posted under the username {post_owner}")

        if self.getlikepostbool() == True:
            liketext = "like"
        else:
            liketext = "unlike"

        print(f" - You put a {liketext} sign in this post")

        print(" - Start making comments ...")

        for i in range(countforrepeatcomment):

            random.shuffle(commentlist)

            for commenttext in commentlist:

                comment_input = self.browser.find_element_by_css_selector(
                    "textarea[aria-label='Add a comment…']")

                sleep(8)

                self.browser.execute_script(
                    """document.querySelector("textarea[aria-label='Add a comment…']").value = ''""")

                # click on textarea/comment box and enter comment
                (
                    ActionChains(self.browser)
                    .move_to_element(comment_input)
                    .click()
                    .send_keys(commenttext + Keys.RETURN)
                    .perform()

                )

                print(f"#{comment_count} - {commenttext}")

                print(" - Posting comment ...")

                comment_count += 1

                if comment_count % 5 == 0:
                    print(" - Sleeping ( 20 ) seconds ...")
                    sleep(20)

                if comment_count % 15 == 0:
                    print(" - Sleeping ( 40 ) seconds ...")
                    sleep(40)

    def likeandcommentallposts(self, commentlist, boollike, countforrepeatcomment=1, countforrepeatallfn=1):
        #    , commentlist, countforrepeatecomment, boollike

        for i in countforrepeatallfn:

            print(" - Getting all posts | Loading ...")

            sleep(8)

            allposts = self.browser.find_elements(
                By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")

            for postdiv in allposts:

                # open post :
                print(" - Opening post")
                postdiv.click()

                sleep(8)

                # set like sign :
                self.likepost(boollike)

                # loop cooment :
                self.commentpost(commentlist, countforrepeatcomment)

                sleep(2)

                # close post :
                print(" - Closing post")
                # close_div = self.browser.find_element_by_css_selector(
                #     "div._2dDPU.CkGkG[role='dialog']")

                close_button = self.browser.find_element_by_css_selector(
                    ".Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG button.wpO6b[type='button']")

                # ".Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG button.wpO6b[type='button']"
                close_button.click()

                sleep(2)

                allposts = self.browser.find_elements(
                    By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")

                print(" - Sleeping ( 20 ) seconds ...")
                sleep(20)


insta = instabot("geckodriver.exe", True)

insta.login("username",  # username
            "password")  # password


# insta.getpost("")  # url post

# insta.likepost(True)  # set like for post (True) else (false)

insta.getuserpage("s3q.x")

insta.likeandcommentallposts(["🧡🧡.", "💛💛.", "❤️❤️.", "🖤🖤.", "👌👌.",
                              "💜💜.", "💙💙.", "💚💚.", "💯🔥.", "😍😍."], True)

# insta.commentpost(["🧡🔥🔥.", "💛🔥🔥.", "❤️🔥🔥.", "🖤🔥🔥.", "👌😍😍.",
#                    "💜🔥🔥.", "💙🔥🔥.", "💚🔥🔥.", "💯🔥🔥.", "😍🔥🔥."],  # comment list

#                   3)  # count for repeat comment
