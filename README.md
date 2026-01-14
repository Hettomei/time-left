# install

python > 3.10

```
python -m pip install -r requirements.txt
```

# test

```
python -m pytest
```

# launch

```
python main.py
```

output : 

```
debut : 8 30
fin   : 12 06

08h30 - 12h06  3:36:00   3:36:00

debut : 13 20
fin   : 17

08h30 - 12h06  3:36:00   3:36:00
13h20 - 17h00  3:40:00   7:16:00

debut : 18h03
fin   : 19

08h30 - 12h06  3:36:00   3:36:00
13h20 - 17h00  3:40:00   7:16:00
18h03 - 19h00  0:57:00   8:13:00
```

# Alias for everyday use

```
alias chrono="python ~/programmes/time-left/main.py -a './chiffrages.md'"
```
