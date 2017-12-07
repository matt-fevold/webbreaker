#!/bin/sh
# pyinstaller --clean -y --windowed webbreaker.spec
# --paths /Library/Python/2.7/site-packages
# hdiutil create ./webbreaker.dmg -srcfolder webbreaker.app -ov
# pyinstaller --clean -y --onefile --dist $(pwd)/dist --name webbreaker-cli $(pwd)/webbreaker/__main__.py 

try 
{
        $pip = get-command pip
}
catch 
{
        throw "Please Install pip or update your PATH "
}

try 
{
        $pyinstaller = get-command pyinstaller
}
catch 
{
        Write-Host "Installing pyinstaller"
        pip install pyinstaller
}


try
{
        $python = get-command python.exe
        if (test-path setup.py) 
        {
                #pip install pyOpenSSL
                #python setup.py build
                pip install -r requirements.txt
                python setup.py install
                pyinstaller.exe --clean -y --onefile --distpath $pwd\dist --name webbreaker $pwd\webbreaker\__main__.py 
        }
        else 
        {
                Write-Host "You are not in the root directory of webbreaker where setup.py is located!"
        }
}
catch 
{
        throw "Please install Python 2.7 or higher"
}

