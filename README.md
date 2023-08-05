This tool is generally designed to flow as the following:

1. A private Burp Collaborator instance is functioning as intended with its configuration's logLevel set to DEBUG.
2. *collaborator_output.txt* is populated from *journalctl* output, containing all interactions from when the instance was started.
3. *collab.py* parses *collaborator_output.txt* -
    1. Populating an SQLite database (*collaborator.db*) with all interactions detected.
    2. Utilising Telegram's sendMessage API to notify the user of any new interactions.

I've included the examples I have used when writing this, see *cron_jobs.md* and *burp.config*.
