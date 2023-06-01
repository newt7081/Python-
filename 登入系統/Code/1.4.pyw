# 2023/05/28-登入系統1.4
import os, pickle
import tkinter as tk
from random import randint
from tkinter import ttk, messagebox
'''=====↓↓↓初始設定↓↓↓====='''
class USER_Sign_in():
    def Sign_in():
        '''登入'''
        global Sign_in_OK, NAME, PASSWORD, name, password, user_test, window_sign_up

        NAME = ver1.get()
        PASSWORD = ver2.get()
        if NAME=="" or PASSWORD=="":
            messagebox.showerror("錯誤","不能有選項空白。")
        else:
            # NAME加密
            a = []
            for i in range(len(NAME)):
                if TEXT.index(NAME[i]) + random_number > 94:
                    a.append(TEXT.index(NAME[i]) + random_number - 94)
                else:
                    a.append(TEXT.index(NAME[i]) + random_number)
            name = ""
            for i in a:
                name = name+TEXT_16[i]
            # PASSWORD加密
            a = []
            for i in range(len(PASSWORD)):
                if TEXT.index(PASSWORD[i]) + random_number > 94:
                    a.append(TEXT.index(PASSWORD[i]) + random_number - 94)
                else:
                    a.append(TEXT.index(PASSWORD[i]) + random_number)
            password = ""
            for i in a:
                password = password+TEXT_16[i]
            
            if name in usrs_info:
                if password == usrs_info[name]:
                    messagebox.showinfo("提示", "登入成功~")
                    window.destroy()
                    Sign_in_OK = 1
                else:
                    user_test = user_test + 1
                    if user_test >= 5:
                        messagebox.showerror("錯誤", "您已嘗試錯誤的密碼超過5次。")
                    else:
                        messagebox.showerror("錯誤", "密碼錯誤。")
            else:
                messagebox.showerror("錯誤", "沒有此帳號。")
    def Sign_up():
        '''註冊'''
        global window_sign_up, Sign_up_ver1, Sign_up_ver2, Sign_up_ver3
        def Sign_up_OK():
            new_name = Sign_up_ver1.get()
            new_password = Sign_up_ver2.get()
            new_password2 = Sign_up_ver3.get()
            if new_name=="" or new_password=="" or new_password2=="":
                messagebox.showerror("錯誤","不能有選項空白。")
            elif new_name in usrs_info:
                messagebox.showerror("錯誤","使用者名稱已存在。")
            elif new_password != new_password2:
                messagebox.showerror("錯誤","密碼前後不一致。")
            else:
                # 註冊資訊沒有問題則將使用者名稱密碼寫入資料庫(也可更改密碼)
                # NEW_name加密
                a = []
                for i in range(len(new_name)):
                    if TEXT.index(new_name[i]) + random_number > 94:
                        a.append(TEXT.index(new_name[i]) + random_number - 94)
                    else:
                        a.append(TEXT.index(new_name[i]) + random_number)
                new_name = ""
                for i in a:
                    new_name = new_name+TEXT_16[i]
                # NEW_password加密
                a = []
                for i in range(len(new_password)):
                    if TEXT.index(new_password[i]) + random_number > 94:
                        a.append(TEXT.index(new_password[i]) + random_number - 94)
                    else:
                        a.append(TEXT.index(new_password[i]) + random_number)
                new_password = ""
                for i in a:
                    new_password = new_password+TEXT_16[i]
                # 則將使用者名稱密碼寫入資料庫
                usrs_info[new_name]=new_password
                with open(filepath,'wb') as usr_file:
                    pickle.dump(usrs_info,usr_file)
                window_sign_up.destroy()
                messagebox.showinfo('歡迎','註冊成功。')
        try:    window_sign_up = tk.Toplevel(window)
        except: window_sign_up = tk.Tk()
        x = "260"
        y = "170"
        Width = str(int(window_sign_up.winfo_screenwidth()/2)-int(int(x)/2))
        Height = str(int(window_sign_up.winfo_screenheight()/2)-int(int(y)/2))
        xy = x+"x"+y+'+'+Width+"+"+Height
        window_sign_up.geometry(xy)
        window_sign_up.title("註冊")
        window_sign_up.iconbitmap('amz4f-z4l89-001.ico')
        canvas=tk.Canvas(window_sign_up,height=150,width=260)
        window_sign_up.resizable(width=False,height=False)
        imagefile=tk.PhotoImage(file='背景.png')
        canvas.create_image(0,0,anchor='nw',image=imagefile)
        canvas.pack(side='top')
        # # ---------- #
        Sign_up_ver1 = tk.StringVar()
        Sign_up_ver2 = tk.StringVar()
        Sign_up_ver3 = tk.StringVar()
        # # ---------- #
        # 標題
        txtid=canvas.create_text(110, 2, font=('Segoe UI Black', 15), anchor="nw")
        canvas.insert(txtid,1,"註冊")
        # 帳號
        txtid=canvas.create_text(45, 55, anchor="nw")
        canvas.insert(txtid,1,"帳號")
        ttk.Entry(window_sign_up, textvariable=Sign_up_ver1).place(x=71, y=53)
        # 密碼
        txtid=canvas.create_text(45, 75, anchor="nw")
        canvas.insert(txtid,1,"密碼")
        ttk.Entry(window_sign_up, textvariable=Sign_up_ver2).place(x=71, y=73)
        # 確認密碼
        txtid=canvas.create_text(21, 95, anchor="nw")
        canvas.insert(txtid,1,"確認密碼")
        ttk.Entry(window_sign_up, textvariable=Sign_up_ver3).place(x=71, y=93)
        # 按鈕
        ttk.Button(window_sign_up, text='Finish', command=window_sign_up.destroy).place(x=15, y=132)
        ttk.Button(window_sign_up, text='OK', command=Sign_up_OK).place(x=160, y=132)

        window_sign_up.mainloop()
    class main1():
        '''登入後的副程式'''
        def OK():
            messagebox.showinfo("提示", "目前暫無此功能")
        def Setup():
            '''帳號設定'''
            def Setup_OK():
                global PASSWORD
                new_name = Setup_ver1.get()
                new_password = Setup_ver2.get()
                if new_name=="" or new_password=="":
                    messagebox.showerror("錯誤","不能有選項空白。")
                else:
                    PASSWORD = new_password
                    # 註冊資訊沒有問題則將使用者名稱密碼寫入資料庫(也可更改密碼)
                    # NEW_name加密
                    a = []
                    for i in range(len(new_name)):
                        if TEXT.index(new_name[i]) + random_number > 94:
                            a.append(TEXT.index(new_name[i]) + random_number - 94)
                        else:
                            a.append(TEXT.index(new_name[i]) + random_number)
                    new_name = ""
                    for i in a:
                        new_name = new_name+TEXT_16[i]
                    # NEW_password加密
                    a = []
                    for i in range(len(new_password)):
                        if TEXT.index(new_password[i]) + random_number > 94:
                            a.append(TEXT.index(new_password[i]) + random_number - 94)
                        else:
                            a.append(TEXT.index(new_password[i]) + random_number)
                    new_password = ""
                    for i in a:
                        new_password = new_password+TEXT_16[i]
                    # 則將使用者名稱密碼寫入資料庫
                    usrs_info[new_name]=new_password
                    with open(filepath,'wb') as usr_file:
                        pickle.dump(usrs_info,usr_file)
                    window_sign_up.destroy()
                    messagebox.showinfo('提示','設定成功。') # 結束程式
            window_sign_up = tk.Toplevel(window)
            x = "260"
            y = "150"
            Width = str(int(window_sign_up.winfo_screenwidth()/2)-int(int(x)/2))
            Height = str(int(window_sign_up.winfo_screenheight()/2)-int(int(y)/2))
            xy = x+"x"+y+'+'+Width+"+"+Height
            window_sign_up.geometry(xy)
            window_sign_up.title("Setup")
            window_sign_up.iconbitmap('amz4f-z4l89-001.ico')
            canvas=tk.Canvas(window_sign_up,height=150,width=260)
            window_sign_up.resizable(width=False,height=False)
            imagefile=tk.PhotoImage(file='背景.png')
            canvas.create_image(0,0,anchor='nw',image=imagefile)
            canvas.pack(side='top')
            # ---------- #
            Setup_ver1 = tk.StringVar()
            Setup_ver2 = tk.StringVar()
            # ---------- #
            # 標題
            txtid=canvas.create_text(90, 2, font=('Segoe UI Black', 15), anchor="nw")
            canvas.insert(txtid,1,"帳號設定")
            # 帳號
            txtid=canvas.create_text(45, 55, anchor="nw")
            canvas.insert(txtid,1,"帳號")
            a = ttk.Entry(window_sign_up, textvariable=Setup_ver1)
            a.insert(0, NAME)
            a.config(state="disable")
            a.place(x=71, y=53)
            # 密碼
            txtid=canvas.create_text(45, 75, anchor="nw")
            canvas.insert(txtid,1,"密碼")
            a = ttk.Entry(window_sign_up, textvariable=Setup_ver2)
            a.insert(0, PASSWORD)
            a.place(x=71, y=73)
            # 按鈕
            ttk.Button(window_sign_up, text='Finish', command=window_sign_up.destroy).place(x=15, y=112)
            ttk.Button(window_sign_up, text='OK', command=Setup_OK).place(x=160, y=112)

            window_sign_up.mainloop()
TEXT = [" ", "!", "\"", "#", "$", "%",
        "&", "\'", "(", ")", "*",
        "+", ",", "-", ".", "/",
        "0", "1", "2", "3", "4", "5",
        "6", "7", "8", "9", ":",
        ";", "<", "=", ">", "?",
        "@", "A", "B", "C", "D", "E",
        "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O",
        "P", "Q", "R", "S", "T", "U",
        "V", "W", "X", "Y", "Z",
        "[", "\\", "]", "^", "_",
        "`", "a", "b", "c", "d", "e",
        "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o",
        "p", "q", "r", "s", "t", "u",
        "v", "w", "x", "y", "z",
        "{", "|", "}", "~"]
TEXT_16 = ["20", "21", "22", "23", "24", "25",
           "26", "27", "28", "29", "2A",
           "2B", "2C", "2D", "2E", "2F",
           "30", "31", "32", "33", "34", "35",
           "36", "37", "38", "39", "3A",
           "3B", "3C", "3D", "3E", "3F",
           "40", "41", "42", "43", "44", "45",
           "46", "47", "48", "49", "4A",
           "4B", "4C", "4D", "4E", "4F",
           "50", "51", "52", "53", "54", "55",
           "56", "57", "58", "59", "5A",
           "5B", "5C", "5D", "5E", "5F",
           "60", "61", "62", "63", "64", "65",
           "66", "67", "68", "69", "6A",
           "6B", "6C", "6D", "6E", "6F",
           "70", "71", "72", "73", "74", "75",
           "76", "77", "78", "79", "7A",
           "7B", "7C", "7D", "7E"]

user_test = 0
Sign_in_OK = 0
'''=====↑↑↑初始設定↑↑↑====='''
def Main0():
    '''登入頁面(主程式)'''
    global ver1, ver2, window
    
    window = tk.Tk()
    x = "260"
    y = "150"
    Width = str(int(window.winfo_screenwidth()/2)-int(int(x)/2))
    Height = str(int(window.winfo_screenheight()/2)-int(int(y)/2))
    xy = x+"x"+y+'+'+Width+"+"+Height
    window.geometry(xy)
    window.title("登入")
    window.iconbitmap('amz4f-z4l89-001.ico')
    canvas=tk.Canvas(window,height=150,width=260)
    window.resizable(width=False,height=False)
    imagefile=tk.PhotoImage(file='背景.png')
    canvas.create_image(0,0,anchor='nw',image=imagefile)
    canvas.pack(side='top')
    # ---------- #
    ver1 = tk.StringVar()
    ver2 = tk.StringVar()
    # ---------- #
    # 標題
    txtid=canvas.create_text(110, 2, font=('Segoe UI Black', 15), anchor="nw")
    canvas.insert(txtid,1,"登入")
    # 帳號
    txtid=canvas.create_text(45, 55, anchor="nw")
    canvas.insert(txtid,1,"帳號")
    ttk.Entry(window, textvariable=ver1).place(x=71, y=53)
    # 密碼
    txtid=canvas.create_text(45, 75, anchor="nw")
    canvas.insert(txtid,1,"密碼")
    ttk.Entry(window, show='●', textvariable=ver2).place(x=71, y=73)
    # 按鈕
    ttk.Button(window, text="Sign up", command=USER_Sign_in.Sign_up).place(x=15, y=112)
    ttk.Button(window, text="OK", command=USER_Sign_in.Sign_in).place(x=160, y=112)

    window.mainloop()

def Main1():
    '''帳號頁面(主程式)'''
    global ver1, ver2, window
    
    window = tk.Tk()
    x = "260"
    y = "150"
    Width = str(int(window.winfo_screenwidth()/2)-int(int(x)/2))
    Height = str(int(window.winfo_screenheight()/2)-int(int(y)/2))
    xy = x+"x"+y+'+'+Width+"+"+Height
    window.geometry(xy)
    window.title("帳號資訊")
    window.iconbitmap('amz4f-z4l89-001.ico')
    canvas=tk.Canvas(window,height=150,width=260)
    window.resizable(width=False,height=False)
    canvas.pack(side='top')
    # ---------- #
    ver1 = tk.StringVar()
    ver2 = tk.StringVar()
    # ---------- #
    # 帳號
    txtid=canvas.create_text(2, 2, anchor="nw")
    canvas.insert(txtid,1,"使用者名稱 :  "+NAME)
    # 按鈕
    ttk.Button(window, text="Sign up", command=USER_Sign_in.main1.Setup).place(x=15, y=112)
    ttk.Button(window, text="OK", command=USER_Sign_in.main1.OK).place(x=160, y=112)

    window.mainloop()

# ==========帳號資訊========== #
# 要檢查的檔案路徑
filepath = "Users_info"
# 載入本地已有的使用者資訊,如果沒有則已有使用者資訊為空
# 已有的使用者資訊
def user():
    global usrs_info, random_number
    messagebox.showinfo('提示','沒有帳號資訊，請註冊帳號。')
    USER_Sign_in.Sign_up()
try:
    with open(filepath,'rb') as usr_file:
        usrs_info = pickle.load(usr_file)
        random_number = int(usrs_info["5365747570"])
        # 測試用
        print(len(usrs_info), usrs_info)
        # 尚未有使用者資訊
        if int(len(usrs_info))==1:
            user()
# 尚未有使用者資訊
except FileNotFoundError:
    with open(filepath,'wb') as usr_file:
        usrs_info = {"5365747570":str(randint(1, 94))}
        pickle.dump(usrs_info,usr_file)
        random_number = int(usrs_info["5365747570"])
    user()

if int(len(usrs_info))!=1:
    Main0()
    if Sign_in_OK == 1:
        Main1()

'''ASCII'''
