from you_get import common
from io import StringIO
from contextlib import redirect_stdout
import json
import tkinter as tk
from tkinter import Button, ttk
from tkinter import filedialog
from tkinter import messagebox
import sys


class Application():
    def __init__(self, master) -> None:
        self.master = master
        self.cur_row = 0
        # self.url = ''
        self.url = tk.StringVar()
        self.out_name = tk.StringVar()
        self.search_btn = None
        self.quality_cbb = None
        self.download_btn = None
        self.stream_ids = []
        self.out_dir = '.'
        self.win_init()
        
    
    def win_init(self):
        r = self.master
        l = ttk.Label(r, text='video url:')
        l.grid(row=self.cur_row, column=0)
        t = ttk.Entry(r, textvariable=self.url)
        t.grid(row=self.cur_row, column=1)
        self.cur_row += 1

        self.search_btn = ttk.Button(r, text='search resources', command=self.search)
        self.search_btn.grid(row=self.cur_row, columnspan=2)
        self.cur_row += 1

        l = ttk.Label(r, text='select quality: ')
        l.grid(row=self.cur_row, column=0)
        cbb = ttk.Combobox(r)
        cbb.grid(row=self.cur_row, column=1)
        cbb['value'] = ['None']
        cbb.current(0)
        self.quality_cbb = cbb
        self.cur_row += 1

        btn = ttk.Button(r, text='select output_folder', command=self.select_folder)
        btn.grid(row=self.cur_row, column=0)
        t_name = ttk.Entry(r, textvariable=self.out_name)
        # t_name.grid(row=self.cur_row, column=1)  # TODO: has bug cannot set file name
        self.cur_row += 1
        
        btn = ttk.Button(r, text='click to download', command=self.download)
        btn.grid(row=self.cur_row, columnspan=2)
        self.download_btn = btn
    
    def download(self):
        self.download_btn['text'] = 'downloading... please wait!'
        stream_id = self.quality_cbb.get().split(',')[0].strip()
        out_name = self.out_name.get().strip()
        if out_name:
            common.download_main(common.any_download, common.any_download_playlist, [self.url.get()], 
                                    playlist=False, info_only=False, json_output=False, caption=False,
                                    merge=True, output_dir=self.out_dir, output_filename=out_name, stream_id=stream_id)
        else:
            common.download_main(common.any_download, common.any_download_playlist, [self.url.get()], 
                                    playlist=False, info_only=False, json_output=False, caption=False,
                                    merge=True, output_dir=self.out_dir, stream_id=stream_id)
        self.download_btn['text'] = 'download finished!'
        sys.stdout.flush()
        messagebox.showinfo(title='Done', message='download finished.')
    
    def search(self):
        serach_txt = 'searching resources, please wait!'
        if self.search_btn['text'] == serach_txt:
            return
        # orig_btn_txt = self.search_btn['text']
        self.search_btn['text'] = 'searching resources, please wait!'
        with redirect_stdout(StringIO()) as sio:
            common.download_main(common.any_download, common.any_download_playlist, [self.url.get()], 
                                    playlist=False, info_only=False, json_output=True, caption=False,
                                    merge=True, output_dir='.') # , stream_id='flv480')
            json_out = json.loads(sio.getvalue())
        self.streams = json_out['streams']  # dict: key: stream_id  value: {container: mp4, quality: 720p, src: [video_list, audio_list]}
        self.search_btn['text'] = 'Done! click to search again.'  # orig_btn_txt
        self.set_stream_id(self.streams)
    
    def set_stream_id(self, streams):
        cbb_value = []
        for stream_id, value_dict in streams.items():
            format = value_dict['container']
            quality = value_dict['quality']
            cbb_value.append(f'{stream_id}, {format}, {quality}')
        self.quality_cbb['value'] = cbb_value
        self.quality_cbb.current(0)
    
    def select_folder(self):
        out_dir = filedialog.askdirectory()
        if out_dir:
            self.out_dir = out_dir
        else:
            self.out_dir = '.'
            

if __name__ == '__main__':
    root = tk.Tk()
    root.title('video downloader based on you-get')
    app = Application(master=root)
    root.mainloop()