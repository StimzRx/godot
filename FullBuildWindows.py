import subprocess
import os
import requests

print("Attempting to build Godot Engine...")
completedProc = subprocess.run('scons p=windows module_mono_enabled=yes production=yes build_csharp=yes')
if completedProc.returncode != 0:
    print("Error building Godot Engine!")
    print(completedProc.stderr)
else:
    print("Successfully built Godot Engine!")


print("Generating Godot C# Glue...")
completedProc = subprocess.run('./bin/godot.windows.editor.x86_64.mono.exe --headless --generate-mono-glue modules/mono/glue')
if completedProc.returncode != 0:
    print("Error generating Godot C# Glue!")
    print(completedProc.stderr)
else:
    print("Successfully generated Godot C# Glue!")


print("Building DotNet assemblies and pushing to local NuGet source...")
completedProc = subprocess.run('python ./modules/mono/build_scripts/build_assemblies.py --godot-output-dir=./bin --push-nupkgs-local C:/Users/%USERNAME%/MyLocalNugetSource')
if completedProc.returncode != 0:
    print("Error generating DotNet assemblies!")
    print(completedProc.stderr)
else:
    print("Successfully generated DotNet assemblies and pushed to local NuGet source!")



print("Building Godot DEBUG template...")
completedProc = subprocess.run('scons p=windows module_mono_enabled=yes production=yes build_csharp=yes target=template_debug')
if completedProc.returncode != 0:
    print("Error building DEBUG template!")
    print(completedProc.stderr)
else:
    print("Successfully built DEBUG template!")



print("Building Godot RELEASE template...")
completedProc = subprocess.run('scons p=windows module_mono_enabled=yes production=yes build_csharp=yes target=template_release')
if completedProc.returncode != 0:
    print("Error building RELEASE template!")
    print(completedProc.stderr)
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
