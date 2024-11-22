A simple pastebin style python server that lets you write over http without authentication.

![demo of how it looks]((https://github.com/deekaph/lanbin/blob/main/lanbin2.png?raw=true))

I wanted something like Pastebin for quick sharing between my various devices - my phone, a guest's laptop, my desktop, the kitchen computer.

You'll obviously need to have a python environment to run this.

It goes without saying but I need to really underline that there is NO AUTHENTICATION, that's kind of the idea, quick and dirty to share links and stuff back and forth without having to create user accounts and permissions.

Furthermore, it includes file upload functionality,

and

__would be trivial to exploit this for arbitrary code execution.__

-=-=-=-

It will accept any file type. Size of the drive is the only limitation I think? I haven't tried sending ISO's over the wire yet, I mainly wanted to quickly share a pic that I had on one laptop over to another laptop on the LAN.

Links that are pasted are clickable without further effort.

HOW TO USE:
Download all the files and extract them to a directory. You'll need the subdirectory templates/ include the html files there.

It depends on flask and a few other things.

Usage:
~# python3 lanbin.py

![executing the python code]((https://github.com/deekaph/lanbin/blob/main/lanbin1.png?raw=true))

If you try to run it and it's missing moduels, then install them with pip:

~# pip install flask

Your local IP:5000 ... it also tells you in the propmpt.
