$env:PYTHONPATH = "C:\Users\Fluffy\PycharmProjects\stinkefurz\src"

Start-Process -FilePath "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" `
              -ArgumentList "--background", "--python", "C:\Users\Fluffy\PycharmProjects\stinkefurz\src\main.py" `
              -NoNewWindow -Wait
