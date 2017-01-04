# eyephish

I saw a talk at hushcon about the problem of IDN domains and punycode
domains and the difficulty of covering every possible base.. I dont
really remember, but I liked the idea of trying to solve this analog
problem a bit with code and heres the PoC I wrote.<br>

The idea is pretty simple, the problem with IDN characters is that
some characters may _look_ similar to other caracters so OpenCV seemed the 
natural solution to brute force possible lookalike options using different
alphabets and fonts, creates a score for how well each character matches
the targets and displays them cutoff by the threshold.<br>
<br>
<br>
<br>
>$ python eyephish.py  --inputstring "amazon" --dialect=greek<br>
>*amazon ['a', 'm', 'a', 'z', 'o', 'n']<br>
>>    οη [' ', ' ', ' ', ' ', u'\u03bf', u'\u03b7']<br>
>>    όή [' ', ' ', ' ', ' ', u'\u03cc', u'\u03ae']<br>
>>    ϙ  [' ', ' ', ' ', ' ', u'\u03d9', ' ']<br>
>>    σ  [' ', ' ', ' ', ' ', u'\u03c3', ' ']<br>
>>    ρ  [' ', ' ', ' ', ' ', u'\u03c1', ' ']<br>
>>    ͻ  [' ', ' ', ' ', ' ', u'\u037b', ' ']<br>
>>    ͽ  [' ', ' ', ' ', ' ', u'\u037d', ' ']<br>
>>    ϱ  [' ', ' ', ' ', ' ', u'\u03f1', ' ']<br>
>>    ϼ  [' ', ' ', ' ', ' ', u'\u03fc', ' ']<br>
<br>
>$ python eyephish.py  --inputstring "microsoft" --dialect=cyrillic  <br>
>*microsoft ['m', 'i', 'c', 'r', 'o', 's', 'o', 'f', 't']<br>
>> ісѓоѕоӏӏ [' ', u'\u0456', u'\u0441', u'\u0453', u'\u043e', u'\u0455', u'\u043e', u'\u04cf', u'\u04cf']<br>
>> ӏҫґӧзӧӀӀ [' ', u'\u04cf', u'\u04ab', u'\u0491', u'\u04e7', u'\u0437', u'\u04e7', u'\u04c0', u'\u04c0']<br>
>> Ӏҁ ө өІІ [' ', u'\u04c0', u'\u0481', ' ', u'\u04e9', ' ', u'\u04e9', u'\u0406', u'\u0406']<br>
>> Іє ӫ ӫгг [' ', u'\u0406', u'\u0454', ' ', u'\u04eb', ' ', u'\u04eb', u'\u0433', u'\u0433']<br>
>> ї  е етт [' ', u'\u0457', ' ', ' ', u'\u0435', ' ', u'\u0435', u'\u0442', u'\u0442']<br>
>> Ї  р ріЇ [' ', u'\u0407', ' ', ' ', u'\u0440', ' ', u'\u0440', u'\u0456', u'\u0407']<br>
>> г  б бЇі [' ', u'\u0433', ' ', ' ', u'\u0431', ' ', u'\u0431', u'\u0407', u'\u0456']<br>
>> т  ё ёїӷ [' ', u'\u0442', ' ', ' ', u'\u0451', ' ', u'\u0451', u'\u0457', u'\u04f7']<br>
>> ғ  ѐ ѐТҭ [' ', u'\u0493', ' ', ' ', u'\u0450', ' ', u'\u0450', u'\u0422', u'\u04ad']<br>
>> ӷ  ҏ ҏ ї [' ', u'\u04f7', ' ', ' ', u'\u048f', ' ', u'\u048f', ' ', u'\u0457']<br>
>> Т        [' ', u'\u0422', ' ', ' ', ' ', ' ', ' ', ' ', ' ']<br>
>> ҭ        [' ', u'\u04ad', ' ', ' ', ' ', ' ', ' ', ' ', ' ']<br>
<br>
>$ python eyephish.py  --inputstring "ebay" --dialect=cyrillic  <br>
>*ebay ['e', 'b', 'a', 'y']<br>
>>ерау [u'\u0435', u'\u0440', u'\u0430', u'\u0443']<br>
>>ёо ӱ [u'\u0451', u'\u043e', ' ', u'\u04f1']<br>
>>ѐҏ ӳ [u'\u0450', u'\u048f', ' ', u'\u04f3']<br>
>>өӧ ӯ [u'\u04e9', u'\u04e7', ' ', u'\u04ef']<br>
>>ӫ  ў [u'\u04eb', ' ', ' ', u'\u045e']<br>
>>ӗ    [u'\u04d7', ' ', ' ', ' ']<br>
>>о    [u'\u043e', ' ', ' ', ' ']<br>
>>ӧ    [u'\u04e7', ' ', ' ', ' ']<br>
<br>
Its also worth mentioning that it can do this trick without resorting to a foreign alphabet as well<br>
<br>
$ python eyephish.py --inputstring "microsoft" --dialect=latin*microsoft ['m', 'i', 'c', 'r', 'o', 's', 'o', 'f', 't']
>microsoft [u'm', u'i', u'c', u'r', u'o', u's', u'o', u'f', u't']
> l  e etf [' ', u'l', ' ', ' ', u'e', ' ', u'e', u't', u'f']
> I  b bll [' ', u'I', ' ', ' ', u'b', ' ', u'b', u'l', u'l']
> !  p pII [' ', u'!', ' ', ' ', u'p', ' ', u'p', u'I', u'I']
> |     !! [' ', u'|', ' ', ' ', ' ', ' ', ' ', u'!', u'!']
> :     ii [' ', u':', ' ', ' ', ' ', ' ', ' ', u'i', u'i']
> f     || [' ', u'f', ' ', ' ', ' ', ' ', ' ', u'|', u'|']
> t     [  [' ', u't', ' ', ' ', ' ', ' ', ' ', u'[', ' ']
> +     T  [' ', u'+', ' ', ' ', ' ', ' ', ' ', u'T', ' ']
> [        [' ', u'[', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
> .        [' ', u'.', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
> ;        [' ', u';', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

<br>
<br>
This script depends on OpenCV and PIL modules<br>
<br>
todo: adding two character brute forcing since vv->w.. which opened up more complicated problems then im interested in solvoing for now.<br>
