from bioblend import galaxy
import time, argparse, requests, os, csv
import psycopg2

#{u'username': u'dchristiany', u'deleted': False, u'id': u'a799d38679e985db', u'last_password_change': u'2018-05-17T15:07:08.015458', u'active': True, u'model_class': u'User', u'email': u'david.christiany@gmail.com'}

def get_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", help="url of galaxy instance to copy", required=True)
    parser.add_argument("-k","--key", help="admin apikey of instance to copy", required=True)
    parser.add_argument("-h1","--host",help="",required=True)
    parser.add_argument("-u","--user",help="",required=True)
    parser.add_argument("-db","--database",help="",required=True)
    parser.add_argument("-p","--password",help="",required=True)
    parser.add_argument("--tmp_dir",help="",required=False,default='.')
    args = parser.parse_args()
    if args.ref[-1]!='/' : args.ref = args.ref+"/"
    return args

class Instance:

    def __init__(self,url,admin_key):
        self.url = url
        self.admin_key = admin_key
        self.config = galaxy.GalaxyInstance(url,admin_key).config
        self.usr = galaxy.GalaxyInstance(url,admin_key).users
        self.quotas = galaxy.GalaxyInstance(url,admin_key).quotas

    @property
    def mails(self):
        return [e['email'] for e in self.usr.get_users()]

    @property
    def version(self):
        return float(self.config.get_version()['version_major'])

    def get_users(self):
        users_list = self.usr.get_users()
        users=[]
        for element in users_list:
            user = User(element['email'],element['id'],element['username'])
            user.apikey = self.get_apikey(user)
            if user.apikey == 'Not available.' : user.apikey = self.create_apikey(user)
            user.disk_usage = self.usr.show_user(user.id)['nice_total_disk_usage']
            user.quota = self.usr.show_user(user.id)['quota']
            users.append(user)
        return users

    def get_workflows(self,user):
        return galaxy.GalaxyInstance(url=self.url,key=user.apikey).workflows.get_workflows()

    def create_user(self,user):
        response = self.usr.create_local_user(user.name,user.mail,user.pwd)
        user.target_id = response['id']
        user.target_key =  self.usr.create_user_apikey(user.target_id)
        self.usr = galaxy.GalaxyInstance(self.url,self.admin_key).users               #update usr

    def get_id(self,user):
        for usr in self.usr.get_users(): 
            print (usr['email'])
            print (user.mail)
            if usr['email'] == user.mail: 
                return usr['id']
        return None

    def get_apikey(self,user):
        return self.usr.get_user_apikey(user.id)

    def create_apikey(self,user):
        return self.usr.create_user_apikey(user.id)

    def get_histories_ids(self,user,deleted=False):
        gi = galaxy.GalaxyInstance(url=self.url, key=user.apikey)
        histories = galaxy.histories.HistoryClient(gi)
        return  [history['id'] for history in histories.get_histories(deleted=deleted)]

    def init_history_archives(self,histories,histories_list):
        pending_histories = []
        for id in histories_list:
            jeha_id=histories.export_history(id, gzip=True, include_hidden=False, include_deleted=False, wait=False)
            if jeha_id == "":
                pending_histories.append(id)
        return pending_histories

    def download_histories(self,user,path,skip):
        path = path+"/"+user.name+"_histories"
        if not os.path.exists(path): os.mkdir(path)
        gi = galaxy.GalaxyInstance(url=self.url, key=user.apikey)
        histories = galaxy.histories.HistoryClient(gi)
        pending_histories = self.init_history_archives(histories,user.histories)                         #init histories archives
        i=1
        done_histories = []
        while len(done_histories) < len(user.histories):
            for id in user.histories:
                if id not in pending_histories and id not in done_histories:
                    filename = path+"/"+id+".tar.gz"
                    with open(filename,"wb") as outf:
                        print (filename+"\t"+str(i)+"/"+str(len(user.histories)))
                        for j in range(5):
                            try:
                                jeha_id=histories.export_history(id, gzip=True, include_hidden=False, include_deleted=False, wait=False)
                                histories.download_history(id, jeha_id, outf, chunk_size=4096)
                                done_histories.append(id)
                            except requests.exceptions.HTTPError as e:
                                if j < 5 :
                                    print (e)
                                    time.sleep(0.5)
                                    continue
                                else:
                                    print ("5 attempt without success for "+id)
                                    raise
                            break
                    i+=1
            if skip is True :
                print (str(i-1)+"/"+str(len(user.histories))+" histories downloaded")
                break
            else :
                if len(done_histories) < len(user.histories):
                    print ("waiting for pending histories (1')")
                    print ("\n".join(pending_histories))
                    time.sleep(60)
                #update histories status
                pending_histories = self.init_history_archives(histories,pending_histories)

    def upload_histories(self,user,path):
        path = path+"/"+user.name+"_histories"
        if os.path.exists(path):
            gi = galaxy.GalaxyInstance(url=self.url, key=user.apikey)
            histories = galaxy.histories.HistoryClient(gi)
            if os.path.isdir(path):
                files = os.listdir(path)
                for file in files:
                    print ("file:"+str(file))
                    histories.import_history(file_path=os.path.join(path,file))
                    time.sleep(5)
            else:
                if not path.endswith('tar.gz'): 
                    print('input file is not a tar.gz file')
                return histories.import_history(file_path=path)
        else:
            return "file path not valid"

    @property
    def quotas(self):
        quotas_list = self.quotas.get_quotas()
        return [self.quotas.show_quota(q['id']) for q in quotas_list]

    def create_quota(self):
        pass

    def import_workflows(self,user):
        gi = galaxy.GalaxyInstance(url=self.url, key=user.target_key)
        workflowsClient = galaxy.workflows.WorkflowClient(gi)
        for wf in user.workflows:
            try:
                return workflowsClient.import_workflow_dict(wf,publish=False)
            except requests.exceptions.HTTPError as e:
                print(e)

class User:

    def __init__(self,mail,id,username):
        self.mail = mail
        self.id = id
        self.apikey = None
        self.name = username
        self.pwd = None
        self.histories = None
        self.total_histories = None
        self.quota = None
        self.disk_usage = None
        self.target_id = None
        self.target_key = None
        self.workflows = None
        self.creation_date = None
        self.last_connection = None

    def is_user(self,instance):
        return self.mail in instance.mails

    @property
    def workflows_id(self):
        if self.workflows is not None:
            return [wf['id'] for wf in self.workflows]

    @property
    def workflows_names(self):
        if self.workflows is not None:
            return [remove_ascii_bad_characters(wf['name']) for wf in self.workflows]

    @property
    def nb_workflows(self):
        if self.workflows is not None:
            return len(self.workflows)

    @property
    def nb_histories(self):
        if self.histories is not None:
            return len(self.histories)

    @property
    def nb_total_histories(self):
        if self.total_histories is not None:
            return len(self.histories)

class Database:

    def __init__(self,user,password,host,database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def get_password(self,user):
        try:
            connection = psycopg2.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = connection.cursor()
            query = """select password from galaxy_user where email = %s;"""
            cursor.execute(query,(user.mail,))
            return cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            if(connection):
                cursor.close()
                connection.close()

    def update_password(self,user,target_mails):
        try:
            connection = psycopg2.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = connection.cursor()
            if user.mail not in target_mails:
                sql_update_query = """update galaxy_user set password = %s where email = %s;"""
                cursor.execute(sql_update_query,(user.pwd,user.mail))                     #update password
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
                if(connection):
                    cursor.close()
                    connection.close()

    def get_passwords(self):
        try:
            connection = psycopg2.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = connection.cursor()
            cursor.execute("select email,password from galaxy_user;")
            record = cursor.fetchall()
            return record
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            if(connection):
                cursor.close()
                connection.close()

    def update_passwords(self,users,target_mails):
        for user in users:
            self.update_password(user,target_mails)
            
    def get_creation_date(self,user):
        try:
            connection = psycopg2.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = connection.cursor()
            command=str("select create_time from galaxy_user where email='"+user.mail+"';")
            cursor.execute(command)
            record = cursor.fetchall()
            return (record[0][0]) #datetime object
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    #print("PostgreSQL connection is closed")

    def get_last_connection(self,user):
        try:
            connection = psycopg2.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = connection.cursor()
            command=str("select galaxy_session.update_time from galaxy_session join galaxy_user on galaxy_session.user_id = galaxy_user.id where galaxy_user.email='"+user.mail+"' order by galaxy_session.update_time DESC limit 1;")
            cursor.execute(command)
            record = cursor.fetchall()
            return (record[0][0]) #datetime object
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL for last connection of user "+user.name, error)
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    #print("PostgreSQL connection is closed")

def remove_ascii_bad_characters(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def create_users_infos_file(users,path):
    path = os.path.join(path,"users_infos.csv")
    header = ["user","id","username","apikey","nb_histories","nb_total_histories","histories_list","password","disk_usage","nb_workflows","workflows_ids","workflows_names","created","last connection"]
    with open(path, 'w') as output:
        writer = csv.writer(output,delimiter="\t")
        writer.writerow(header)
        for user in users:
            line = [user.mail,user.id,user.name,user.apikey,user.nb_histories,user.nb_total_histories,user.histories,user.pwd,user.disk_usage,user.nb_workflows,";".join(user.workflows_id),";".join(user.workflows_names),user.creation_date,user.last_connection]
            writer.writerow(line)

def main():

    #get args from command
    print ("get args")
    args = get_args()

    print ("init instance")
    #init galaxy instances
    galaxy_ref = Instance(args.ref,args.key)

    print ("init database")
    #init database instances
    bdd_ref = Database(user = args.user, password = args.password, host = args.host, database = args.database)
    print ("ok")

    print ("galaxy_ref version: "+str(galaxy_ref.version))

    #get users from ref galaxy
    print ("get users")
    users = galaxy_ref.get_users()

    #get missing attributes
    for user in users:

        #get attributes
        print("getting attributes")
        user.pwd = bdd_ref.get_password(user)
        user.histories = galaxy_ref.get_histories_ids(user)
        user.total_histories = galaxy_ref.get_histories_ids(user,deleted=True)
        user.workflows = galaxy_ref.get_workflows(user)
        user.creation_date = bdd_ref.get_creation_date(user)
        user.last_connection = bdd_ref.get_last_connection(user)
        print("Done")

    create_users_infos_file(users,args.tmp_dir)

if __name__ == "__main__":
    # execute only if run as a script
    main()
