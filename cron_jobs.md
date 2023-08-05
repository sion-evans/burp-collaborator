```
* * * * * /usr/bin/python3 /root/collab.py >> /root/collab_script_output.txt 2>&1
* * * * * /usr/bin/journalctl -u collaborator --since "1 hour ago" > /root/collaborator_output.txt 2>&1
```
