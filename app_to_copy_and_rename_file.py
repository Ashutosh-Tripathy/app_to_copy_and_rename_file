from os import listdir, rename
from os.path import isfile, join, isdir
# import tkinter as tk
from tkinter import Frame, Button, Label, Tk
from tkinter import filedialog
import shutil

class App(Frame):
    def __init__(self, root):
        self._source_path = None
        # self._destination_path = None
        # self._filenames_map_path = None
        self._filenames_map = None
        # self._files_at_source_paths = None
        self._files_at_source = None
        # root = Tk()
        self.create_app_view(root)

        self.dir_opt = dict([('parent', root), ('mustexist', True),
                             ('title', 'Select directory')])
        self.file_opt = dict([('parent', root), ('mustexist', True),
                              ('title', 'Select csv file'), ('filetypes', [('csv file', '*.csv')])])


    def _copy_file(self, filename, source, destination):
        src_file = join(source, filename)
        shutil.copy(src_file, destination)

    def _rename_file(self, old_filename, new_filename, destination):
        source_file = join(destination, old_filename)
        destination_file = join(destination, new_filename)
        rename(source_file, destination_file)

    def copy_and_raname_file(self):
        if self.is_valid_input():
            self._files_at_source = self.get_files(self._source_label['text'])
            self._filenames_map = self._get_file_name_map(self._filenames_map_label['text'])
            for filename, new_filename in self._filenames_map:
                if filename in self._files_at_source:
                    source = self._source_label['text']
                    destination = self._destination_label['text']
                    self._copy_file(filename, source, destination)
                    self._rename_file(filename, new_filename, destination)

        else:
            print("Invalid")


    def ask_directory(self):
        """Returns a selected directoryname."""
        return filedialog.askdirectory(**self.dir_opt)

    def ask_source_directory(self):
        path = self.ask_directory()
        if path:
            self._source_label['text'] = path

    def ask_detination_directory(self):
        path = self.ask_directory()
        if path:
            self._destination_label['text'] = path

    def ask_file_path(self):
        return filedialog.askopenfilename()

    def ask_csv_file_path(self):
        self._filenames_map_label['text'] = self.ask_file_path()

    @staticmethod
    def get_files(path):
        return [f for f in listdir(path) if isfile(join(path, f))]

    def is_valid_input(self):
        return isdir(self._source_label['text']) and isdir(self._destination_label['text']) and \
                self._filenames_map_label['text'].endswith('.csv')

    def _get_file_name_map(self, filenames_map_path):
        lines = [line.rstrip('\n') for line in open(self._filenames_map_label['text'])]
        return list((line.split(',')[0], line.split(',')[1]) for line in lines)

    def create_app_view(self, root):
        Frame.__init__(self, root)

        root.geometry('500x400+300+100')
        root.title('My app')

        button_opt = {'fill': 'x', 'padx': 20, 'pady': (20, 0)}
        label_opt = {'fill': 'x', 'padx': 20, 'pady': (5, 20)}
        # button_opt = label_opt = {}
        self._source_button = Button(self, text='Choose sourece directory....',
                                        command=self.ask_source_directory)
        self._source_button.pack(**button_opt)
        self._source_label = Label(self, text='source label', anchor='c')
        self._source_label.pack(**label_opt)

        self._destination_button = Button(self, text='Choose destination directory....',
                                             command=self.ask_detination_directory)
        self._destination_button.pack(**button_opt)
        self._destination_label = Label(self, text='destincation label', anchor='c')
        self._destination_label.pack(**label_opt)


        self._filenames_map_button = Button(self, text='Select csv file....',
                                               command=self.ask_csv_file_path)
        self._filenames_map_button.pack(**button_opt)
        self._filenames_map_label = Label(self, text='csv file path', anchor='c')
        self._filenames_map_label.pack(**label_opt)

        self._copy_button = Button(self, text='Copy And Rename',
                                      command=self.copy_and_raname_file).pack(**button_opt)
        # copy_button.pack()

if __name__=='__main__':
    root = Tk()
    app_view = App(root)
    app_view.pack(side='top', fill='both', expand=True)
    root.mainloop()