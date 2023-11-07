# git App

- This app  shows a overview of pull requests with labels for a  repository.
- This app is built using relflex python framework and github api.



# Installation
1. clone the repository 
  ```bash```
  
git clone ashish111333/hacktoberfest 

2. go to project directory 
  ```bash```

cd hacktoberfest/submissions/data_Visualizations/ashish_git_App

3. create virtual enviroment in current directory and activate it

 ```bash```
 python3 -m venv venv
 source venv/bin/activate
 
 


4. Install dependencies and intialize virtual env with "reflex init"
 ```bash```
 cd venv
 pip install reflex
 pip install requests
 reflex init

5. copy git app files to venv
 ```bash```
 cd ..
 cat git_app/git_app.py > venv/venv/venv.py
 rm venv/venv/state.py
 cp state.py venv/
 
 
 
 

6. run the App
 ```bash```
 cd venv
 reflex run






 


 


