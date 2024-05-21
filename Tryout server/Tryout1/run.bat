powershell -noexit -command ^
.\env\Scripts\activate.ps1;^
pip install -r .\env\requirements.txt;^
python app.py