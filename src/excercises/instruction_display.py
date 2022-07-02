import threading
import tkinter as tk
from threading import Condition
from PIL import Image, ImageTk
import cv2


class InstructionDisplay:
    def __init__(self, success_image=None):
        self.instruction_label = None
        self.img_label = None
        self.root = tk.Tk()
        self.root.title("Instructions")
        self.cond = Condition()
        self.ready_to_display = False
        self.current_instruction = None
        self.root.bind("<<Instruction>>", self._display_instruction_mainloop)
        self.root.bind("<<Success>>", self._display_success_mainloop)
        self.root.bind("<<Exit>>", self._close_window_mainloop)
        self.root.configure(background='white')
        self.root.minsize(200,260)
        self.success_image = success_image

    def run(self):
        while True:
            with self.cond:
                while not self.ready_to_display:
                    self.cond.wait()  # block until ready
                self.root.mainloop()
                self.ready_to_display = False

    def mark_ready(self):
        with self.cond:
            self.ready_to_display = True
            self.cond.notify()

    def _cleanup(self):
        if self.instruction_label:
            self.instruction_label.destroy()
        if self.img_label:
            self.img_label.destroy()

    def _convert_to_tl(self,img):
        blue,green,red = cv2.split(img)
        img = cv2.merge((red,green,blue))
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk

    def _display_instruction_mainloop(self, *args):
        self._cleanup()
        self.instruction_label = tk.Label(self.root, text=self.current_instruction.text,background='white', wraplengt=200)
        self.instruction_label.place(x=0, y=200)
        if self.current_instruction.image is not None:
            img = self._convert_to_tl(self.current_instruction.image)
            self.img_label = tk.Label(self.root, image=img)
            self.img_label.image = img
            self.img_label.pack()


    def display_instruction(self, instruction):
        self.current_instruction = instruction
        self.root.event_generate("<<Instruction>>")

    def _display_success_mainloop(self, *args):
        self._cleanup()
        self.instruction_label = tk.Label(self.root, text="Good Job!",background='white', wraplengt=200)
        self.instruction_label.place(x=0, y=200)
        if self.success_image is not None:
            img = self._convert_to_tl(self.success_image)
            self.img_label = tk.Label(self.root, image=img)
            self.img_label.image = img
            self.img_label.pack()

    def display_success(self):
        self.root.event_generate("<<Success>>")

    def _close_window_mainloop(self, *args):
        self.root.destroy()

    def close_window(self):
        self.root.event_generate("<<Exit>>")
