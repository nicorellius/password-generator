# password-generator

`PyPass3`

Dice Roll Optional, Mostly-Random Word, Number, and Mixed Password Generator

Thanks to EFF for their short and long word lists:

https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases

Currently, this password generator can make mixed passwords, numeric-only passwords, and multi-word passphrases. The passwords (non-words type), use the [random.org]() system to generate mostly random strings.

For RDO Client, I had to edit `rdoclient.py` line 33 to this:

`from queue import Queue, Empty`

for Python 3 compatibility.