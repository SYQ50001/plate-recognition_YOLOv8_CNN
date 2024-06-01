import cv2
import torch
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, font
from plate_recognition.plate_rec import init_model
from detect_rec_plate import load_model, det_rec_plate, draw_result

# 初始化模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
detect_model = load_model(r"weights/yolov8s.pt", device)
plate_rec_model = init_model(device, 'weights/plate_rec_color.pth', is_color=True)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('车牌识别系统')
        self.root.geometry('800x700')  # 设置窗口大小

        # 设置选择文件按钮
        self.btn_select = tk.Button(root, text='选择图片', command=self.select_image)
        self.btn_select.pack(side=tk.TOP, padx=10, pady=10)

        # 设置开始识别按钮
        self.btn_start = tk.Button(root, text='开始识别', command=self.start_recognition, state=tk.DISABLED)
        self.btn_start.pack(side=tk.TOP, padx=10, pady=10)

        # 图像显示区域
        self.panel = tk.Label(root)
        self.panel.pack(side=tk.TOP, fill="both", expand="yes")

        # 识别结果显示区域
        result_font = font.Font(size=14, weight="bold")
        self.result_label = tk.Label(root, text='识别结果将显示在这里', relief=tk.SUNKEN, font=result_font)
        self.result_label.pack(side=tk.BOTTOM, fill=tk.X, ipady=20)

        # 文件路径变量
        self.file_path = None

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if len(path) > 0:
            self.file_path = path
            self.btn_start['state'] = tk.NORMAL
            img = Image.open(self.file_path)
            img = img.resize((640, 480), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.panel.configure(image=img)
            self.panel.image = img
            self.result_label.configure(text="准备识别...")

    def start_recognition(self):
        if self.file_path:
            img = cv2.imread(self.file_path)
            img_ori = img.copy()
            result_list = det_rec_plate(img, img_ori, detect_model, plate_rec_model)
            img, result_str = draw_result(img, result_list)
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            img = img.resize((640, 480), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.panel.configure(image=img)
            self.panel.image = img
            self.result_label.configure(text=f"识别结果：{result_str}")
        else:
            messagebox.showinfo("错误", "请先选择一张图片")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.attributes('-topmost', True)  # 使窗口保持在最上层
    root.mainloop()
