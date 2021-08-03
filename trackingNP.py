from tkinter import *
import requests

#Window creating
def setwindow(win):
    win.title("Tracking NP")
    w = 600
    h = 500
    x = int((win.winfo_screenwidth() - w)/2)
    y = int((win.winfo_screenheight() - h) / 2)
    win.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))
    win.resizable(False, False)
    win.config(bg='#eef')

#Status request
def apirequest(tracks):
    api_url = 'https://api.novaposhta.ua/v2.0/json/'
    params = {
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [{"DocumentNumber": t} for t in tracks]
        }
    }
    data = requests.post(api_url, json=params).json()
    res = []
    if 'success' in data:
        for i in range(len(data['data'])):
            res.append(data['data'][i]['Status'][:35])
    else:
        res = ['Не вдалося здійснити перевірку.', 'Спробуйте пізніше.']
    return res

#Filling textareas
def reqtracks(tbox, rbox):
    tracks = tbox.get('1.0', 'end').split()
    tbox.delete('1.0', 'end')
    tbox.insert(END, '\n\n'.join(tracks))
    rbox.config(state=NORMAL)
    rbox.delete('1.0', 'end')
    rbox.insert(END, '\n\n'.join(apirequest(tracks)))
    rbox.config(state=DISABLED)

win=Tk()
setwindow(win)

tracklabel = Label(win, text='Номери ТТН', font='Tahoma 10', bg='#eef', fg='#000')
tracklabel.place(relx=0.05, rely=0.02, anchor='nw', relwidth=0.25)
statuslabel = Label(win, text='Статуси', font='Tahoma 10', bg='#eef', fg='#000')
statuslabel.place(relx=0.95, rely=0.02, anchor='ne', relwidth=0.6)

trackbox = Text(win)
trackbox.place(relx=0.05, rely=0.1, anchor='nw', relwidth=0.25, relheight=0.75)
resultbox = Text(win, state=DISABLED)
resultbox.place(relx=0.95, rely=0.1, anchor='ne', relwidth=0.6, relheight=0.75)

def callforbutton(tb=trackbox, rb=resultbox):
    reqtracks(tb, rb)

butsend = Button(win, text='Перевірити', bg='#acf', font='Tahoma 12', command=callforbutton)
butsend.place(relx=0.5, rely=0.97, anchor='s')

win.mainloop()
