############# ---- #############
from os import path
import random
from time import sleep
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import os
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import urllib3
from bs4 import BeautifulSoup
import posixpath
import urllib
import asyncio
############# ---- #############


def randomlist(listo, lenpm):

    random.shuffle(listo)

    if len(listo) > lenpm:
        listm = listo[:lenpm]
        listo = listm
    elif len(listo) < lenpm:
        listp = random.sample(listo[:lenpm - len(listo)], lenpm - len(listo))
        random.shuffle(listp)
        listo += (i for i in listp)

    return listo


class Maillepra:

    def __init__(self, email, password):
        self.email = str(email).strip()  # <---- write your email
        self.password = str(password).strip()  # <---- write password

    def preparationforsendemail(self):
        print(" - PREPARATION FOR SEND EMIAL ...")
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
        print(" - SENDING EMAIL ...")
        if self.preparationforsendemail():

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
                #     msbody)[str(msbody).find(">", str(msbody).find("<body")):])

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


############# ---- #############
# mail = Maillepra("example@gmail.com",  # your account
#                  "password")  # password

# - For Send Email :
# mail.preparationforsendemail()
# mail.sendemail()

#  - For Save Email :
# mail.getinbox(0)
# mail.saveemail()
############# ---- #############


class Instabot:
    def __init__(self, executable_path, hidebrowser=False):

        browser_options = Options()

        if hidebrowser:
            browser_options.add_argument('--headless')

        self.browser = webdriver.Firefox(
            executable_path=executable_path, options=browser_options)

        print(" - STARTING BOT ...")

    def getcbrowser(self):
        return self.browser

    def login(self, username, password):

        self.loginusername = username
        self.loginpassword = password

        self.instaloginurl = "https://www.instagram.com/accounts/login/"

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

        sleep(6)
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

        print(" - LIKING ...")

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

    def sendpost(self, userslist):

        print(" - SENDING ...")

        sendpost_button = self.browser.find_element_by_css_selector(
            "span._5e4p button.wpO6b[type=button]")
        sendpost_button.click()

        print(" - Searching and selecting user ...")
        sleep(6)

        for user in userslist:

            search_input = self.browser.find_element_by_css_selector(
                "input.j_2Hd.uMkC7.M5V28[name='queryBox']")
            search_input.send_keys(user + Keys.RETURN)

            sleep(4)

            usertg = self.browser.find_elements(
                By.CSS_SELECTOR, "div.Igw0E.rBNOH.eGOV_.ybXk5._4EzTm.XfCBB.HVWg4")
            usertg[0].click()

            print(f" - Select {user}")

        print(" - Send post for all users ...")

        send_button = self.browser.find_element_by_css_selector(
            "button.sqdOP.yWX7d.y3zKF.cB_4K[type=button]")
        send_button.click()

    def commentpost(self, commentlist, lenpm=6, countforrepeatcomment=1):

        print(" - COMMENTING ...")

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

            commentlist = randomlist(commentlist, lenpm)

            for commenttext in commentlist:

                comment_input = self.browser.find_element_by_css_selector(
                    "textarea[aria-label='Add a comment…']")

                sleep(4)

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

                print(f" # {comment_count} - {commenttext}")

                print(" - Posting comment ...")

                comment_count += 1

                # if comment_count % 5 == 0:
                #     print(" - Sleeping ( 20 ) seconds ...")
                #     sleep(10)

                # if comment_count % 15 == 0:
                #     print(" - Sleeping ( 40 ) seconds ...")
                #     sleep(40)

    def likeandcommentallposts(self, commentlist, boollike, countforrepeatcomment=1, countforrepeatallfn=1):

        print(" - COMMENTING AND LIKING FOR ALL POSTS HIS HAVE ...")
        #    , commentlist, countforrepeatecomment, boollike

        for i in range(countforrepeatallfn):

            print(" - Getting all posts | Loading ...")

            sleep(4)

            allposts = self.browser.find_elements(
                By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")

            for postdiv in allposts:

                # open post :
                print(" - Opening post")
                postdiv.click()

                sleep(4)

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


############# ---- #############
# for i in range(4):
# insta = Instabot("geckodriver.exe", True)

# insta.login("username",  # username
#             "password")  # password

# "https://www.instagram.com/p/CMCvkekgpTY/"
# insta.getpost("...url..")  # url post

# insta.sendpost(["s3q.x", "web_dev"])
# insta.likepost(True)  # set like for post (True) else (false)
# insta.commentpost(["🧡🧡.", "💛💛.", "❤️❤️.", "🖤🖤."],  # comment list

#                   3)  # count for repeat comment


# insta.getuserpage("s3q.x")

# insta.likeandcommentallposts(["🧡🧡.", "💛💛.", "❤️❤️.", "🖤🖤."], True)


# insta.getcbrowser().close()

############# ---- #############


class Fachtml:
    def __init__(self, url):
        req = urllib3.PoolManager()
        print(f" - Requesting ... To {url}")
        res = req.request(
            "GET", url)

        resdata = res.data
        self.respage = BeautifulSoup(resdata, features="html.parser")

        self.requrl = str(res.geturl())
        self.reqfilename = str(posixpath.basename(
            urllib.parse.urlparse(self.requrl).path)).strip()

        if self.reqfilename != "":
            self.requrl = self.requrl[:self.requrl.rfind('/')] + "/"

        self.newdir = str(urllib.parse.urlparse(self.requrl).netloc) + \
            str(posixpath.dirname(urllib.parse.urlparse(self.requrl).path))

        if not path.isdir(self.newdir):
            os.makedirs(self.newdir)

    def downloadfilebylink(self, data, path="", link=""):

        print(" - Save content in file ...")

        filename = str(posixpath.basename(
            self.getpathforpage(link))).strip()

        filedir = str(posixpath.dirname(self.getpathforpage(link))).strip()
        filedir = path + "/" + filedir
        print("File dir : " + filedir)

        if not os.path.isdir(filedir) and not filedir == "":
            os.makedirs(filedir)
        print(filename)
        if filename == "":
            filename = "index.html"
        elif filename.endswith(".php"):
            filename = filename.replace(".php", ".html")

        newfilename = filedir + "/" + filename

        print("Link : " + link)
        print("Filename : " + filename)
        print("New filename : " + newfilename, "\n")

        if not os.path.isfile(newfilename) and not newfilename == "":
            with open(newfilename, "w+", encoding='utf-8') as f:
                f.write(str(data))

    def getpagedata(self, url):

        req = urllib3.PoolManager()
        print(f" - Requesting ... To {url}")
        res = req.request(
            "GET", url)
        return BeautifulSoup(res.data)

    def getpathforpage(self, url):
        return urllib.parse.urlparse(url).path

    def download_htfile(self):

        for link in self.respage.findAll(attrs={"href": re.compile("")}):
            strlink = str(link.get("href"))
            if not strlink.startswith("https://") or not strlink.startswith("http://"):
                newlink = urllib.parse.urljoin(self.requrl, strlink)
                link['href'] = link['href'].replace(strlink, newlink)

        for link in self.respage.findAll(attrs={"src": re.compile("")}):
            strlink = str(link.get("src"))
            if not strlink.startswith("https://") or not strlink.startswith("http://"):
                newlink = urllib.parse.urljoin(self.requrl, strlink)
                link['src'] = link['src'].replace(strlink, newlink)

        self.downloadfilebylink(self.respage, self.newdir, self.reqfilename)

    def download_all_dependentfiles(self):

        for link in self.respage.findAll(attrs={"href": re.compile("")}):
            strlink = str(link.get("href")).strip()
            if not strlink.startswith("https://") and not strlink.startswith("http://"):
                newlink = urllib.parse.urljoin(self.requrl, strlink)
                link['href'] = link['href'].replace(strlink, newlink)

                resdata = self.getpagedata(newlink)

                self.downloadfilebylink(resdata, self.newdir, strlink)

        for link in self.respage.findAll(attrs={"src": re.compile("")}):
            strlink = str(link.get("src")).strip()
            if not strlink.startswith("https://") and not strlink.startswith("http://"):
                newlink = urllib.parse.urljoin(self.requrl, strlink)
                link['src'] = link['src'].replace(strlink, newlink)

                resdata = self.getpagedata(newlink)
                self.downloadfilebylink(resdata, self.newdir, strlink)

        self.downloadfilebylink(self.respage, self.newdir, self.reqfilename)

    def download_all_dependentfiles_wlink(self):

        for link in self.respage.findAll(attrs={"href": re.compile("")}):
            strlink = str(link.get("href")).strip()
            if not strlink.startswith("https://") and not strlink.startswith("http://"):
                newlink = urllib.parse.urljoin(self.requrl, strlink)

                resdata = self.getpagedata(newlink)
                self.downloadfilebylink(resdata, self.newdir, strlink)

        for link in self.respage.findAll(attrs={"src": re.compile("")}):
            strlink = str(link.get("src")).strip()
            if not strlink.startswith("https://") and not strlink.startswith("http://"):
                newlink = urllib.parse.urljoin(self.requrl, strlink)

                resdata = self.getpagedata(newlink)
                self.downloadfilebylink(resdata, self.newdir, strlink)

        self.downloadfilebylink(self.respage, self.newdir, self.reqfilename)


############# ---- #############
fhtml = Fachtml("http://google.com/")
# fhtml.download_htfile()
# fhtml.download_all_dependentfiles()
fhtml.download_all_dependentfiles_wlink()
############# ---- #############
