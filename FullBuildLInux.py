import subprocess
import os
import requests

print("Attempting to build Godot Engine...")
completedProc = subprocess.run('scons p=linuxbsd target=editor precision=double module_mono_enabled=yes production=yes', shell=True, capture_output=True, text=True)
if completedProc.returncode != 0:
    print("Error building Godot Engine!")
    print(completedProc.stderr)
else:
    print("Successfully built Godot Engine!")


print("Generating Godot C# Glue...")
completedProc = subprocess.run('./bin/godot.linuxbsd.editor.double.x86_64.mono --headless --generate-mono-glue modules/mono/glue', shell=True, capture_output=True, text=True)
if completedProc.returncode != 0:
    print("Error generating Godot C# Glue!")
    print(completedProc.stderr)
    exit
else:
    print("Successfully generated Godot C# Glue!")


print("Building DotNet assemblies and pushing to local NuGet source...")
completedProc = subprocess.run('python3 ./modules/mono/build_scripts/build_assemblies.py --godot-output-dir=./bin --precision=double --push-nupkgs-local ~/MyLocalNugetSource', shell=True, capture_output=True, text=True)
if completedProc.returncode != 0:
    print("Error generating DotNet assemblies!")
    print(completedProc.stderr)
    exit
else:
    print("Successfully generated DotNet assemblies and pushed to local NuGet source!")



print("Building Godot DEBUG template...")
completedProc = subprocess.run('scons p=linuxbsd module_mono_enabled=yes production=yes precision=double target=template_debug', shell=True, capture_output=True, text=True)
if completedProc.returncode != 0:
    print("Error building DEBUG template!")
    print(completedProc.stderr)
    exit
else:
    print("Successfully built DEBUG template!")



print("Building Godot RELEASE template...")
completedProc = subprocess.run('scons p=linuxbsd module_mono_enabled=yes precision=double production=yes target=template_release', shell=True, capture_output=True, text=True)
if completedProc.returncode != 0:
    print("Error building RELEASE template!")
    print(completedProc.stderr)
    exit
else:
    print("Successfully built RELEASE template!")

ntfy_token_path = "ntfy_token"
if os.path.exists(ntfy_token_path):
    print("Found ntfy token...")
    file = open(ntfy_token_path, "r")
    ntfy_token = file.readlines()
    file.close()
    requests.post(ntfy_token[0].strip(),
        data="Godot Engine was successfully built! ✔️".encode(encoding='utf-8'),
        headers={
            "Title": "Godot Build Completed!",
            "Priority": "high",
            "Tags": "warning",
            "Authorization": "Bearer " + ntfy_token[1].strip()
        })
