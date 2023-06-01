import pickle
import tkinter as tk
from tkinter import ttk, messagebox
# 主程式-------------------------------------------------------->
def Main():
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
    ttk.Button(window, text="Sign up", command=Sign_up).place(x=13, y=112)
    ttk.Button(window, text="OK", command=Sign_in).place(x=160, y=112)

    window.mainloop()
def Sign_in():
    '''登入'''
    global Sign_in_OK

    name = ver1.get()
    password = ver2.get()
    Sign_in_OK = 0
    if name=="" or password=="":
        messagebox.showerror("錯誤","不能有選項空白。")
    else:
        if name in usrs_info:
            if password == usrs_info[name]:
                messagebox.showinfo("提示", "登入成功~")
                window.destroy()
                Sign_in_OK = 1
            else:
                messagebox.showerror("錯誤", "密碼錯誤。")
        else:
            messagebox.showerror("錯誤", "沒有此帳號。")
def Sign_up():
    '''註冊'''
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
            # 註冊資訊沒有問題則將使用者名稱密碼寫入資料庫(更改密碼)
            usrs_info[new_name]=new_password
            with open(filepath,'wb') as usr_file:
                pickle.dump(usrs_info,usr_file)
            messagebox.showinfo('歡迎','註冊成功。')
            window_sign_up.destroy
    window_sign_up = tk.Toplevel(window)
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
    # ---------- #
    Sign_up_ver1 = tk.StringVar()
    Sign_up_ver2 = tk.StringVar()
    Sign_up_ver3 = tk.StringVar()
    # ---------- #
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
    ttk.Button(window_sign_up, text='Finish', command=window_sign_up.destroy).place(x=13, y=132)
    ttk.Button(window_sign_up, text='OK', command=Sign_up_OK).place(x=160, y=132)

    window_sign_up.mainloop()

# 要檢查的檔案路徑
filepath = "Users_info"
# 載入本地已有的使用者資訊,如果沒有則已有使用者資訊為空
try:
    with open(filepath,'rb') as usr_file:
        usrs_info = pickle.load(usr_file)
except FileNotFoundError:
    usrs_info = {}

Main()