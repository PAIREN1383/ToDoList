from tkinter import *
from tkinter import messagebox
import sqlite3

def Connect():
    conn = sqlite3.connect("To_Do.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, T_E_X_T text )")
    conn.commit()
    conn.close()

def View():
    conn = sqlite3.connect("To_Do.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo")
    rows = cur.fetchall()
    conn.close()
    return rows

def Insert(T_E_X_T):
    conn = sqlite3.connect("To_Do.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO todo VALUES (NULL,?)", (T_E_X_T,))
    conn.commit()
    conn.close()

def Delete(id):
    conn = sqlite3.connect("To_Do.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM todo WHERE id=?", (id,))
    conn.commit()
    conn.close()

def Update(id, TexT):
    conn = sqlite3.connect("To_Do.db")
    cur = conn.cursor()
    cur.execute("UPDATE todo SET T_E_X_T=? WHERE id=?", (TexT, id))
    conn.commit()
    conn.close()

def Search(TexT=""):
    conn = sqlite3.connect("To_Do.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo WHERE T_E_X_T=?", (TexT,))
    rows = cur.fetchall()
    conn.close()
    return rows

Connect()


# ============================== FrontEnd ==================================
window = Tk()
window.title("To Do List")
window.geometry("600x400")

Lb = Label(window, text="Write what needs to be done:")
Lb.grid(row=0, column=0)

Txt = StringVar()
Ent = Entry(window, textvariable=Txt, width=48)
Ent.grid(row=0, column=1)

LBox = Listbox(window, width=80, height=20)
LBox.grid(row=1, column=0, rowspan=1, columnspan=2)

Slb = Scrollbar(window)
Slb.grid(row=1, column=2)
Slb2 = Scrollbar(window)
Slb2.place(x=500, y=157)

LBox.configure(yscrollcommand=Slb.set)
Slb.configure(command=LBox.yview)
LBox.configure(xscrollcommand=Slb2.set)
Slb2.configure(command=LBox.xview)


def get_selected_row(event):
    global selected_Todo
    if len(LBox.curselection()) > 0:
        index = LBox.curselection()[0]
        selected_Todo = LBox.get(index)
        Txt.set(selected_Todo[1])

LBox.bind("<<ListboxSelect>>", get_selected_row)


def Show_All():
    Result = View()
    LBox.delete(0,END)
    for item in Result:
        LBox.insert(END,item)

def Search_2(Find):
    Result = Search(Find)
    LBox.delete(0,END)
    for item in Result:
        LBox.insert(END,item)

def Update_2(TxT):
    if len(LBox.curselection()) == 0:
        messagebox.showerror("Nothing selected", "Please click on text from list box.")
    else:
        Update(selected_Todo[0], TxT)
        Show_All()

def Insert_2(Add):
    Insert(Add)
    Show_All()

def Delete_2():
    if len(LBox.curselection()) == 0:
        messagebox.showerror("Nothing selected", "Please click on text from list box.")
    else:
        Delete(selected_Todo[0])
        Show_All()

def Delete_All():
    Y_N = messagebox.askyesno("Delete All", "Are you Sure?")
    if Y_N is True:
        for num in range(len(LBox.keys())):
            Delete(num)
        Show_All()

def Done():
    if len(LBox.curselection()) == 0:
        messagebox.showerror("Nothing selected", "Please click on text from list box.")
    else:
        D_o_n_e = selected_Todo[1] + " ---> Done"
        Update(selected_Todo[0], D_o_n_e)
        Show_All()


Show_All()
Btn_show = Button(window, text="Show All", width=8, command=Show_All)
Btn_show.place(x=520, y=0)
Btn_search = Button(window, text="Search", width=8, command=lambda: Search_2(Ent.get()))
Btn_search.place(x=520, y=30)
Btn_edit = Button(window, text="Edit", width=8, command=lambda: Update_2(Ent.get()))
Btn_edit.place(x=520, y=60)
Btn_in = Button(window, text="Insert", width=8, command=lambda: Insert_2(Ent.get()))
Btn_in.place(x=520, y=90)
Btn_del = Button(window, text="Delete", width=8, command=Delete_2)
Btn_del.place(x=520, y=120)
Btn_del_all = Button(window, text="Delete All", width=8, command=Delete_All)
Btn_del_all.place(x=520, y=150)
Btn_done = Button(window, text="Done", width=8, command=Done)
Btn_done.place(x=520, y=180)
Btn_exit = Button(window, text="Exit", width=8, command=window.destroy)
Btn_exit.place(x=520, y=210)

window.mainloop()
