try:
    itemCode = items["itemCode"]
except KeyError:
    print "Bad parameter name"
else:    
    dbObject=db.GqlQuery("SELECT * FROM %s WHERE code=:1" % dbName,itemCode).get()
    try:    
        dbObject.delete() 
    except AttributeError:
        print "There's no item with that code"
    except:
        print "Unknow error" 
