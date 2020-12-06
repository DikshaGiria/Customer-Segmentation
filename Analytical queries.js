db.customers.find().limit(5);

#first query
db.customers.aggregate([{ $group : { _id : "$CustomerID", number : { $sum : 1 }}},{ $sort : { number: -1 } },{ $limit : 10 }]);
    
#second query
db.customers.aggregate({ $group : { _id : "$Description", number : { $sum : 1 }}},{ $sort : { number: -1 } },{ $limit : 10 });

#third query
db.customers.aggregate( [{$match: {Country : 'France'}},
                        { $group : { _id : "$CustomerID", number : { $sum : 1 }}},
                        { $sort : { number: -1 } },
                        { $limit : 1 }]);
                       
#Fourth query                     
db.customers.distinct('InvoiceNo', {Country: 'France'}).length                       