import tkinter as tk
from tkinter import ttk
from tkinter import INSERT, filedialog
from PIL import ImageTk,Image
import binascii as t
from tkinter import messagebox

def decode(hexcode):
    if hexcode[-1] in ('0','1'):
        return hexcode[-1]
    else:
        return None

def rgb2hex(r,g,b):
    return '#{:0x}{:0x}{:0x}'.format(r,g,b)

def bin2str(binary):
    message=t.unhexlify('%x' % (int('0b' + binary,2)))
    message=str(message)
    message=message[2:-1]

    return message

def hex2rgba(hexcode):
    hexcode = hexcode.lstrip('#')
    lv = len(hexcode)
    return tuple(int(hexcode[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def str2bin(message):
    binary=str(''.join(format(ord(i), '08b') for i in message))
    return binary

class Page1(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,height=600,width=450)
        self.parent = parent

        label = tk.Label(self, text="IMAGE STEGANOGRAPHY",font="arial 25 bold")
        label.place(x=20,y=70)

        Button_encode = tk.Button(self,text="Encode Image",height=4,width=15,command=lambda:controller.show_frame(Encode))
        Button_encode.place(x=165,y=200)

        Button_decode = tk.Button(self,text="Decode Image",height=4,width=15,command=lambda:controller.show_frame(Decode))
        Button_decode.place(x=165,y=300)

class EncodeNext(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,height=600,width=450)

        global encodedimg

        encodedimgLocal=encodedimg.resize((400,350),Image.ANTIALIAS)
        
        imga = ImageTk.PhotoImage(encodedimgLocal)

        encode_label = tk.Label(self,text="ENCODED IMAGE",font="arial 20 bold italic")
        encode_label.place(x=120,y=20)

        download_button = tk.Button(self,text="Download",command=self.download)
        download_button.place(x=200,y=500)

        label=tk.Label(self,image=imga,borderwidth=3,relief="solid")
        label.image=imga
        label.place(x=23,y=100)

        back=tk.Button(self,text="Back",height=2,width=8,command=lambda:controller.show_frame(Encode))
        back.place(x=10,y=5)
    
    def download(self):
        cpyselect_file=filedialog.asksaveasfile(initialfile="Untitled.png",title="Select",filetypes=[('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg')],defaultextension="jpg")

        try:
            encodedimg.save(cpyselect_file.name,"PNG")
            messagebox.showinfo(title="DOWNLOADED",message="Encoded image sucessfully doenloaded")
            controller.show_frame(Page1)
        except:
            messagebox.showerror(title="ERROR",message="File not selected")

class Encode(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,height=600,width=450)

        decode_label = tk.Label(self,text="ENCODE PAGE",font="arial 20 bold italic")
        decode_label.place(x=150,y=20)

        label = tk.Label(self,text="Select image to encode")
        label.place(x=100,y=65)

        select_button = ttk.Button(self,text="SELECT",command=lambda:self.openPanel())
        select_button.place(x=275,y=65)

        self.encode_button = tk.Button(self,text="Encode",state="disable")
        self.encode_button.place(x=200,y=550)

        back=tk.Button(self,text="Back",height=2,width=8,command=lambda:controller.show_frame(Page1))
        back.place(x=10,y=5)

    def openPanel(self):
        global file
        
        self.file=filedialog.askopenfilename(initialdir="This PC",title="Select",filetypes=[('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg')])

        file=self.file

        if (self.file):
            self.encode_button["state"]="normal"

            img=Image.open(self.file)

            self.imgcpy=img.copy()
            imgcpyLocal=self.imgcpy.resize((200,250),Image.ANTIALIAS)
            imga = ImageTk.PhotoImage(imgcpyLocal)
        
            label=tk.Label(self,image=imga,borderwidth=3,relief="solid")
            label.image=imga
            label.place(x=130,y=100)

            textbox=tk.Text(self,height=10,width=45)
            textbox.place(x=50,y=370)

            self.encode_button["command"]=lambda:self.update(textbox)
        else:
            messagebox.showwarning("ERROR",message="File not selected")
        
    def update(self,text):
        global textmess
        textmess=text.get("1.0", "end-1c")
        self.hide(textmess)

    def hide(self,message):
        binary=str2bin(message)+'1111111111111110'
        if self.imgcpy.mode in ('RGBA'):
            self.imgcpy=self.imgcpy.convert('RGBA')
            datas=self.imgcpy.getdata()
            newData=[]
            digit=0
            for item in datas:
                if digit<len(binary):
                    newpix=self.encode(rgb2hex(item[0],item[1],item[2]),binary[digit])
                    if newpix==None:
                        newData.append(item)
                    else:
                        (r,g,b)= hex2rgba(newpix)
                        newData.append((r,g,b,255))
                        digit+=1
                else:
                    newData.append(item)
            # self.imgcpy.putdata(newData)
            self.imgcpy.putdata(newData)

            # self.imgcpy.save("hehehhe.png","PNG")

            global encodedimg
            encodedimg=self.imgcpy

            messagebox.showinfo(title="Sucess",message="SUCESSFULLY COMPLETED")
            controller.show_frame(EncodeNext)
            
            return "completed"
        return "Incorrect Image Mode, couldn't hide :("
    def encode(self,hexcode,digit):
        if hexcode[-1] in ('0','1','2','3','4','5'):
            hexcode=hexcode[:-1]+digit
            return hexcode
        else:
            return None

class Decode(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,height=600,width=450)

        decode_label = tk.Label(self,text="DECODE PAGE",font="arial 20 bold italic")
        decode_label.place(x=150,y=20)

        back=tk.Button(self,text="Back",height=2,width=8,command=lambda:controller.show_frame(Page1))
        back.place(x=10,y=5)

        select_label = tk.Label(self,text="Select image to decode : ",font="arial 10")
        select_label.place(x=100,y=65)

        select_button = ttk.Button(self,text="SELECT",command=self.select)
        select_button.place(x=270,y=65)

        self.decode_button = tk.Button(self,text="Decode",state="disable",command=self.retr)
        self.decode_button.place(x=300,y=550)

        home_button = tk.Button(self,text="Go to Home",command=lambda:controller.show_frame(Page1))
        home_button.place(x=100,y=550)

    def retr(self):
        filename=self.select_file
        img=Image.open(filename)
        binary=''

        if img.mode in ('RGBA'):
            img=img.convert('RGBA')
            datas=img.getdata()
            
            for item in datas:
                digit=decode(rgb2hex(item[0],item[1],item[2]))
                if digit==None:
                    pass
                else:
                    binary+=digit
                    if (binary[-16:]=='1111111111111110'):
                        self.textbox.delete("1.0","end")
                        self.textbox.insert(INSERT,bin2str(binary[:-16]))
                        return bin2str(binary[:-16])
            self.textbox.delete("1.0","end")
            self.textbox.insert(INSERT,bin2str(binary))
            return bin2str(binary)
        self.textbox.delete("1.0","end")
        self.textbox.insert(INSERT,"Incorrect Image Mode, couldn't retrieve :(")
        return "Incorrect Image Mode, couldn't retrieve :("

    def select(self):
        try:
            self.select_file=filedialog.askopenfilename(initialdir="This PC",title="Select",filetypes=[('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg')])
            img=Image.open(self.select_file,'r')
            img=img.resize((200,250),Image.ANTIALIAS)
            imga = ImageTk.PhotoImage(img)
        
            label=tk.Label(self,image=imga,borderwidth=3,relief="solid")
            label.image=imga
            label.place(x=130,y=100)
            self.textbox=tk.Text(self,height=10,width=45)
            self.textbox.place(x=50,y=370)
            self.decode_button["state"]="normal"

        except:
            messagebox.showwarning("ERROR",message="File not selected")


class PageController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.geometry(self.size())
        self.resizable(0,0)
        self.title("Image Steganography")
        self.iconbitmap("icon.ico")

        self.window=tk.Frame(self)
        self.window.pack()

        self.window.rowconfigure(0,minsize=600)
        self.window.columnconfigure(0,minsize=450)

        self.frames={}

        self.show_frame(Page1)

    def show_frame(self,PAGE):
        if (PAGE in self.frames):
            frame=self.frames[PAGE]
            frame.destroy()
        
        self.frames[PAGE]=PAGE(self.window,self)
        frame=self.frames[PAGE]
        frame.grid(row=0,column=0)
        frame.tkraise()

    def size(self):
        x = self.winfo_screenwidth()
        y = self.winfo_screenheight()

        xx = int(x / 2 - 450 / 2)
        yy = int(y / 2 - 600 / 2)
        xx = str(xx)
        yy = str(yy - 10)
        m = "450x600+" + xx + "+" + yy
        return m

file=""
textmess=""
encodedimg=""
cpyselect_file=""
controller=PageController()
controller.mainloop()