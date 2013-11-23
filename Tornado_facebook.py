import tornado.gen
import tornado.web
import tornado.httpserver
import tornado.auth
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.log
import logging
import tornado.options
import time
import md5
from datetime import datetime
import json
from bson.json_util import dumps
from bson import json_util

import redis
import pymongo

#connect to Mongo
client = pymongo.MongoClient("localhost", 27017)
db = client.test

# connecct to redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

class Logger():    

    def config_logger(self, filePath, loggerName):
        self.filePath = filePath
        self.loggerName = loggerName
        self.logTime = time.asctime( time.localtime(time.time()) )
        
    
    def write_warning_to_logger(self, logType, logData):
        filePath = 'bruwz.log'
        logTime = time.asctime( time.localtime(time.time()) )

        f = open(filePath, 'a')
        errorMessage = logType+"\n"+logData+"\n  at - "+logTime+"\n"
        f.write(errorMessage)
        f.close()

class PyRestfulException(Exception):
    """ Class for PyRestful exceptions """
    def __init__(self,message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class User():
    @tornado.web.asynchronous
    def _check_FB_Token(self, logType, token , User_id):
        
        timer = time.time()
        
        if logType == 0:
            
            #call to check in DB
            getFB_token = db.dannysaban2.find_one({"fb_id_endFbToken":User_id})
            
            #test token - retrive from mongo and serialized results
            del getFB_token["_id"]
            serialized_result = json.dumps(getFB_token, sort_keys=True,indent=4, separators=(',', ': '))
            json_result = json.loads(serialized_result)
            
            if json_result < timer:
                userState = UserInit.Config.registrationStatus["registrationStatus"][3]["registered"]
                return userState
            else:
            
#             #call to check in DB
#             db.dannysaban2.find_one({"fb_id_endBruwzToken":User_id})
                userState = UserInit.Config.registrationStatus["registrationStatus"][1]["FB_invalid"]
                return userState 

    @tornado.web.asynchronous
    def _check_BR_Token(self, logType, token , User_id):
        
        timer = time.time()
        
        if logType == 0:
            
            #call to check in DB
            getBR_token = db.dannysaban2.find_one({"br_id_endFbToken":User_id})
            
            #test token - retrive from mongo and serialized results
            del getBR_token["_id"]
            serialized_result = json.dumps(getBR_token, sort_keys=True,indent=4, separators=(',', ': '))
            json_result = json.loads(serialized_result)
            
            if json_result < timer:
                userState = UserInit.Config.registrationStatus["registrationStatus"][3]["registered"]
                return userState
            else:
            
#             #call to check in DB
#             db.dannysaban2.find_one({"fb_id_endBruwzToken":User_id})
                userState = UserInit.Config.registrationStatus["registrationStatus"][2]["BR_invalid"]
                return userState 
      
    @tornado.web.asynchronous
    def _create_BR_Id(self):
        pass
    
    @tornado.web.asynchronous
    def _check_user_state(self,User_id):
        user_state = self._check_User_exist(User_id)
        return user_state
    
    @tornado.web.asynchronous
    def _check_FBuser_exist(self, User_id):
        
        # retrive data from mongoDB
        getData_me = db.dannysaban2.find_one({"fb_id":User_id})
        getData_fbImgURL = db.dannysaban2.find_one({"fb_id_fbImgURL":User_id})
        
        getData_bruwzImgURL = db.dannysaban2.find_one({"fb_id_bruwzImgURL":User_id})
        
        
        #retrive from mongo and serialized results
        del getData_me["_id"]
        serialized_results_me = json.dumps(getData_me, sort_keys=True,indent=4, separators=(',', ': '))
        json_result_me = json.loads(serialized_results_me) 
        
        
        
        #retrive from mongo and serialized results
        del getData_fbImgURL["_id"]
        serialized_results_pic = json.dumps(getData_fbImgURL, sort_keys=True,indent=4, separators=(',', ': '))
        json_result_pic = json.loads(serialized_results_pic) 
        
        set_user_state = 0
        return set_user_state
    
    @tornado.web.asynchronous
    def _check_valid_FBdata(self,User_id):
        pass

    @tornado.web.asynchronous
    def _check_valid_BRdata(self,User_id):
        pass   
    
class Fatch_Facebook_Data():
     
#-----------fatching facebook data-----------------
    
    @tornado.web.asynchronous
    def _fetch_FB_profile(self, profile_link):
        
        http_client = tornado.httpclient.AsyncHTTPClient()
        
        self.profile = profile_link
        
        #prepare -me- response for mongoDB insertion
        response_profile = yield http_client.fetch(self.profile)
        json_acceptable_profile = response_profile.body.replace("'", "\"")
        profile_data = json.loads(json_acceptable_profile)
        
        #close client
        http_client.close()
        
        Build_Responds.user_respond(profile_data)
        
        return True
    
    @tornado.web.asynchronous
    def _fetch_FB_likes(self, tv, movies, music):
        
        http_client = tornado.httpclient.AsyncHTTPClient()
        
        self.tv_likes = tv
        self.movies_likes = movies
        self.music_likes = music
        
        #prepare -me- response for mongoDB insertion
        response_tv_likes = yield http_client.fetch(self.tv_likes)
        json_acceptable_tv_likes = response_tv_likes.body.replace("'", "\"")
        tv_data = json.loads(json_acceptable_tv_likes)
        #close client
        http_client.close()
        
        #prepare -me- response for mongoDB insertion
        response_movies_likes = yield http_client.fetch(self.movies_likes)
        json_acceptable_movies_likes = response_movies_likes.body.replace("'", "\"")
        movies_data = json.loads(json_acceptable_movies_likes)
        #close client
        http_client.close()
        
        #prepare -me- response for mongoDB insertion
        response_music_likes = yield http_client.fetch(self.music_likes)
        json_acceptable_music_likes = response_music_likes.body.replace("'", "\"")
        music_data = json.loads(json_acceptable_music_likes)
        #close client
        http_client.close()
        
        total_likes =[tv_data, movies_data, music_data]
        
        Build_Responds.likes_respond(self, total_likes)
    
    @tornado.web.asynchronous
    def _fetch_FB_friends(self, friends_link):
        self.friends = friends_link
        pass   

class DBs():
    
    @tornado.web.asynchronous
    def _set_offline_data(self,User_id):
        pass
    
    @tornado.web.asynchronous
    def _get_offline_data(self,User_id):
        pass
    
    @tornado.web.asynchronous
    def _set_online_data(self,User_id):
        pass
       
    @tornado.web.asynchronous
    def _get_online_data(self,User_id):
        pass

class Build_Responds():
    
    def db_respond(self):
        pass
    
    def likes_respond(self, likes):
        
        #build rest response to client
        self.likes = likes['work']['data'][0]['work'][0]['employer']['name']
        fb_id = self.likes['fb_id_work']
        rest_likes = {"fb_id" : fb_id, "position" : position}
        
        return rest_likes
    
    def profile_respond(self, profile):
       
        #build rest response to client
        self.position = profile['work']['data'][0]['work'][0]['employer']['name']
        fb_id = self.position['fb_id_work']
        rest_profile = {"fb_id" : fb_id, "position" : position}
        
        return rest_profile
    
    def friends_respond(self, friends):
       
        #build rest response to client
        self.friends = friends['work']['data'][0]['work'][0]['employer']['name']
        fb_id = self.position['fb_id_work']
        rest_friends = {"fb_id" : fb_id, "position" : position}
        
        return rest_friends
    

#---------Login User------------------#

class UserInit(tornado.web.RequestHandler):
    
    def Config(self):
       

        self.registrationStatus = {"registrationStatus" :
                                        [
                                         {"new":                "0"}, # bruwz tokens not valid
                                         {"FB_invalid":         "1"}, # missing required data (beside image)
                                         {"BR_invalid":         "2"},
                                         {"registered":         "3"},
                                         {"blocked" :           "4"}, # blocked account
                                         {"temp":               "5"} # have required data, missing image
                                         #{"legit":              "4"}  # authenticated, heve all required data                                      
                                        ]
                                   }
        
#self.write(registrationStatus)
#self.finish()
        
        self.questions_values =  {
                                 "profession_val" :    {"qType":"0"},
                                 "homeTwon_val" :      {"qType":"1"},
                                 "relationship_val" :  {"qType":"2"},
                                 "music_val" :         {"qType":"3"},
                                 "movie_val" :         {"qType":"4"},
                                 "birthday_val" :      {"qType":"5"},
                                 "image_val" :         {"qType":"6"}     
                                 }
        
        
#self.write({"qType": profession_val["qType"]})
#self.finish()
        
        #questions to select
        self.questions = {"question":[
                                    {"music": "what is your favorite singer/band?"},
                                    {"movie": "what is your favorite movie/TVShow?"},
                                    {"img": "upload your image?"},
                                    {"birthday": "what is your birth date?"},
                                    {"relationship": "what is your relationship status?"},
                                    {"homeTown":"what is your hometown?"}
                                ]} 
        
        callback = [self.questions_values, self.questions ] 
        return callback
    
    @tornado.web.asynchronous
    def _messaging(self, logType, logData):
        raise PyRestfulException(logType+" : "+logData)
    
    @tornado.web.asynchronous
    def _call_logger(self,logType, logData):
        if logType == "WARNING:":
            sendWarning = Logger()
            sendWarning.write_warning_to_logger(logType, logData)     
        if logType == "ERROR:":
            sendError = Logger()
            sendError.write_warning_to_logger(logType, logData)
            

    
#-----------------START-----------------------                
            
    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, data = None ):
             
        getdata = {}
        mydata = self.get_argument('getdata', data)
        #GET params from url
        getMe = json.loads(mydata)
        logType = getMe['userInitReq']['loginType']
        #Globals
        User_id = getMe['userInitReq']['valId']
        token = getMe['userInitReq']['valToken']
        
# start logger        
#        self._call_logger(logType = 'WARNING:', logData = 'you have entered a wrong status value.')
#        self.messaging(logType, logData)
#         
#        self.write({"loginType error": "you have entered a wrong status value "})
#        self.finish()
# end logger
        
        #check user status
        if logType == 1:
            #validate token
            token_Status = self._check_token(logType, token, User_id)
            id_Validation = self._check_User_exist(User_id)
            
            if token_Status == 0:
                bruwzToken = token
            else:
                self.write({"errorLog_BrwuzToken":"Bruwz Token not valid: need a new Bruwz token "+str(logType)})
                self.finish()
            
            if id_Validation == 0:
                bruwzId = User_id
            else:
                self.write({"errorLog_BrwuzId":"Bruwz Id not valid: need to register "+str(logType)})
                self.finish()
            
            start_token_time = time.time()
            
            #check if BruwzToken valid
            get_user_state = self._check_User_exist(User_id)
            
            self.write({"errorLog":"BruwzToken not valid: need a new Bruwz token "+str(logType)})
            self.finish()
            
            callback = self._check_token(logType, token)
            regStatus = callback
            db.dannysaban2.insert({"fb_id_bruwzStatus":User_id, "data":{"registrationStatus":regStatus}})
            
        elif logType == 0:
            
            token_Status = self._check_token(logType, token, User_id)
            id_Validation = self._check_User_exist(User_id)
            
            fbToken = token
            fbId = User_id            
                   
            db.dannysaban2.insert({"fb_id_bruwzStatus":User_id,"data" :{"registrationStatus":regStatus}})            
            
            #generating secrets
            start_token_time = time.time()
            end_token_time = start_token_time + 3600 # set to 1 hour 
            
            #check if BruwzToken valid
            #..
            #...
            #...
            #-------------------------
            
            #generate bruwzId
            brz_int = int(start_token_time)
            brz_id = str(brz_int)
            #generate bruwzToken
            bruwz_id_token = str(brz_id)
            
            tmp_bruwz_token = md5.new(bruwz_id_token)
            bruwz_token = tmp_bruwz_token.hexdigest()
            
            #self.write(bruwz_token)
            #self.finish()
             
            # create bruwzToken and bruwzImgURL - insert to mongoDB
            db.dannysaban2.insert({ "fb_id_bruwzImgURL":User_id, "data":{"bruwzImgURL":None}  })
            db.dannysaban2.insert({"fb_id_bruwzToken":User_id, "data":{"bruwzToken":bruwz_token}})
            db.dannysaban2.insert({"fb_id_endBruwzToken":User_id, "data":{"endBruwzToken": end_token_time}})
            db.dannysaban2.insert({"fb_id_endFbToken":User_id, "data":{"endFbToken": end_token_time}})
            
            #test
            #get_fb_id_me_bruwzToken = db.dannysaban2.find_one({"fb_id_me_bruwzToken":User_id})
            #retrive from mongo and serialized results
            #del get_fb_id_me_bruwzToken["_id"]
            #serialized_results_2 = json.dumps(get_fb_id_me_bruwzToken, sort_keys=True,indent=4, separators=(',', ': '))
            #json_result_me_2 = json.loads(serialized_results_2) 
            
            #self.write(json_result_me_2)
            #self.finish()
            # end test
        else:
            Logger()
            self.write({"errorLog":"loginType error: wrong status value "+str(logType)})
            self.finish()
            # logger
            
            
        
        http_client = tornado.httpclient.AsyncHTTPClient()
        #http_client = tornado.httpclient.HTTPClient()
        
        #build links for data
        tv = "https://graph.facebook.com/fql?q=SELECT%20tv%20FROM%20user%20WHERE%20uid="+fbId+"&access_token="+fbToken
        movies = "https://graph.facebook.com/fql?q=SELECT%20movies%20FROM%20user%20WHERE%20uid="+fbId+"&access_token="+fbToken
        music ="https://graph.facebook.com/fql?q=SELECT%20music%20FROM%20user%20WHERE%20uid="+fbId+"&access_token="+fbToken
        Fatch_Facebook_Data.likes(tv, movies, music)
        
        me_pic_work = "https://graph.facebook.com/fql?q=SELECT%20last_name,%20pic,%20relationship_status,%20first_name,%20sex,%20birthday_date,%20%20work%20%20FROM%20user%20WHERE%20uid="+fbId+"&access_token="+fbToken
        Fatch_Facebook_Data.likes(me_pic_work)
        
        
        #prepare -me- response for mongoDB insertion
        response_me_pic_work = yield http_client.fetch(me_pic_work)
        json_acceptable_me_pic_work = response_me_pic_work.body.replace("'", "\"")
        dataMe = json.loads(json_acceptable_me_pic_work)
        
        #build rest response to client
        fname = dataMe['data'][0]['first_name']
        lname = dataMe['data'][0]['last_name']
        birthday = dataMe['data'][0]['birthday_date']       
        genderName = dataMe['data'][0]['sex']
        # check gender for setting values (0/1)
        if genderName == "male":
            gender = 0
        else:
            gender = 1
        relationship_status = dataMe['data'][0]["relationship_status"]
        fb_me_pic = dataMe['data'][0]['pic']
        position = dataMe['data'][0]['work'][0]['position']['name']
        
        #self.write({'position':position, 'pic':fb_me_pic, 'fname':fname, 'lname': lname, 'birthday': birthday, 'gender':gender, 'relationship_status': relationship_status })
        #self.finish()
        
#         response0 = yield http_client.fetch(me)
#         json_acceptable_string0 = response0.body.replace("'", "\"")
#         dataMe = json.loads(json_acceptable_string0)
#         
#         #prepare -pic- response for mongoDB insertion
#         response1 = yield http_client.fetch(fb_me_pic)
#         json_acceptable_string1 = response1.body.replace("'", "\"")
#         dataFbPic = json.loads(json_acceptable_string1)
        
        # insert dataMe and dataPic to mongoDB
        db.dannysaban2.insert({"fb_id":User_id, "me":me_pic_work})
        db.dannysaban2.insert({"fb_id_fbImgURL":User_id, "fbImgURL":fb_me_pic})
        
        
        #build response json
        rest_me = {'position':position, "pic":fb_me_pic, "fName":fname,"lName":lname, "gender": gender, 'birthday': birthday, "relationship_status":relationship_status, "userImage":None}#, "gender":relationship_status, "bruwzImgURL":None}
                
        
        
        #--------------------------------------------#
#         response1 = http_client.fetch(work)
#         json_acceptable_string = response1.body.replace("'", "\"")
#         data = json.loads(json_acceptable_string)
#         db.dannysaban2.insert({"fb_id_work":User_id, "work":data})
#         getData_work = db.dannysaban2.find_one({"fb_id_work":User_id})
#          
#         #retrive from mongo and serialized results
#         del getData_work["_id"]
#         serialized_results_work = json.dumps(getData_work, sort_keys=True,indent=4, separators=(',', ': '))
#         json_result_work = json.loads(serialized_results_work) 
#          
#         #build rest response to client
#         position = json_result_work['work']['data'][0]['work'][0]['employer']['name']
#         fb_id = json_result_work['fb_id_work']
#         rest_work = {"fb_id" : fb_id, "position" : position}
         
#         #--------------------------------------------#
#         
#         response2 = http_client.fetch(tv)
#         json_acceptable_string = response2.body.replace("'", "\"")
#         data = json.loads(json_acceptable_string)
#         db.dannysaban2.insert({"fb_id_tv":User_id, "tv":data})
#         getData_tv = db.dannysaban2.find_one({"fb_id_tv":User_id})
#         
#         
#         
#         #--------------------------------------------#
#         response3 = http_client.fetch(movies)
#         json_acceptable_string = response3.body.replace("'", "\"")
#         data = json.loads(json_acceptable_string)
#         db.dannysaban2.insert({"fb_id_movies":User_id, "movies":data})
#         getData_movies = db.dannysaban2.find_one({"fb_id_movies":User_id})
#         
#         
#         
#         #--------------------------------------------#
#         response4 = http_client.fetch(music)
#         json_acceptable_string = response4.body.replace("'", "\"")
#         data = json.loads(json_acceptable_string)
#         db.dannysaban2.insert({"fb_id_music":User_id, "music":data})
#         getData_music = db.dannysaban2.find_one({"fb_id_music":User_id})
#         
#         
#         
#         #create response list         
#         setResponse = [rest_me, rest_work]
# 
#         
        #exe response
        self.write(rest_me)
        # close connection           
        self.finish()
                
        
        
        
        

# class Application(tornado.web.Application):
#     def __init__(self):
#         #handlers = []
#                     (r'/', UserInit)
#                     #(r'/userInit/', LoginHandler)
#                     #(r'/auth/logout', LogoutHandler)
#                     
       
        
application = tornado.web.Application([
    #(r"/wakeup", Wakeup),
    #(r"/userInit1", GetGlobals),   
    (r"/userInit/(.*)", UserInit),
    #(r"/register", Register), 
    #(r"/getUser/(.*)", GetUser),
    #(r"/tempUser/(.*)", TempUser),
    #(r"/register/(.*)", Register),
    
    
    #(r".*", FallbackHandler, dict(fallback=tr)),
])

if __name__ == '__main__':
    tornado.options.parse_command_line()
    logging.info("starting torando web server")
    #app = Application()
    application.listen(8001)
    tornado.ioloop.IOLoop.instance().start()


