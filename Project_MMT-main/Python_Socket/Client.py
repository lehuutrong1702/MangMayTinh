import socket
import json
import os
import subprocess
import tkinter
from tkinter import *
from tkinter import messagebox
from Func import *
from functools import partial
from PIL import Image
from tkinter import Menu
FORMAT = "utf8"
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

class Client:
    def __init__(self):
        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 65432        # The port used by the server
        # Create a TCP/IP socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        print('connecting to %s port ' + str(server_address))
        self.client.connect(server_address)

    def receive_msg(self):
        data = self.client.recv(1024).decode(FORMAT)
        print("Server: " + data)
        return data

    def send_msg(self, msg):
        self.client.send(bytes(msg, "utf8"))

    def send_file(self, filename):
        # get the file size
        filesize = os.path.getsize(filename)
        # send the filename and filesize
        self.client.send(f"{filename}{SEPARATOR}{filesize}".encode())
        # start sending the file
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in
                # busy networks
                self.client.sendall(bytes_read)


    def receive_file(self):
        # receive the file infos
        # receive using client socket, not server socket
        received = self.client.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        format = filename.split("_")
        _filename = "client_" + format[1]
        # convert to integer
        filesize = int(filesize)
        current_size = 0
        # start receiving the file from the socket
        # and writing to the file stream
        with open(_filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = self.client.recv(BUFFER_SIZE)
                current_size += len(bytes_read)
                # write the bytes to the file
                f.write(bytes_read)
                # check if the file transmission is done
                if current_size == filesize:
                    # if done, break
                    break
        return _filename

    def first_UI(self):
        print("\n1. Sign up\n2. Sign in\n3. Exit")
        option = input("Choose option: ")
        self.send_msg(option)
        if option == "1":
            self.sign_up()
            self.second_UI()
        elif option == '2':
            self.sign_in()
            self.second_UI()
        elif option == '3':
            print("Closing socket")

    def second_UI(self):
        print("\n1. View note\n2. Create note\n3. Exit")
        option = input("Choose option: ")
        self.send_msg(option)
        if option == "1":
            self.view_list_note()
        elif option == '2':
            self.create_note()
            #self.first_UI()
        elif option == '3':
            self.first_UI()

    def third_UI(self):
        print("\n1. View image\n2. Download image\n3. Exit\n")
        option = input("Choose option: ")
        self.send_msg(option)
        if option == "1":
            self.view_image()
            #self.second_UI()
        elif option == '2':
            self.download()
            #self.second_UI()
        elif option == '3':
            self.view_list_note()
            #self.second_UI()

    def fourth_UI(self):
        print("\n1. View note\n2. Download file\n2. Exit\n")
        option = input("Choose option: ")
        self.send_msg(option)
        if option == "1":
            self.view_note()
            #self.second_UI()
        elif option == '2':
            self.download()
            #self.second_UI()
        elif option == '3':
            self.second_UI()

    def sign_up(self,_name,_pass):
       # _name = input("User name: ")
       # _pass = input("Password: ")
        #send info
        self.send_msg(_name)
        x = self.receive_msg()
        self.send_msg(_pass)
        #receive msg from Server
        check = self.receive_msg()
        if check == "False":

            messagebox.showinfo("showinfo", "Account is exist or size is smaller than required size.")
           # self.first_UI()
        else:
            messagebox.showinfo("showinfo","Successfully registered.")
        return check

    def sign_in(self, _name, _pass):
     #   _name = input("User name: ")
      #  _pass = input("Password: ")
        #send info
       # print(_name)
      #  print(_pass)
        self.send_msg(_name)
        x = self.receive_msg()
        self.send_msg(_pass)
        #receive msg from Server
        check = self.receive_msg()
        if check == "False":
           messagebox.showinfo("showinfor", "Username or password is wrong.")
          #  self.first_UI()
        else:
            messagebox.showinfo("showinfor","Successfully logged in.")
        return check

    def view_list_note(self):
        viewlistnote= Tk()
        viewlistnote.title("View list note")
        viewlistnote.geometry("700x500")
        frame = tkinter.Frame(viewlistnote)
        try:
            data = self.client.recv(1024).decode(FORMAT)
            data = json.loads(data)
        except:
            messagebox.showinfo("showinfo", "chua co du lieu")
            return

        txt = tkinter.Text(frame)
        k = 1
        for i in data['Note']:
            txt.insert(tkinter.END, str(k),":")
            txt.insert(tkinter.END, i)
            txt.insert(tkinter.END, "\n")
            print(k,":", i)
            k += 1
        txt.grid()

        note = Label (frame, text ="Choose a note which you want to open:  ")
        note.grid()
        entryx = Entry(frame, width=20,bd=5)
        entryx.grid()
        frame.grid_rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.pack(side="top", fill="both", expand=True)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid()


        thirdframe = tkinter.Frame(viewlistnote)
        thirdframe.grid_rowconfigure(0, weight=1)
        thirdframe.columnconfigure(0, weight=1)
        thirdframe.grid(row=0, column=0, sticky="nsew")
        third_label = Label(thirdframe, text="THIRD UI", font=("ROBOTO", 16), bd=5)
        third_label.grid()

        def return2_click():
            option = "3"
            self.send_msg(option)
            viewlistnote.destroy()

        #  self.send_msg(option)
        def viewimage_click():
            option = "1"
            self.send_msg(option)
            self.view_image()
          #  frame.tkraise()

        def download_click():
            # self.second_UI()
            option = "2"
            self.send_msg(option)
            self.download()
        #    frame.tkraise()
            # self.second_UI()

        viewimage_button = Button(thirdframe, width=20, height=2, text="View Image", bd=5, command=viewimage_click)
        viewimage_button.grid()
        downloadimage_button = Button(thirdframe, width=20, height=2, text="Download Image", bd=5, command=download_click)
        downloadimage_button.grid()
        return2_button = Button(thirdframe, width=20, height=2, text="Back", bd=5, command=return2_click)
        return2_button.grid()

        fourthframe = tkinter.Frame(viewlistnote)
        fourthframe.grid_rowconfigure(0, weight=1)
        fourthframe.columnconfigure(0, weight=1)
        fourthframe.grid(row=0, column=0, sticky="nsew")
        fourth_label = Label(fourthframe, text="FOURTH UI", font=("ROBOTO", 16), bd=5)
        fourth_label.grid()

        def viewinote_click():
            option = "1"
            self.send_msg(option)
            self.view_note()
           # frame.tkraise()

        def downloadnote_click():
            # self.second_UI()
            option = "2"
            self.send_msg(option)
            self.download()
      #      frame.tkraise()

        def return3_click():
            option = "3"
            self.send_msg(option)
            viewlistnote.destroy()
        #    frame.tkraise()
        #  self.send_msg(option)
        viewnote_button = Button(fourthframe, width=20, height=2, text="View Note", bd=5, command=viewinote_click)
        viewnote_button.grid()
        downloadfile_button = Button(fourthframe, width=20, height=2, text="Download file", bd=5, command=downloadnote_click)
        downloadfile_button.grid()
        return3_button = Button(fourthframe, width=20, height=2, text="Back", bd=5, command=return3_click)
        return3_button.grid()
        frame.tkraise()

        def click():
            option = entryx.get()
            self.send_msg(option)
            format = self.receive_msg()
            if format == "png" or format == "jpg":
                thirdframe.tkraise()
            else:
                fourthframe.tkraise()

        b = Button(frame, text="Enter", bd=5, command=click)
        b.grid()





    def create_note(self):
        createnote = Tk()
        createnote.title("Create Note")
        inputid_label = Label(createnote,text=" Input ID:")
        inputid_label.grid()
        inputid_entry = Entry(createnote, width=20, bd=5)
        inputid_entry.grid()
        inputtype_label = Label(createnote, text=" Input type:")
        inputtype_label.grid()
        inputtype_entry = Entry(createnote, width=20, bd=5)
        inputtype_entry.grid()
        inputfile_label = Label(createnote, text=" Input file name :")
        inputfile_label.grid()
        inputfile_entry = Entry(createnote, width=20, bd=5)
        inputfile_entry.grid()

        def button_click():
            id = inputid_entry.get()
            type = inputtype_entry.get()
            file=inputfile_entry.get()
            self.send_msg(id)
            print(id)
            self.receive_msg()
            self.send_msg(type)
            self.receive_msg()
            print(type)
            self.send_msg(file)
            print(file)
            check = self.receive_msg()
            if check == "False":
                messagebox.showinfo("showinfo","ID has been used or wrong input.")
               # self.create_note()
            # send file
            else:
                messagebox.showinfo("showinfo", "Success!")

            try:
                self.send_file(file)
                print("send success")
            except:
                print("send fail")
                messagebox.showinfo("showinfo", "File {} not found".format(file))
                return
        enter_button = Button(createnote, height=2,width=20,text="Enter",bd=5,command=button_click)
        enter_button.grid()

        #createnote.mainloop()
    def view_note(self):
        _filename =self.receive_file()

        cmd = _filename
        subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)

        cmd = "del/Q " + _filename
        subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)

    def view_image(self):
        _filename =self.receive_file()

        img = Image.open(_filename)
        # Output Images
        img.show()

        cmd = "del/Q " + _filename
        subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)

    def download(self):
        _filename = self.receive_file()
        print("File {} has been downloaded ".format( _filename))



    def main(self):
  #      self.first_UI()
        window = Tk()
        window.geometry("500x200")
        window.title("Client")
        menubar= Menu(window)
        window.config(menu=menubar)
        file_menu= Menu(menubar)
        file_menu.add_command(
        label='Exit',
        command=window.destroy)
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        ##### FIRST UI ####

        firstframe = tkinter.Frame(window)
        secondframe = tkinter.Frame(window)
        login_label = Label (firstframe, text = "LOGIN PAGE", font=("ROBOTO",16))
        login_label.grid(row=0, column=2,)
        label_username = Label(firstframe, text="User name: ")
        box_username = Entry(firstframe,width=20,bg="pink",bd=5)
        label_username.grid(column = 2, row  = 1 )
        box_username.grid(column = 3 , row = 1 )
        label_password = Label(firstframe, text ="Password")
        label_password.grid(column = 2, row = 2 )
        box_password = Entry(firstframe, width=20, bg="pink",bd=5)
        box_password.grid(column = 3, row = 2)



        def login_click():
            option = "2"
            self.send_msg(option)
            _username = box_username.get()
            print(_username)
            _pass = box_password.get()
            print(_pass)
            check = self.sign_in(_username, _pass)
            if check == "True":
                secondframe.tkraise()

        def register_click():
            option = "1"
            self.send_msg(option)
            _username = box_username.get()
            print(_username)
            _pass = box_password.get()
            print(_pass)
            check = self.sign_up(_username, _pass)
            if check == "True":
                secondframe.tkraise()

        firstframe.pack(side="top", fill="both", expand=True)
        firstframe.grid_rowconfigure(0, weight=1)
        firstframe.columnconfigure(0, weight=1)
        firstframe.grid(row=0,column=0,sticky="nsew")

    #    secondframe.pack(side="top", fill="both", expand=True)
        secondframe.grid_rowconfigure(0, weight=1)
        secondframe.columnconfigure(0, weight=1)
        secondframe.grid(row=0, column=0, sticky="nsew")
        firstframe.tkraise()
        login_button = Button(firstframe, width=20, height=2, text="Login", command=login_click)
        login_button.grid(column = 3)
        register_button = Button(firstframe, width=20, height=2, text="Register", bg="yellow", command=register_click)
        register_button.grid(column = 3)

    ##Second UI
        def return_click():
            option = "3"
            firstframe.tkraise()
            self.send_msg(option)
        def viewnote_click():
            option="1"
            self.send_msg(option)
            self.view_list_note()
        def createnote_click():
            option="2"
            self.send_msg(option)
            self.create_note()
        #   secondframe.tkraise()
        second_label = Label(secondframe, text="SECOND UI", font=("ROBOTO", 16),bd=5)
        second_label.grid()
        viewnote_button = Button(secondframe,width=20,height=2,text="View Note",bd=5,command=viewnote_click)
        viewnote_button.grid()
        createnote_button = Button(secondframe, width=20, height=2, text="Create Note",bd=5,command=createnote_click)
        createnote_button.grid()
        return_button = Button(secondframe, width=20, height=2, text="Back",bd=5,command=return_click)
        return_button.grid()
  ### Third UI

    ## FOURth UI

        firstframe.tkraise()
        window.mainloop()
   #     self.client.close()

C = Client()


C.main()