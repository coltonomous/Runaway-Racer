import cx_Freeze

executables = [cx_Freeze.Executable("Runaway_Racer.py")]

cx_Freeze.setup(
    name = "Runaway Racer",
    options = {"build.exe": {"packages": ["pygame"],
                             "include_files": ["car_icon.png", "car_sprite.png", "crash.wav", "racecar_track.wav", "RaceFlags.png", "fixedsys.ttf"]}},
    executables = executables
)
