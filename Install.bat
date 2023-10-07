@echo off
git clone https://github.com/enescakircali/Dubbing-Gui.git
%cd ./Dubbing-Gui
pip install -r requirements.txt
pip uninstall torch torchvision torchaudio -y
pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu117
echo INFO: The download is complete. Don't panic, this bat file will be deleted and the interface will open. press any key to continue.
pause
start go-web.bat
del %0