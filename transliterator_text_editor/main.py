from constants import LANGUAGE_LIST
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from tkinter import *
from tkinter import font, colorchooser, filedialog, messagebox
from tkinter.ttk import *
import tkinter as tk
import tkinter.ttk as ttk


class MyApp(Tk):
    """
    Inherits the tkinter class to modify its functionalities.
    """

    def __init__(self):
        super().__init__()
        self.init_dir = ""
        self.file_name = False
        self.geometry('1200x800')
        self.title("Indic Text Editor")
        self.resizable(True, True)

        # font family and font size functionality
        self.current_font_family = "Arial"
        self.current_font_size = 12
        self.current_lang = "Malayalam"

        # ----------------- menu bar ---------------------------------
        self.menu_bar = tk.Menu(self)
        self.add_menu_bar()

        # ----------------- end menu bar ---------------------------------
        # ----------------- tool box ---------------------------------

        tool_bar = ttk.Label(self)
        tool_bar.pack(side=tk.TOP, fill=tk.X)

        # Font Box
        font_tuple = font.families()
        self.font_family = tk.StringVar()
        font_box = ttk.Combobox(tool_bar, width=20, textvariable=self.font_family, state="readonly")
        font_box["values"] = font_tuple
        font_box.current(font_tuple.index("Arial"))
        font_box.grid(row=0, column=0, padx=2)

        # Size Box
        self.size_var = tk.IntVar()
        font_size = ttk.Combobox(tool_bar, width=14, textvariable=self.size_var, state="readonly")
        font_size["values"] = tuple(range(8, 80, 2))
        font_size.current(3)  # 12 is at index 4
        font_size.grid(row=0, column=1, padx=2)

        # Bold Button.
        self.bold_btn = ttk.Button(tool_bar, text="bold")
        self.bold_btn.grid(row=0, column=2, padx=2)

        # underline button
        underline_btn = ttk.Button(tool_bar, text="underline")
        underline_btn.grid(row=0, column=4, padx=2)

        # Font color button
        font_color_btn = ttk.Button(tool_bar, text="font color")
        font_color_btn.grid(row=0, column=5, padx=2)

        # align left button
        align_left_btn = ttk.Button(tool_bar, text="align left")
        align_left_btn.grid(row=0, column=6, padx=2)

        # align center button
        align_center_btn = ttk.Button(tool_bar, text="align center")
        align_center_btn.grid(row=0, column=7, padx=2)

        # align right button
        align_right_btn = ttk.Button(tool_bar, text="align right")
        align_right_btn.grid(row=0, column=8, padx=2)

        # Language Box
        lang_tuple = list(LANGUAGE_LIST.keys())
        self.lang_selected = tk.StringVar()
        lang_box = ttk.Combobox(tool_bar, width=20, textvariable=self.lang_selected, state="readonly")
        lang_box["values"] = lang_tuple
        lang_box.current(lang_tuple.index(self.current_lang))
        lang_box.grid(row=0, column=9, padx=2)

        # ------------------ end tool box ------------------------------
        # ------------------ text editor -------------------------------

        self.text_editor = tk.Text(self)
        self.text_editor.config(wrap="word", relief=tk.FLAT)

        scroll_bar = tk.Scrollbar(self)  # to add scroll bar
        self.text_editor.focus_set()  # cursor position
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)  # gridding scrollbar
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        scroll_bar.config(command=self.text_editor.yview)
        self.text_editor.config(yscrollcommand=scroll_bar.set)

        # ------------------ events -------------------------------

        self.bold_btn.configure(command=self.change_bold)
        font_box.bind("<<ComboboxSelected>>", self.change_font)
        font_size.bind("<<ComboboxSelected>>", self.change_font_size)
        lang_box.bind("<<ComboboxSelected>>", self.change_language)
        self.text_editor.configure(font=("Arial", 12))
        underline_btn.configure(command=self.change_underline)
        font_color_btn.configure(command=self.change_font_color)
        align_left_btn.configure(command=self.align_left)
        align_center_btn.configure(command=self.align_center)
        align_right_btn.configure(command=self.align_right)
        self.text_editor.bind("<space>", self.translate)
        self.text_editor.bind("<Return>", self.translate)

        # Binding the functions with keyword
        self.bind("<Control-o>", self.open_file)
        self.bind("<Control-n>", self.new_file)
        self.bind("<Control-s>", self.save_file)
        self.bind("<Control-a>", self.save_as_file)
        self.bind("<Control-q>", self.exit_func)
        self.bind("<Control-f>", self.find_func)

        # ------------------ end events -------------------------------
        # ------------------ end text editor -------------------------------

        # ------------------ status bar -------------------------------

        self.status_bar = ttk.Label(self, text="Status Bar")
        self.status_bar.pack(side=tk.BOTTOM)

        self.text_changed = False
        self.text_editor.bind("<<Modified>>", self.changed)

        # ------------------ end status bar -------------------------------

    def add_menu_bar(self):
        # Adding file menu
        file_menu = tk.Menu(self.menu_bar, title='file menu', tearoff=False)  # file
        self.menu_bar.add_cascade(label="file", menu=file_menu)  # Top Line
        file_menu.add_command(label="New file", command=lambda: self.new_file(),
                              accelerator="Ctrl+n")
        file_menu.add_command(label="Open file", command=lambda: self.text_editor.event_generate("<Control o>"),
                              accelerator="Ctrl+o")
        file_menu.add_command(label="Save", command=lambda: self.text_editor.event_generate("<Control s>"),
                              accelerator="Ctrl+s")
        file_menu.add_command(label="Save As..", command=lambda: self.text_editor.event_generate("<Control a>"),
                              accelerator="Ctrl+a")
        file_menu.add_command(label="Close", command=self.close_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_func, accelerator="Ctrl+q")

        # Add edit menu
        edit_menu = tk.Menu(self.menu_bar, title='edit menu', tearoff=False)  # edit
        self.menu_bar.add_cascade(label="edit", menu=edit_menu)  # Top Line
        # TODO : Add option for malayalam keyboard, Convert an entire file from manglish to malayalam, Delete file
        edit_menu.add_command(label="Copy", compound=tk.LEFT, accelerator="Ctrl+c",
                              command=lambda: self.text_editor.event_generate("<Control c>"))
        edit_menu.add_command(label="Paste", compound=tk.LEFT, accelerator="Ctrl+v",
                              command=lambda: self.text_editor.event_generate("<Control v>"))
        edit_menu.add_command(label="Cut", compound=tk.LEFT, accelerator="Ctrl+x",
                              command=lambda: self.text_editor.event_generate("<Control x>"))
        edit_menu.add_command(label="Clear All", compound=tk.LEFT, accelerator="Ctrl+Alt+x",
                              command=lambda: self.text_editor.delete(1.0, tk.END))
        edit_menu.add_command(label="Find", compound=tk.LEFT, accelerator="Ctrl+f", command=self.find_func)
        edit_menu.add_separator()
        edit_menu.add_command(label="Malayalam Keyboard", command=self.find_func)
        edit_menu.add_command(label="Convert File", command=self.find_func)
        edit_menu.add_command(label="Delete File", command=self.find_func)

        help_menu = tk.Menu(self.menu_bar, title='help menu', tearoff=False)  # help
        self.menu_bar.add_cascade(label="help", menu=help_menu)  # Top Line
        help_menu.add_command(label="about", command=self.about)

        self.config(menu=self.menu_bar)  # adding menu to window

    def change_font(self, event=None):
        self.current_font_family = self.font_family.get()
        self.text_editor.configure(font=(self.current_font_family, self.current_font_size))

    def change_font_size(self, event=None):
        self.current_font_size = self.size_var.get()
        self.text_editor.configure(font=(self.current_font_family, self.current_font_size))

    def change_bold(self):
        text_property = tk.font.Font(font=self.text_editor["font"])  # dictionary
        if text_property.actual()["weight"] == "normal":
            self.text_editor.config(font=(self.current_font_family, self.current_font_size, "bold"))
        if text_property.actual()["weight"] == "bold":
            self.text_editor.config(font=(self.current_font_family, self.current_font_size, "normal"))

    def change_underline(self):
        text_property = tk.font.Font(font=self.text_editor["font"])  # dictionary
        if text_property.actual()["underline"] == 0:
            self.text_editor.config(font=(self.current_font_family, self.current_font_size, "underline"))
        if text_property.actual()["underline"] == 1:
            self.text_editor.config(font=(self.current_font_family, self.current_font_size, "normal"))

    def change_font_color(self):
        color_var = colorchooser.askcolor()
        self.text_editor.configure(fg=color_var[1])

    def align_left(self):
        text_content = self.text_editor.get(1.0, "end")
        self.text_editor.tag_config("left", justify=tk.LEFT)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, "left")

    def align_center(self):
        text_content = self.text_editor.get(1.0, "end")
        self.text_editor.tag_config("center", justify=tk.CENTER)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, "center")

    def align_right(self):
        text_content = self.text_editor.get(1.0, "end")
        self.text_editor.tag_config("right", justify=tk.RIGHT)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, "right")

    def changed(self, event=None):
        if self.text_editor.edit_modified():
            self.text_changed = True
            words = len(self.text_editor.get(1.0, "end-1c").split())
            characters = len(self.text_editor.get(1.0, "end-1c"))
            self.status_bar.config(text=f'Characters:{characters} Words: {words}')
        self.text_editor.edit_modified(False)  # Increase the count of the char and words

    def change_language(self, event=None):
        self.current_lang = self.lang_selected.get()

    def translate(self, event):
        """
        The method translates manglish text to malayalam using trans-literate method.

        :param event: The event
        :return: None
        """
        final_result = ''
        sub_string = ''
        word = str(self.text_editor.get(0.0, tk.END)).rstrip("\n").split(" ")[-1].split('\n')[-1]
        current_mal_text = str(self.text_editor.get(0.0, tk.END)).rstrip('\n').rstrip(word)
        # Translating alphabets avoiding non-alphabetic characters
        for element in word:
            if element.isalpha():
                sub_string += element
            else:
                result = transliterate(sub_string, sanscript.ITRANS, LANGUAGE_LIST[self.current_lang]) if sub_string else ''
                final_result += result + element
                sub_string = ''
        if sub_string:
            final_result += transliterate(sub_string, sanscript.ITRANS, LANGUAGE_LIST[self.current_lang]) if sub_string else ''
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(0.0, current_mal_text)
        self.text_editor.insert(tk.END, final_result)

    def new_file(self, event=None):
        # Delete previous text
        self.text_editor.delete('1.0', END)

        self.file_name = False

    def exit_func(self, event=None):
        try:
            if self.text_changed:
                mbox = messagebox.askyesnocancel(title="Wait!", message="Hey Wait ! Don't You want to save the File !")
                if mbox is True:  # Save krne h file :)  is true to be used as cancel is also false value
                    if self.file_name:
                        content = self.text_editor.get(1.0, tk.END)
                        with open(self.file_name, "w", encoding="utf-8") as fw:
                            fw.write(content)
                            self.destroy()
                    else:
                        content2 = self.text_editor.get(1.0, tk.END)
                        self.file_name = filedialog.asksaveasfile(mode="w", defaultextension=".txt",
                                                                  filetypes=(
                                                                  ("Text File", "*.txt"), ("All Files", "*.*")))
                        self.file_name.write(content2)
                        self.file_name.close()
                        self.destroy()
                elif mbox is False:
                    self.destroy()
            else:
                self.destroy()
        except:
            return

    def open_file(self, event):
        # Delete previous text
        self.text_editor.delete('1.0', END)
        file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Rtf File", '*.rtf'),
                                                     ("All Files", '*.*')],
                                          defaultextension=".txt", initialdir=self.init_dir, title='Open File')
        if file:
            # Make file global so that it can be accessed on saving.
            self.file_name = file  # set the file name
            self.title(self.file_name)  # update the GUI title
            fob = open(file, 'r')  # open in read mode
            my_str1 = fob.read()  # read data from file & store in variable
            self.text_editor.insert(tk.END, my_str1)  # add new data from file to text box
            fob.close()

    def save_file(self, event):
        if self.file_name:  # if default file name is still there
            fob = open(self.file_name, 'w')  # open the file in write mode
            my_str1 = self.text_editor.get("1.0", tk.END)  # collect data from text widget
            fob.write(my_str1)  # write to file
            self.title(self.file_name)  # Update the GUI title with file name
            fob.close()  # Close file pointer
        else:
            self.save_as_file(event)  # call the function

    def save_as_file(self, event):
        file = filedialog.asksaveasfilename(
            title='Save File',
            filetypes=[("Text Files", "*.txt"), ("Rtf File", '*.rtf'),
                       ("All Files", '*.*')],
            defaultextension=".*", initialdir=self.init_dir)
        if file:  # if user has not cancelled the dialog to save
            fob = open(file, 'w')  # open the file in write mode
            my_str1 = self.text_editor.get("1.0", tk.END)  # collect data from text widget
            fob.write(my_str1)  # write to file
            self.title(file)  # Update the GUI title with file name
            fob.close()  # Close file pointer
        else:  # user has cancelled the operation
            print("No file chosen")

    def close_file(self):
        self.text_editor.delete('1.0', tk.END)  # remove the content from text widget
        self.title('')  # remove the title of GUI

        self.file_name = False

    def about(self):
        about_window = Toplevel(self)
        string = "This is a text editor which is designed in tkinter python for editing malayalam which is written " \
                 "as manglish.\n In the case of anu issues you can raise a ticket at " \
                 "https://github.com/MerinRose123/manglish_text_editor .\n "
        label = Label(about_window, text=string)
        label.pack()

    # find functionally in edit command (last option)
    def find_func(self, event=None):
        def find():
            word = find_input.get()
            self.text_editor.tag_remove('match', "1.0", tk.END)
            matches = 0
            if word:
                start_pos = "1.0"
                while True:
                    start_pos = self.text_editor.search(word, start_pos, stopindex=tk.END)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+ {len(word)}c"
                    self.text_editor.tag_add("match", start_pos, end_pos)
                    matches += 1
                    start_pos = end_pos
                    self.text_editor.tag_config("match", foreground="yellow", background="green")

        def replace():
            word = find_input.get()
            replace_text = replace_input.get()
            content = self.text_editor.get(1.0, tk.END)

            new_content = content.replace(word, replace_text)
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, new_content)

        # Dialog box for Find and Replace
        find_dialogue = tk.Toplevel()
        find_dialogue.geometry("375x250+500+200")
        find_dialogue.title("Find")
        find_dialogue.resizable(0, 0)  # Can't maximise and minimise

        # Frame
        find_frame = ttk.LabelFrame(find_dialogue, text="Find/ Replace")
        find_frame.pack(pady=20)

        # labels
        text_find_label = ttk.Label(find_frame, text="Find : ")
        text_replace_label = ttk.Label(find_frame, text="Replace :")

        # entry

        find_input = ttk.Entry(find_frame, width=30)
        replace_input = ttk.Entry(find_frame, width=30)

        # Button
        find_button = ttk.Button(find_frame, text="Find", command=find)
        replace_button = ttk.Button(find_frame, text="Replace", command=replace)

        # Label Grid

        text_find_label.grid(row=0, column=0, padx=4, pady=4)
        text_replace_label.grid(row=1, column=0, padx=4, pady=4)

        # Entry grid

        find_input.grid(row=0, column=1, padx=4, pady=4)
        replace_input.grid(row=1, column=1, padx=4, pady=4)

        # Button grid

        find_button.grid(row=2, column=0, padx=2, pady=2)
        replace_button.grid(row=2, column=1, padx=2, pady=2)

        find_dialogue.mainloop()


if __name__ == "__main__":
    print("Running the text editor")
    myapp = MyApp()
    myapp.mainloop()
