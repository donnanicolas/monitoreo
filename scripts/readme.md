# Scripts for KILL and RENICE

These two commands have permissions problems:

* **renice**: Can only reduce the priority of a process (greater number) and not increase it
* **kill**: Can only kill process owned by the user

A solution is the creation of scripts that have some sort of security and allow them to run with `sudo` without password by editing **/etc/sudoers** and adding
```
<server-user> ALL= NOPASSWD:/path/to/scripts/script-name.sh
```
And then run them within the app with `sudo`.

The password is hashed to avoid any user from reading it. To avoid changes to this scripts they should only be allowed to be written by the **root**.

The recommended settings are **500** (for chmod) and the running user should be the owner.

The password hashed in the files is **testpasswd**

## renice

The scripts takes 3 arguments: **pass**, **priority** and **pid**

### Example
```
sudo /path/to/script/sudo_renice.sh passwd -10 7300
```

If the password is correct it will set the priority regardless the value.

## kill

The scripts takes 2 arguments: **pass** and **pid**

### Example
```
sudo /path/to/script/sudo_kill.sh passwd 7300
```

This scripts also checks the password, but it will not run if the process is owned by the **root**
