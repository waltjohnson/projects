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



