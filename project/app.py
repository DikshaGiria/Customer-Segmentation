from flask import Flask, render_template,request,redirect,url_for,flash
#from bson import ObjectId 
from pymongo import MongoClient 
import os

app = Flask(__name__)
title = "Customer Segmentation Application"
heading = "Customer Segmentation"

print("hey")
client = MongoClient("mongodb://127.0.0.1:27017") #host uri  
db = client.Project #Select the database  
customers = db.CustomerSegmentation #Select the collection name 
    
def redirect_url():    
    return request.args.get('next') 

@app.route("/")      
def homepage ():    
    #display the homepage      
    return render_template('index.html',t=title,h=heading) 

@app.route("/create", methods=['GET','POST'])
def create():
    #adding an invoice
    if request.method == 'POST':
        InvoiceNo=request.form["InvoiceNo"]  
        StockCode=request.form["StockCode"] 
        Description=request.form["Description"]    
        Quantity=request.form["Quantity"]
        InvoiceDate=request.form["InvoiceDate"]    
        UnitPrice=request.form["UnitPrice"]  
        CustomerID=request.form["CustomerID"]   
        Country=request.form["Country"] 
        customers.insert({ "InvoiceNo":InvoiceNo, "StockCode":StockCode, "Description":Description, "Quantity":Quantity, "InvoiceDate":InvoiceDate, "UnitPrice":UnitPrice, "CustomerID":CustomerID, "Country":Country })    
        return '<h1> Invoice Added! </h1>'
    return render_template('/create.html')

@app.route("/read")    
def read ():    
    #Display the Invoice
    InvoiceNo=request.values.get("InvoiceNo")
    form = customers.find_one({'InvoiceNo':InvoiceNo})
    print(InvoiceNo)
    #print(invoice[0],invoice[1])
    return render_template('read.html',form=form,t=title,h=heading) 

@app.route("/update")    
def update ():    
    InvoiceNo=request.values.get("InvoiceNo")   
    StockCode=request.values.get("StockCode")
    Quantity=request.values.get("Quantity")
    invoice = customers.find({"InvoiceNo":InvoiceNo, "StockCode":StockCode})
    print(invoice)
    i=list(invoice)
    if(len(i)!=0):
        newvalues = {"$set": {"Quantity": Quantity}}
        customers.update_one({"InvoiceNo":InvoiceNo, "StockCode":StockCode}, newvalues)
        print(newvalues)
        return render_template('update.html',invoice=invoice,h=heading,t=title)
    else:
        print("Invalid Input")
        return '<h1> Invalid Input </h1>' 

@app.route("/delete")    
def remove ():
    #Deleting a Task with various references    
    InvoiceNo=request.values.get("InvoiceNo")
    StockCode=request.values.get("StockCode")
    customers.remove({"InvoiceNo":InvoiceNo,"StockCode":StockCode})
    return render_template('delete.html')
    #return redirect("/")     

if __name__ == "__main__":
    app.run()       
