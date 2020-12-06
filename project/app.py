from flask import Flask, render_template,request,redirect,url_for,flash
from pymongo import MongoClient 
import os
import json

app = Flask(__name__)
title = "Customer Segmentation Application"
heading = "Customer Segmentation"

print("Server Running")
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
        flash('Invoice Added!')
        return render_template('/create.html')
    return render_template('/create.html')

@app.route("/read")    
def read ():    
    #Display the Invoice
    InvoiceNo=request.values.get("InvoiceNo")
    form = customers.find({'InvoiceNo':InvoiceNo})
    print(InvoiceNo)
    print(form)
    invoice = []
    for i in form:
        invoice.append(i)
    print(invoice)
    return render_template('/read.html',invoice=invoice,t=title,h=heading)

@app.route("/update",methods=['GET','POST'])    
def update ():
    if request.method == 'POST':
        InvoiceNo=request.values.get("InvoiceNo")   
        StockCode=request.values.get("StockCode")
        Quantity=request.values.get("Quantity")
        print(InvoiceNo, StockCode, Quantity)
        invoice = customers.find_one({"InvoiceNo":InvoiceNo, "StockCode":StockCode})
        print(invoice)
        newvalues = {"$set": {"Quantity": Quantity}}
        temp=customers.update_one({"InvoiceNo":InvoiceNo, "StockCode":StockCode}, newvalues)
        print(newvalues)
        if(temp.modified_count > 0):
            flash('Invoice updated!')
        else:
            flash("Failed to update the invoice. Enter valid data.")
        return render_template('update.html',invoice=invoice,h=heading,t=title)
    return render_template('/update.html')

@app.route("/delete",methods=['GET','POST'])    
def remove ():
    #Deleting a Task with various references
    if request.method == 'POST':
        InvoiceNo=request.values.get("InvoiceNo")
        StockCode=request.values.get("StockCode")
        result=customers.delete_one({"InvoiceNo":InvoiceNo,"StockCode":StockCode})
        print(result.deleted_count)
        if(result.deleted_count > 0):
            flash('Item Deleted!')
        else:
            flash('Failed to delete the item.Enter valid data.')
    return render_template('delete.html')     

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
