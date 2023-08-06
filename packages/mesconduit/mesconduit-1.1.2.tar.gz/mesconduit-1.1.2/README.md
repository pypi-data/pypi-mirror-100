

42Q- MES - Conduit Integration Setup!

Author  - Melvin Paul Miki
Version - 1.1.2

#Importing the Module:

    > import mesconduit

#Creating a session:

    > session = mesconduit.conduit(url,username,password,device_id,clinet_id)
    
        Attributes Descriptions

                #  url        => Enter the url to do the conduit
                #  Username   => Enter the username of the user
                #  password   => Enter the password of the user
                #  station_id => Enter the device id to be processed
                #  client_id  => Enter the device id to be processed
            


Login Valdation:
    > session.mes_login()
        
        ==> True  - Authorised User
        ==> False - Unathorised User    


Stage Pasing the unit

    > session.mes_PassUnit("123456")

        ==> STATUS :: Respective Message from the MES

        Attributes Descriptions

                #  Unit Serial Number   => "123456"
        
Mutli Units Pasing 

    > session.mes_MultiPass(["1234","5678",.,.,.,.,n])

        ==> [STATUS :: Respective Message from the MES,STATUS :: Respective Message from the MES,.,.,.,.,.,n]

        Attributes Descriptions

                #  Unit Serial Numbers   => ["123456","5678"]


Applying MEO the Serial Number

    > session.mes_ApplyMeo("123456","Screw 1 - Passed")

        ==> STATUS :: Respective Message from the MES

        Attributes Descriptions

                #  Unit Serial Number   => "123456"
                #  Added MEO Message    => "Screw = 1" 



Adding non tracked component 


    > session.mes_AddNonTrackedComponent("123456","Strip","345363"):

        ==> STATUS :: Respective Message from the MES

        Attributes Descriptions

                #  Unit Serial Number   => "123456"
                #  Component Key        => "Strip" 
                #  Component Value      => "345363"  

Data Collector
    Execute in Command Prompt
        >python -c "import  mesconduit; mesconduit.start_app()"
    
    Ex:
        $Enter the conduit URL
            >www.conduit.com
        $Enter the operator Username
            >1234567
        $Enter the operator Password
            >1234567
        $Enter the Station Id
            >123
        $Enter the Client Id
            >abcb123
        $Serial Number?
            >12334BC123
        $STATUS :: Respective Message from the MES

