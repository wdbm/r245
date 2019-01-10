# R2-45

![](https://raw.githubusercontent.com/wdbm/r245/master/media/r245.png)

R2-45 monitors overall volatile memory usage and when memory usage goes to or beyond what it considers too far (meaning that the poor system switches to super-slow swap memory) it kills progressively a list of programs it has in its internal blacklist. As it does this it notifies you of its actions and, when it has done all it can based on its blacklist, it sends a final message of warning. It is not perfect, but it is trying. And really, the pursuit of a positive contribution to reality is really all for which anyone or script can hope.

# setup

```Bash
pip install r245
```

# usage

Just run it.

```Bash
r245
```

You can ask it for help if you want to learn how to specify via command line options and arguments the critical RAM usage limit or a custom blacklist.

```Bash
r245 --help
```

# example program to demonstrate large memory usage

```Python
x = bytearray(512000000)
```

# background reading

- <https://wikileaks.org/wiki/Scientology_cult_recording:_R2-45_is_the_act_of_shooting_a_person_with_a_firearm,_20_Nov_1959>
