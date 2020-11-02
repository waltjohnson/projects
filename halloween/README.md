Halloween Sound Effects

# Setup 

1. Setup cron job to run for the user on startup.  Don't do this as sudo as it will attempt to run as root and the audio will not work.
```
$ crontab -e

@reboot /home/pi/projects/halloween/start.py
```

2. On Raspberry Pi, set default audio to 3.5mm audio jack.
```
$ raspi-config

Force audio to 3.5 jack
```

3. On Raspberry Pi, uncomment and set `hdmi_force_hotplug=1` in `/boot/config.txt` to pretend HDMI hotplug signal is asserted so it appears HDMI display is attached.  Uses HDMI mode even though no monitor is attached.  This is necessary to enable audio, otherwise we get no sound.
```
$ sudo vi /boot/config

hdmi_force_hotplug=1
```


# ToDo's (- do, + done)
- Ensure fast GPIO input events get caught by either changing GPIO input sampling to external interrupt or reduce sample rate from 0.2 to 0.01 seconds and add I/O debounce. 
- Add fog machine to GPIO output.


