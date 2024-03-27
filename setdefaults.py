import subprocess

def set_mic_parameters():
    commands = [
        "python tuning.py FREEZEONOFF 0",
        "python tuning.py HPFONOFF 2",
        "python tuning.py CNIONOFF 0",
        "python tuning.py GAMMA_NS 2",
        "python tuning.py GAMMA_NN 2",
        "python tuning.py MIN_NS 0.9",
        "python tuning.py MIN_NN 0.9",
    ]

    for cmd in commands:
        subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    set_mic_parameters()
