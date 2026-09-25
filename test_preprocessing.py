from preprocessing import preprocess_text

#Test sentences
samples = [
"WIFI is not working in the MCA lab!!!",
"There is Water leakage near Classroom.",
"Projector is Not working..",
"Hello , GOOD morning!!",
"INTERNET speed is very slow      ",
"FAN is making noise !!"
]

print("-----testing preprocessing-----\n")
for s in samples:
	cleaned=preprocess_text(s)
	print("Original:",s)
	print("Cleaned:",cleaned)
	print("-"*50)
