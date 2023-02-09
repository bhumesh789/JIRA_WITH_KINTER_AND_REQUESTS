import tkinter as tk
import mysql.connector as mysql
import requests

con = mysql.connect(
    host='localhost',
    user='root',
    password='1',
    database='Jira'
)
mycursor = con.cursor()

TicketQuery = "SELECT * FROM AllTicket"
mycursor.execute(TicketQuery)
allTicket = mycursor.fetchall()

def on_button_click():

    url = "https://magical.atlassian.net/rest/api/3/search"
    headers = {
            "Accept":"application/json",
            "Content-Type":"application/json"
    }
    query = {
            "jql":"project = JIR"
    }
    response = requests.get(url,headers=headers,params=query,auth=("bhumeshkewat10@gmail.com","vpaqB9vnQZtRCWKrhAWhE4C4"))  
    data = response.json()

    issues = data['issues']
    TicketQuery = "SELECT * FROM AllTicket"
    mycursor.execute(TicketQuery)
    allTicket = mycursor.fetchall()

    TicketId = []
    for ticket in allTicket:
        TicketId.append(int(ticket[1]))

    for issue in issues:

        number,name,description = issue['id'],issue['fields']['issuetype']['name'],issue['fields']['description']["content"][0]["content"][0]["text"]
        reporter,status,DueDate = issue['fields']['reporter']['displayName'],issue['fields']['status']['name'],issue['fields']['created']

        if int(number) in TicketId:
            TicketQ = f'UPDATE AllTicket SET Number={number},Name="{name}",Description="{description}",Reporter="{reporter}",Status="{status}",DueDate="{DueDate}" WHERE Number={number}'
            mycursor.execute(TicketQ)
            con.commit()
        else:
            ticketQuery = f'INSERT INTO AllTicket (Number,Name,Description,Reporter,Status,DueDate) VALUES({number},"{name}","{description}","{reporter}","{status}","{DueDate}")'
            mycursor.execute(ticketQuery)
            con.commit()

    count = 0
    Tobj = {}
    for ticket in allTicket:
        Tobj["id"] = ticket[0]
        Tobj["Number"] = ticket[1]
        Tobj["Name"] = ticket[2]
        Tobj["Description"] = ticket[3]
        Tobj["Reporter"] = ticket[4]
        Tobj["Status"] = ticket[5]
        Tobj["DueDate"] = ticket[6]
        count += 1
        listbox.insert("end", f"Ticket {count}.{Tobj}")


root = tk.Tk()

root.title("My Tkinter GUI")
root.geometry("1700x900")

frame = tk.Frame(root)
frame.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
listbox.pack(side="left", fill="both", expand=True)

scrollbar.config(command=listbox.yview)


tCount = 0
TicketObject = {}
for ticket in allTicket:
    TicketObject["id"] = ticket[0]
    TicketObject["Number"] = ticket[1]
    TicketObject["Name"] = ticket[2]
    TicketObject["Description"] = ticket[3]
    TicketObject["Reporter"] = ticket[4]
    TicketObject["Status"] = ticket[5]
    TicketObject["DueDate"] = ticket[6]
    tCount += 1
    listbox.insert("end", f"Ticket{tCount}.{TicketObject}")


button = tk.Button(root, text="Refresh", command=on_button_click,fg="yellow",bg='blue',bd=6,relief="sunken",font="bold")
button.pack(side='left',anchor="nw")

root.mainloop()