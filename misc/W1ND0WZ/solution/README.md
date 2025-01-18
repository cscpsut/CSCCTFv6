# W1ND0WZ
1. First, you need to identify what parts of the code might be vulenrable or exploitable. As a rule of thumb in PyJails, any use of `eval` or `exec` is a red flag. 

2. In the provided code, the user is prompted for input, which is then passed to the `break_` function if it passeds the input check. The `break_` function uses `exec` to execute a hardcoded print statement. Your first instinct might be to exploit the initial eval, which could be possible using a complex payload, but the `break_` function is the real target.

3. The break function takes as parameters any number of `*args` and `**kwargs`. A little bit of reading will tell you that:
- *args allows a function to accept any number of positional arguments as a tuple.
- **kwargs allows a function to accept any number of keyword arguments as a dictionary.

4. The first part of the `break_` function loops over the `*args`, and for each one, initialized a random 30 character variable where the flag is stored. Unfortunately for you, nothing about this part of the code is exploitable, as you can't guess the variable name or print it, or even print the locals. (At least not that I know of)

5. The second part of the `break_` loops over the `**kwargs` and updates the local variables with the key-value pairs. Bear in mind that this is followed directly by the `exec` statement. This means that you can overwrite the `print` function to allow you to print the flag. The payload would be in the format `print=lambda: NEW PRINT HERE`.

Intended solution:
```python
print=lambda x: print(*open('fla''g.txt'))
```
