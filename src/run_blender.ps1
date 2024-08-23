$env:PYTHONPATH = {absolute path to src folder}

Start-Process -FilePath {absolute path to blender.exe (blender 4.0.2)} `
              -ArgumentList "--background", "--python", {absolute path to main.py (in src)} `
              -NoNewWindow -Wait
