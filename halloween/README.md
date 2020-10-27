Halloween Sound Effects

# Setup

1. Setup cron job to run for the user on startup.  Don't setup as sudo or audio will not work.

```
$ crontab -e

@reboot python3 /home/pi/projects/halloween/script.py &
```



