# eyephish

I saw a talk at hushcon about the problem of IDN domains and punycode
domains and the difficulty of covering every possible base.. I dont
really remember, but I liked the idea of trying to solve this analog
problem a bit with code and heres the PoC I wrote.

The idea is pretty simple, the problem with IDN characters is that
some characters may _look_ similar to other caracters so OpenCV seemed the 
natural solution to brute force possible lookalike options using different
alphabets and fonts, creates a score for how well each character matches
the targets and displays them cutoff by the threshold.



$ python eyephish.py  --inputstring "amazon" --dialect=greek
*amazon ['a', 'm', 'a', 'z', 'o', 'n']
>    οη [' ', ' ', ' ', ' ', u'\u03bf', u'\u03b7']
>    όή [' ', ' ', ' ', ' ', u'\u03cc', u'\u03ae']
>    ϙ  [' ', ' ', ' ', ' ', u'\u03d9', ' ']
>    σ  [' ', ' ', ' ', ' ', u'\u03c3', ' ']
>    ρ  [' ', ' ', ' ', ' ', u'\u03c1', ' ']
>    ͻ  [' ', ' ', ' ', ' ', u'\u037b', ' ']
>    ͽ  [' ', ' ', ' ', ' ', u'\u037d', ' ']
>    ϱ  [' ', ' ', ' ', ' ', u'\u03f1', ' ']
>    ϼ  [' ', ' ', ' ', ' ', u'\u03fc', ' ']


$ python eyephish.py  --inputstring "microsoft" --dialect=cyrillic  
*microsoft ['m', 'i', 'c', 'r', 'o', 's', 'o', 'f', 't']
> ісѓоѕоӏӏ [' ', u'\u0456', u'\u0441', u'\u0453', u'\u043e', u'\u0455', u'\u043e', u'\u04cf', u'\u04cf']
> ӏҫґӧзӧӀӀ [' ', u'\u04cf', u'\u04ab', u'\u0491', u'\u04e7', u'\u0437', u'\u04e7', u'\u04c0', u'\u04c0']
> Ӏҁ ө өІІ [' ', u'\u04c0', u'\u0481', ' ', u'\u04e9', ' ', u'\u04e9', u'\u0406', u'\u0406']
> Іє ӫ ӫгг [' ', u'\u0406', u'\u0454', ' ', u'\u04eb', ' ', u'\u04eb', u'\u0433', u'\u0433']
> ї  е етт [' ', u'\u0457', ' ', ' ', u'\u0435', ' ', u'\u0435', u'\u0442', u'\u0442']
> Ї  р ріЇ [' ', u'\u0407', ' ', ' ', u'\u0440', ' ', u'\u0440', u'\u0456', u'\u0407']
> г  б бЇі [' ', u'\u0433', ' ', ' ', u'\u0431', ' ', u'\u0431', u'\u0407', u'\u0456']
> т  ё ёїӷ [' ', u'\u0442', ' ', ' ', u'\u0451', ' ', u'\u0451', u'\u0457', u'\u04f7']
> ғ  ѐ ѐТҭ [' ', u'\u0493', ' ', ' ', u'\u0450', ' ', u'\u0450', u'\u0422', u'\u04ad']
> ӷ  ҏ ҏ ї [' ', u'\u04f7', ' ', ' ', u'\u048f', ' ', u'\u048f', ' ', u'\u0457']
> Т        [' ', u'\u0422', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
> ҭ        [' ', u'\u04ad', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

$ python eyephish.py  --inputstring "ebay" --dialect=cyrillic  
*ebay ['e', 'b', 'a', 'y']
>ерау [u'\u0435', u'\u0440', u'\u0430', u'\u0443']
>ёо ӱ [u'\u0451', u'\u043e', ' ', u'\u04f1']
>ѐҏ ӳ [u'\u0450', u'\u048f', ' ', u'\u04f3']
>өӧ ӯ [u'\u04e9', u'\u04e7', ' ', u'\u04ef']
>ӫ  ў [u'\u04eb', ' ', ' ', u'\u045e']
>ӗ    [u'\u04d7', ' ', ' ', ' ']
>о    [u'\u043e', ' ', ' ', ' ']
>ӧ    [u'\u04e7', ' ', ' ', ' ']

todo: adding two character brute forcing since vv->w.. which opened up more complicated problems
then im interested in solvoing for now.
