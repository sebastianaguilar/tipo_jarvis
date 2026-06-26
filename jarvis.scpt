tell application "Terminal"
	reopen
	activate
	#do script ("say -v Paulina -r 185  Ejecutando") in window 1
	#activate
	#set currentTab to do script ("cd Proyectos/GPT4")
	do script ("cd /Users/sebastianaguilar/Proyectos/GPT4") in window 1
	do script ("say -v Paulina -r 185  Ejecutando sistema Jarvis") in window 1
	delay 3
	do script ("python3 vision.py") in window 1
	delay 2
	do script ("Despierta Jarvis necesito tu ayuda") in window 1
	#delay 8
	tell application "VideoJar"
		activate
	end tell
end tell
tell application "System Events"
	#key code 96
end tell
