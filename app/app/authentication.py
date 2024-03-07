from ldap3 import Server, Connection, ALL

# This file is not used for the global applicaiton.
def ldap_authentication(username,password):
    try:
        server = Server("KAPSDCP01.KAP.LOCAL",get_info=ALL)
        conn = Connection(server,user="KAP\\"+username,password=password,check_names=True,read_only=True,
                          auto_bind=False)
        if not conn.bind():
            return "Authentication Error",False
        else:
            return "Successfully logged in",True
    except:
        return "Unexpected error happned during authentication",False
