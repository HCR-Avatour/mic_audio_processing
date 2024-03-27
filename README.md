This README includes the instructions for setting up and tuning the microphone array. Start by copying this folder to your directory.

DOA.py is used to check the audio input angle into the microphone, printing Mic_tuning.direction which gives 45 to 135 degrees or OFF if outside this range.

tuning.py contains the list of parameters and the variables they correspond to for tuning the noise suppression system. 

setdefaults.py sets the tuned parameters to apply to the microphone.

record.py includes the function for processing the received DOA variable, as well as recording and processing directional noise.
