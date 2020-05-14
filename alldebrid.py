import requests

class Client():#TODO Centralize requests to implement rate limits

    def __init__(self,app_name,api_key):
        self.base_url = self.authenticate(app_name,api_key)

    def authenticate(self, app_name, api_key):
        base_url = "?agent={}&apikey={}".format(app_name, api_key)
        response=requests.get("http://api.alldebrid.com/v4/user"+base_url)
        if response.json()["status"] != "success": raise Exception(response.json().get('error'))
        return base_url

    def debrid_link(self,link):
        return Link(self.base_url,link)

class Link():
    def __init__(self,base_url,link):
        self.link = link
        self.base_url=base_url
    
    def send_request(self):
        response=requests.get("https://api.alldebrid.com/v4/link/unlock{}&link={}".format(self.base_url,self.link))
        if response.json()["status"] != "success": raise Exception(response.json().get('error'))
        json_data = response.json()["data"]
        if "delayed" in json_data.keys():
            self.delayed=True
            self.delayed_id=json_data["delayed"]
        else:
            self.delayed=False
            self.link=json_data["link"]
            return json_data["link"]

    def status(self):#Return time left
        if self.delayed_id is None: return None
        response=requests.get("https://api.alldebrid.com/v4/link/delayed{}&id={}".format(self.base_url,self.delayed_id))
        if response.json()["status"] != "success": raise Exception(response.json().get('error'))
        if response.json()["data"]["time_left"]==0: self.dl_link_data=response.json()["data"]["link"]
        return response.json()["data"]["time_left"]

    @property
    def dl_link(self):
        if self.dl_link_data is not None: return self.dl_link_data
        if self.status()==0: return self.dl_link_data
        
#TODO Magnet