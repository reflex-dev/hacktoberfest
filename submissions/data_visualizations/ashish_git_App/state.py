import reflex as rx
import requests
from typing import List,Dict

class app_state(rx.State):
    
    token :str
    repo_name :str
    user_name :str
    data :List[dict]=[]
    state: str
    page: int =1
   
    
    def filter(self,value: str):
        values=["only merged prs","assigned prs","closed prs","open prs","approved prs"]
        keys=["merged","assigned","closed","open","is_approved"]
        key_to_search=keys[values.index(value)]
        new_data :List[dict]=[]
        
        if key_to_search=="closed":
            for pull_data in self.data:
                if pull_data['status']=="closed":
                    new_data.append(pull_data)
                
                
                        
                
        elif key_to_search=="open":
            for pull_data in self.data:
                if pull_data['status']=="open":
                    new_data.append(pull_data)
        
        else:
            for pull_data in self.data:
                if pull_data[key_to_search]==True:
                    new_data.append(pull_data)
                    
                    
        self.data=new_data
        
        
        
        
    
    
    
    def check_if_pr_is_merged(self,pr :dict):
        
        response=requests.get(f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/pulls/{pr['number']}",headers={"Authorization":f"Bearer {self.token}"})        
        pull_req_data=response.json()
        if pull_req_data.get("merged")==True:
            return True
        
        return False
            
            
        
        
        
    
    def assigned(self,pr : dict):
        if pr.get("assignees"):
            if len(pr["assignees"])!=0:
                return True
        return False
    
    
    
    def state_of_pr(self,pr :dict):
        if pr.get("state")=="open":
            return True
        else:
            return False
        
    
    def reviewers(self,pr :dict):
        if pr.get("requested_reviewrs"):
            return pr['requested_reviewers']
        
        return []
    
    def reviewers_who_approved(self,pull: Dict[str,str]):
        
        reviewers=[]
        
        reviewers_=None
       
        response=requests.get(url=f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/pulls/{pull['number']}/reviews",headers={"Authorization":f"Bearer {self.token}",})
        reviewers_=response.json()
            
        for reviewer in reviewers_:
            if reviewer.get('state')=="APPROVED":
                reviewers.append(reviewer)
                    
        
        return reviewers
    
    def return_pull_data(self,pulls :List[dict]):
        pull_data_list=[]
        for pull in pulls:
                
                tem_={}
                approved_by=self.reviewers_who_approved(pull)
                if self.assigned(pull):
                    tem_["assigned"]=True
                    tem_["assignees"]=pull["assignees"]
                else:
                    tem_["assigned"]=False
                    tem_["assignees"]=[]
                if self.state_of_pr(pull):
                    tem_['status']="open"
                else:
                    tem_['status']="closed"
            
                if len(approved_by)>0:
                    tem_["is_approved"]=True
                else:
                    tem_["is_approved"]=False
    
                if self.check_if_pr_is_merged(pull):
                    tem_["merged"]=True
                else:
                    False
                tem_["approved_by"]=approved_by
                tem_["link"]=pull.get("html_url")
                tem_["title"]=pull.get("title")
                tem_["pull_no"]=pull.get("number")
                tem_["avatar_url"]=pull["user"]["avatar_url"]
                tem_["author"]=pull["user"]["login"]
                tem_["created_at"]=pull["created_at"]
                pull_data_list.append(tem_)
            
        return pull_data_list
        
        
           
    
            
    def return_pull_request_info(self):
        
        header={"Authorization":f"Bearer {self.token}"}
        param={"state":"all","per_page":10,"page":{self.page}}
        
        response=None
        if len(self.data)==0:
            response=requests.get(url=f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/pulls",headers=header,params=param)
            if response.status_code!=200:
                print("request failed")
            else:
                print("request successfull")
            pulls_=response.json()
            pulls_data=self.return_pull_data(pulls_)
            self.data.extend(pulls_data)
            self.page+=1
            
        response=requests.get(url=f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/pulls",headers=header,params=param)
        pulls_=response.json()
        pulls_data=self.return_pull_data(pulls_)
        self.data.extend(pulls_data)
        self.page+=1
        
    
        
        
        
            
        
        
            
            
            
            
            
        
            
            
            
            
            
        
            
        
        
        
        


        
        

            
            
        
            
            
            
        
    
        
    
        
        
        
        
        
    
    
    
