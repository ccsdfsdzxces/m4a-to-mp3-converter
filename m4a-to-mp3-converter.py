import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading

class M4AToMP3Converter:
    def __init__(self, master):
        self.master = master
        master.title("M4A to MP3 转换器")
        master.geometry("600x500")
        master.resizable(False, False)

        # 输入文件列表
        self.input_files_label = tk.Label(master, text="选择的M4A文件:")
        self.input_files_label.pack(pady=(10, 0))

        self.input_files_listbox = tk.Listbox(master, width=70, height=10)
        self.input_files_listbox.pack(pady=10, padx=20)

        # 按钮框架
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        # 选择文件按钮
        self.select_files_button = tk.Button(
            self.button_frame, 
            text="选择M4A文件", 
            command=self.select_input_files
        )
        self.select_files_button.pack(side=tk.LEFT, padx=5)

        # 清除列表按钮
        self.clear_list_button = tk.Button(
            self.button_frame, 
            text="清除列表", 
            command=self.clear_input_files
        )
        self.clear_list_button.pack(side=tk.LEFT, padx=5)

        # 输出文件夹选择
        self.output_frame = tk.Frame(master)
        self.output_frame.pack(pady=10)

        self.output_path_label = tk.Label(self.output_frame, text="输出文件夹:")
        self.output_path_label.pack(side=tk.LEFT, padx=(0, 10))

        self.output_path_entry = tk.Entry(self.output_frame, width=40)
        self.output_path_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.select_output_button = tk.Button(
            self.output_frame, 
            text="选择输出文件夹", 
            command=self.select_output_folder
        )
        self.select_output_button.pack(side=tk.LEFT)

        # 转换进度条
        self.progress_label = tk.Label(master, text="转换进度:")
        self.progress_label.pack(pady=(10, 0))

        self.progress_bar = ttk.Progressbar(
            master, 
            orient="horizontal", 
            length=500, 
            mode="determinate"
        )
        self.progress_bar.pack(pady=10)

        # 转换按钮
        self.convert_button = tk.Button(
            master, 
            text="开始转换", 
            command=self.start_conversion
        )
        self.convert_button.pack(pady=10)

        # 状态标签
        self.status_label = tk.Label(master, text="", fg="green")
        self.status_label.pack(pady=10)

        # FFmpeg路径（请根据实际情况修改）
        self.ffmpeg_path = self.find_ffmpeg()

    def find_ffmpeg(self):
        """
        尝试定位FFmpeg可执行文件
        """
        # 常见的FFmpeg可能位置
        possible_paths = [
            r"C:\Users\86133\Downloads\ffmpeg-7.1-full_build\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
            "ffmpeg"  # 系统PATH中
        ]
        
        for path in possible_paths:
            try:
                # 检查FFmpeg是否可以正常运行
                subprocess.run([path, "-version"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               check=True)
                return path
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        # 如果找不到FFmpeg
        messagebox.showerror("错误", "未找到FFmpeg。请确保已安装FFmpeg并配置系统PATH")
        return None

    def select_input_files(self):
        filetypes = [('M4A Audio Files', '*.m4a')]
        files = filedialog.askopenfilenames(
            title="选择M4A文件", 
            filetypes=filetypes
        )
        
        # 清空并添加新选择的文件
        self.input_files_listbox.delete(0, tk.END)
        for file in files:
            self.input_files_listbox.insert(tk.END, file)

    def clear_input_files(self):
        self.input_files_listbox.delete(0, tk.END)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="选择输出文件夹")
        self.output_path_entry.delete(0, tk.END)
        self.output_path_entry.insert(0, folder)

    def start_conversion(self):
        # 检查FFmpeg是否可用
        if not self.ffmpeg_path:
            return

        # 获取输入文件和输出路径
        input_files = list(self.input_files_listbox.get(0, tk.END))
        output_path = self.output_path_entry.get()

        # 检查输入有效性
        if not input_files:
            messagebox.showerror("错误", "请先选择M4A文件")
            return
        
        if not output_path:
            messagebox.showerror("错误", "请选择输出文件夹")
            return

        # 禁用转换按钮防止重复点击
        self.convert_button.config(state=tk.DISABLED)
        
        # 重置进度条
        self.progress_bar["maximum"] = len(input_files)
        self.progress_bar["value"] = 0
        
        # 启动转换线程
        conversion_thread = threading.Thread(
            target=self.convert_files, 
            args=(input_files, output_path)
        )
        conversion_thread.start()

    def convert_files(self, input_files, output_path):
        successful_conversions = 0
        failed_conversions = 0

        for index, input_file in enumerate(input_files, 1):
            try:
                # 确保文件路径正确处理
                input_file = os.path.normpath(input_file)
                
                # 检查文件是否存在
                if not os.path.exists(input_file):
                    print(f"文件不存在: {input_file}")
                    failed_conversions += 1
                    self.update_progress(index, successful_conversions, failed_conversions)
                    continue

                # 生成输出文件名
                filename = os.path.splitext(os.path.basename(input_file))[0]
                output_file = os.path.join(output_path, f"{filename}.mp3")

                # FFmpeg转换命令，使用引号处理可能的特殊字符
                cmd = [
                    self.ffmpeg_path, 
                    '-i', f'"{input_file}"', 
                    '-acodec', 'libmp3lame', 
                    '-b:a', '128k', 
                    f'"{output_file}"'
                ]

                # 执行转换，使用 shell=True 处理复杂路径
                result = subprocess.run(
                    " ".join(cmd), 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True,
                    shell=True
                )

                # 检查转换是否成功
                if result.returncode == 0:
                    successful_conversions += 1
                else:
                    failed_conversions += 1
                    print(f"转换失败: {input_file}")
                    print(result.stderr)

                # 更新UI
                self.update_progress(index, successful_conversions, failed_conversions)

            except Exception as e:
                print(f"转换出错: {input_file}")
                print(str(e))
                failed_conversions += 1
                self.update_progress(index, successful_conversions, failed_conversions)

        # 线程结束后在主线程更新UI
        self.master.after(0, self.conversion_complete, successful_conversions, failed_conversions)

    def update_progress(self, current, successful, failed):
        # 在主线程更新进度条
        self.master.after(0, self._update_progress_ui, current, successful, failed)

    def _update_progress_ui(self, current, successful, failed):
        self.progress_bar["value"] = current
        self.status_label.config(
            text=f"已转换: {current}, 成功: {successful}, 失败: {failed}"
        )

    def conversion_complete(self, successful, failed):
        # 恢复转换按钮
        self.convert_button.config(state=tk.NORMAL)
        
        # 显示最终转换结果
        result_message = f"转换完成\n总文件: {successful + failed}\n成功: {successful}\n失败: {failed}"
        messagebox.showinfo("转换结果", result_message)

def main():
    root = tk.Tk()
    app = M4AToMP3Converter(root)
    root.mainloop()

if __name__ == "__main__":
    main()