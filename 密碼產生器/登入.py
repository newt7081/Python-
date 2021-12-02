import tkinter as tk
from tkinter import ttk
def Setup():
	def Detect_True():
		pass
	ver3 = tk.StringVar()
	ver4 = tk.StringVar()
	window = tk.Tk()
	x = "260"
	y = "150"
	Width = str(int(window.winfo_screenwidth()/2)-int(int(x)/2))
	Height = str(int(window.winfo_screenheight()/2)-int(int(y)/2))
	xy = x+"x"+y+'+'+Width+"+"+Height
	window.geometry(xy)
	window.title("登入")
	window.iconbitmap('amz4f-z4l89-001.ico')
	#畫布放置圖片
	canvas = tk.Canvas(window, height=150, width=260)
	imagefile = tk.PhotoImage(file='登入背景.png')
	canvas.create_image(0, 0, anchor='nw', image=imagefile)
	canvas.pack(side='top')
	# 標題
	ttk.Label(window, text="登入", font=('Segoe UI Black', 15)).pack()
	ttk.Label(window, text="").pack()
	# 帳號
	height_frame = tk.Frame(window)
	height_frame.pack(side=tk.TOP)
	ttk.Label(height_frame, text="帳號").pack(side=tk.LEFT)
	a1 = ttk.Entry(height_frame, textvariable=ver3).pack(side=tk.LEFT)
	# 密碼
	height_frame = tk.Frame(window)
	height_frame.pack(side=tk.TOP)
	ttk.Label(height_frame, text="密碼").pack(side=tk.LEFT)
	a1 = ttk.Entry(height_frame, textvariable=ver4, show='●').pack(side=tk.LEFT)
	ttk.Label(window, text="").pack()
	# 按鈕
	height_frame = tk.Frame(window)
	height_frame.pack(side=tk.TOP)
	ttk.Button(height_frame, text='Finish', command=window.destroy).pack(side=tk.LEFT)
	ttk.Label(height_frame, text="	").pack(side=tk.LEFT)
	ttk.Button(height_frame, text='OK', command=Detect_True).pack(side=tk.LEFT)