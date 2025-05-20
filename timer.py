import tkinter as tk
import time

class Stopwatch:
    def __init__(self, master):
        self.master = master
        self.master.title("精準碼表 (小數點後5位)")
        self.start_time = None
        self.running = False

        self.label = tk.Label(master, text="0.00000", font=("Courier", 40))
        self.label.pack(padx=20, pady=20)

        self.start_button = tk.Button(master, text="開始", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(master, text="停止", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(master, text="重設", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.update_clock()

    def start(self):
        if not self.running:
            self.start_time = time.perf_counter() - (float(self.label['text']))
            self.running = True

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.label.config(text="0.00000")

    def update_clock(self):
        if self.running:
            elapsed = time.perf_counter() - self.start_time
            self.label.config(text=f"{elapsed:.5f}")
        self.master.after(10, self.update_clock)  # 每 10ms 更新一次畫面

root = tk.Tk()
stopwatch = Stopwatch(root)
root.mainloop()
