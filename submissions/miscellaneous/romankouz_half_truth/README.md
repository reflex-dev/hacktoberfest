# Welcome to 50/50!

This game tests your ability to discern true statements about any subjects from the fake ones.

The exact rules can be found in the "Rules" tab of our game page and the game can be customized to your liking on the "Settings" tab of the game page.

The objective is to identify all true statements without selecting any false statements, so be careful and trust (or don't trust) your instincts!

# To Play!

1. Clone the repository
```bash
git clone https://github.com/romankouz/hacktoberfest.git
```

2. Navigate to the project directory
```bash
cd hacktoberfest/submissions/miscellaneous/romankouz_half_truth
``` 

3. Make virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate
```

4. Install the dependencies
```bash
pip install reflex
reflex init
pip install -r requirements.txt
```

5. Add your OpenAI Key to the appropriate line in ```round.py```.

```openai.api_key = "YOUR KEY HERE"```

6. Feel free to change the ```MODEL_VERSION``` as well, however, GPT-4 is recommended for maximum entertainment and accuracy.

7. Run the app
```bash
reflex init
reflex run
```