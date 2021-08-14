import pymongo
import re,logging
import smtplib

try:

    client=pymongo.MongoClient("mongodb://localhost:27017/") 
    mydatabase=client['bloodmanageDb']     
    collection_name=mydatabase['bloodmange']

    bloodlist=[]
    bloodview=[]


    class bloodbank:

        def bdata(self,name,address,bloodgroup,pincode,mobileno,last_donate,place):
            dic={"name":name,"address":address,"bloodgroup":bloodgroup,"pincode":pincode,"mobileno":mobileno,"lastdonated date":last_donate,"place":place}
            bloodlist.append(dic)

    def val(name,address,pincode,mobileno,bloodgroup,place):
        val1=re.search("^[A-Z]?[a-n]",name)
        val2=re.search("^[1-9]",pincode)
        val3=re.search("^[1-9]\d{9}$",mobileno)
        val4=re.search("^[A-Z]",address)
        val4=re.search("^[A-Z]?[a-z]",place)
        val5=re.search("^(A|B|AB|O)[+-]$",bloodgroup)
        if val1 and val2 and val3 and val4 and val5:
            return True
        else:
            return False

    obj1=bloodbank()

    while(True):
        print("1. add donors: ")
        print("2. search donors based on blood group: ")
        print("3. search donors based on blood group and place: ")
        print("4. update all donar details with their mobile no :")
        print("5. delete the donor using mobile no : ")
        print("6. display the total no of donors on each blood group : ")
        print("7. email the details:")
        print("8. view all the details")
        print("9. EXIT")

        choice=int(input("\nEnter the number of your choice:"))

        if (choice==1):
            name=input("\nEnter the name:")
            address=input("\nEnter your address:")
            bloodgroup=input("\nEnter your blood group:")
            mobileno=input("\nenter your mobile no: ")
            pincode=input("\nEnter your pincode:")
            last_donate=input("\nEnter your last date of donate:")
            place=input("\nEnter the place:")

            if val(name,address,pincode,mobileno,bloodgroup,place)==True:
                data=obj1.bdata(name,address,bloodgroup,pincode,mobileno,last_donate,place) 
                bloodlist.append(data)
                result=collection_name.insert_many(bloodlist)
                print(result.inserted_ids)
            else:
                logging.error("INVALID VALIDATION")
                break
            

        if(choice==2):
            n=input("enter the blood group to be searched: ")
            result2=collection_name.find({"bloodgroup":n})
            for i in result2:
                print(i)

        if(choice==3):
            n=input("enter the blood group to be searched: ")
            m=input("enter the place to searched : ")
            result3=collection_name.find({"$and":[{"bloodgroup":n},{"place":m}]})
            # result3=collection_name.find({"$or":[{"bloodgroup":n},{"place":m}]})
            for i in result3:
                print(i)



        if(choice==4):
            mno=input("enter the mobile no: ")
            na=input("enter the c name to be update: ")
            result3=collection_name.update_many({"mobileno":mno}, {"$set": {"name":na}})
            print(result3)

        if(choice==5):
            mb=input("enter the mobile no to delete: ")
            d=collection_name.delete_one({"mobileno":mb})
            print(d)


        if(choice==6):
            result=collection_name.aggregate([{"$group":{"_id":"$bloodgroup","count":{"$sum":1}}}]) 
            for i in result:        
                print(i) 
    
        if (choice==7):
                bloodgroup=input("Enter blood group : ")
                print(bloodgroup)
                connection=smtplib.SMTP("smtp.gmail.com",587)
                connection.starttls()
                connection.login("krupamh0@gmail.com","panipuri23@")
                message="immediately want A+ blood group in XY Hospital"
                connection.sendmail("krupa9927@gmail.com",bloodgroup,message)
                print("Mail sent sucessfully")
                connection.quit()

        if (choice==8):
            result1=collection_name.find()
            for i in result1:
                bloodview.append(i)
            print(bloodview)
            bloodview.clear()
                    
        if (choice==9):
            break    
except:
    logging.error("Something is wrong ERROR!!") 
finally:
    print("COMPLETED")      

