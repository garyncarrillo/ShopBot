# 01: Create the pyton virtual enviroment in linux - wsl
python3 -m venv venv

# 02: Activate the virtual enviroment in linux - wsl
source venv/bin/activate

# 03: Install the project requirements in linux - wsl
pip install -r requirements.txt

# 04: Run the uvicorn server in linux - wsl
uvicorn shopbot.main:app --reload

# 05: Open the project documentation in the browser
localhost:8000/docs
