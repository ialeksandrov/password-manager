# password-manager

This simple cli tool has two abilities at the moment:
- generate password with custom length (provided by the user).
- show list of all saved passwords.
- Remove old passwords.
- Add custom passwords.

Future ideas:
- ~~List all saved passwords.~~ -> Done
- ~~Show last saved password.~~ -> Done
- ~~Remove old passwords ( passwords you don`t want to use anymore.)~~ -> Done
- ~~Add the ability the user to add custom password to saved passwords.~~ -> Done
- Probably develop GUI version with tkinter or pyQT.(or both, or some modern gui framework.)
- ~~Add hashing using Argon2 algorithm.~~
- ~~Think for a way to improve password generation.(better way)~~
- ~~Think for a way to improve password storing.(better way)~~ - use DB SQL lite - Done
- Write unit tests.

CLI HELP:
```
$ python password_manager.py -h
usage: Password Manager [-h] [--title TITLE] [--username USERNAME] [--password PASSWORD] {add,list,update,delete}

Managing passwords and users

positional arguments:
  {add,list,update,delete}
                        Actions to perform

options:
  -h, --help            show this help message and exit
  --title TITLE         Title of the password entry
  --username USERNAME   Username for the password entry
  --password PASSWORD   Password for the entry
```

Sample usage:
```
$ python password_manager.py add --title 'os creds' --username 'pesho' --password 'jijiplqktor'
```

```
$ python password_manager.py update --title 'os creds' --username 'pesho' --password '123456'
```

```
$ python password_manager.py verify --title "test" --username "test123" --password "password123"
Password is correct
```

```
$ python password_manager.py delete --title 'os creds'
```

```
$ python password_manager.py generate --length 20
````
