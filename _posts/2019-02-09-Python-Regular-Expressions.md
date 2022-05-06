---
layout: post 
title: Python-Regular-Expressions
date: 2019-02-09 16:20:23 +0900 
category: Python 
tag: Python 
---

<html lang="en">
<head>
<title>Python regular expressions - using regular expressions in Python</title>
<link rel="stylesheet" href="/cfg/style.css" type="text/css">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="keywords" content="Python, regular expressions, programming, language">
<meta name="description" content="Python regular expressions tutorial shows how
to use regular expressions in Python. The examples work with quantifiers, character classes,
alternations, and groups.">
<meta name="author" content="Jan Bodnar">

</head>

<body>

<header>

</header>

<div class="container">

<div class="content">

<h1>Python regular expressions</h1>

<p>
Python regular expressions tutorial shows how to use regular expressions 
in Python. For regular expressions in Python we use the re module.
</p>


<p>
Regular expressions are used for text searching and more advanced text 
manipulation. Regular expressions are built-in tools like grep, sed, 
text editors like vi, emacs, programming languages like Tcl, Perl, and Python. 
</p>


<h2>Python re module</h2>

<p>
In Python, the <code>re</code> module provides regular expression 
matching operations.
</p>

<p>
A <em>pattern</em> is a regular expression that defines the text we are 
searching for or manipulating. It consists of text literals and 
metacharacters. The pattern is compiled with the <code>compile</code>
function. Because regular expressions often include special characters,
it is recommended to use raw strings. (Raw strings are preceded with
r character.) This way the characters are not interpreded before they
are compiled to a pattern.
</p>

<p>
After we have compiled a pattern, we can use one of the functions
to apply the pattern on a text string. The funcions include
<code>match</code>, <code>search</code>, <code>find</code>, 
and <code>finditer</code>.
</p>

<h2>Regular expressions</h2>

<p>
The following table shows some basic regular expressions:
</p>

<table>
<thead>
    <tr>
        <th>Regex</th>
        <th>Meaning</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td><code>.</code></td>
        <td>Matches any single character.</td>
    </tr>
    <tr>
        <td><code>?</code></td>
        <td>Matches the preceding element once or not at all.</td>
    </tr>    
    <tr>
        <td><code>+</code></td>
        <td>Matches the preceding element once or more times.</td>
    </tr>     
    <tr>
        <td><code>*</code></td>
        <td>Matches the preceding element zero or more times.</td>
    </tr> 
    <tr>
        <td><code>^</code></td>
        <td>Matches the starting position within the string.</td>
    </tr>
    <tr>
        <td><code>$</code></td>
        <td>Matches the ending position within the string.</td>
    </tr>
    <tr>
        <td><code>|</code></td>
        <td>Alternation operator.</td>
    </tr>
    <tr>
        <td><code>[abc]</code></td>
        <td>Matches a or b, or c.</td>
    </tr>    
    <tr>
        <td><code>[a-c]</code></td>
        <td>Range; matches a or b, or c.</td>
    </tr>
    <tr>
        <td><code>[^abc]</code></td>
        <td>Negation, matches everything except a, or b, or c. </td>
    </tr>    
    <tr>
        <td><code>\s</code></td>
        <td>Matches white space character.</td>
    </tr>
    <tr>
        <td><code>\w</code></td>
        <td>Matches a word character; equivalent to <code>[a-zA-Z_0-9]</code></td>
    </tr>
</tbody>
</table>


<h2>The regex functions</h2>

<p>
We look for matches with regex functions.
</p>

<table>
<thead>
    <tr>
        <th>Function</th>
        <th>Description</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td><code>match</code></td>
        <td>Determines if the RE matches at the beginning of the string.</td>
    </tr>
    <tr>
        <td><code>fullmatch</code></td>
        <td>Determines if the RE matches the whole of the string.</td>
    </tr>       
    <tr>
        <td><code>search</code></td>
        <td>Scans through a string, looking for any location where this RE matches.</td>
    </tr>    
    <tr>
        <td><code>findall</code></td>
        <td>Finds all substrings where the RE matches, and returns them as a list.</td>
    </tr>       
    <tr>
        <td><code>finditer</code></td>
        <td>Finds all substrings where the RE matches, and returns them as an iterator.</td>
    </tr>     

    <tr>
        <td><code>split</code></td>
        <td>Splits the string by RE pattern.</td>
    </tr>           
</tbody>
</table>

<p>
The <code>match</code>, <code>fullmatch</code>, and <code>search</code> functions return a match object if they 
are successful. Otherwise, they return <code>None</code>.
</p>


<h2>The match function</h2>

<p>
The <code>match</code> function returns a match object if zero or more
characters at the  beginning of string match the regular expression pattern.
</p>

<div class="codehead">match_fun.py</div>
<pre class="code">
#!/usr/bin/env python

import re

words = ('book', 'bookworm', 'Bible', 
    'bookish','cookbook', 'bookstore', 'pocketbook')

pattern = re.compile(r'book')

for word in words:

    if re.match(pattern, word):
        print(f'The {word} matches')
</pre>

<p>
In the example, we have a tuple of words. The compiled pattern will 
look for a 'book' string in each of the words.
</p>

<pre class="explanation">
pattern = re.compile(r'book')
</pre>

<p>
With the <code>compile</code> function, we create a pattern. The regular
expression is a raw string and consists of four normal characters.
</p>

<pre class="explanation">
for word in words:

    if re.match(pattern, word):
        print(f'The {word} matches')
</pre>

<p>
We go through the tuple and call the <code>match</code> function.
It applies the pattern on the word. The <code>match</code> function
returns a match object if there is a match at the beginning of a string.
It returns <code>None</code> if there is no match.
</p>

<pre class="compact">
$ ./match_fun.py 
The book matches 
The bookworm matches 
The bookish matches 
The bookstore matches 
</pre>

<p>
Four of the words in the tuple match the pattern. Note that the words
that do not start with the 'book' term do not match. To include also 
these words, we use the <code>search</code> function.
</p>


<h2>The fullmatch function</h2>

<p>
The <code>fullmatch</code> function looks an exact match.
</p>

<div class="codehead">fullmatch_fun.py</div>
<pre class="code">
#!/usr/bin/env python

import re

words = ('book', 'bookworm', 'Bible', 
    'bookish','cookbook', 'bookstore', 'pocketbook')

pattern = re.compile(r'book')

for word in words:

    if re.fullmatch(pattern, word):
        print(f'The {word} matches')
</pre>

<p>
In the example, we use the <code>fullmatch</code> function to look for
the exact 'book' term.
</p>

<pre class="compact">
$ ./fullmatch_fun.py 
The book matches
</pre>

<p>
There is only one match.
</p>


<h2>The search function</h2>

<p>
The <code>search</code> function looks for the first location where 
the regular expression pattern produces a match.
</p>

<div class="codehead">search_fun.py</div>
<pre class="code">
#!/usr/bin/env python

import re

words = ('book', 'bookworm', 'Bible', 
    'bookish','cookbook', 'bookstore', 'pocketbook')

pattern = re.compile(r'book')

for word in words:

    if re.search(pattern, word):
        print(f'The {word} matches')   
</pre>

<p>
In the example, we use the <code>search</code> function to look for
the 'book' term.
</p>

<pre class="compact">
$ ./search_fun.py 
The book matches 
The bookworm matches 
The bookish matches 
The cookbook matches 
The bookstore matches 
The pocketbook matches 
</pre>

<p>
This time the cookbook and pocketbook words are included as well.
</p>


<h2>Dot metacharacter</h2>

<p>
The dot (.) metacharacter stands for any single character in the text. 
</p>

<div class="codehead">dot_meta.py</div>
<pre class="code">
#!/usr/bin/env python

import re

words = ('seven', 'even', 'prevent', 'revenge', 'maven', 
    'eleven', 'amen', 'event')

pattern = re.compile(r'.even')

for word in words:
    if re.match(pattern, word):
        print(f'The {word} matches')
</pre>

<p>
In the example, we have a tuple with eight words. We apply a pattern
containing the dot metacharacter on each of the words.
</p>

<pre class="explanation">
pattern = re.compile(r'.even')
</pre>

<p>
The dot stands for any single character in the text. The character must
be present.
</p>

<pre class="compact">
$ ./dot_meta.py 
The seven matches 
The revenge matches 
</pre>

<p>
Two words match the pattern: seven and revenge.
</p>



<h2>Question mark meta character</h2>

<p>
The question mark (?) meta character is a quantifier that matches the 
previous element zero or one time.
</p>

<div class="codehead">question_mark_meta.py</div>
<pre class="code">
#!/usr/bin/env python

import re

words = ('seven', 'even','prevent', 'revenge', 'maven', 
    'eleven', 'amen', 'event')

pattern = re.compile(r'.?even')

for word in words:

    if re.match(pattern, word):
        print(f'The {word} matches')
</pre>

<p>
In the example, we add a question mark after the dot character.
This means that in the pattern we can have one arbitrary character
or we can have no character there. 
</p>

<pre class="compact">
$ ./question_mark_meta.py 
The seven matches 
The even matches 
The revenge matches 
The event matches 
</pre>

<p>
This time, in addition to seven and revenge, the even and event words
match as well.
</p>


<h2>Anchors</h2>

<p>
Anchors match positions of characters inside a given text. 
When using the ^ anchor the match must occur at the beginning of the 
string and when using the $ anchor the match must occur at the end
of the string.
</p>

<div class="codehead">anchors.py</div>
<pre class="code">
#!/usr/bin/env python

import re

sentences = ('I am looking for Jane.',
    'Jane was walking along the river.',
    'Kate and Jane are close friends.')

pattern = re.compile(r'^Jane')

for sentence in sentences:
    
    if re.search(pattern, sentence):
        print(sentence)
</pre>

<p>
In the example, we have three sentences. The search pattern is 
<code>^Jane</code>. The pattern checks if the "Jane" string is located 
at the beginning of the text. The <code>Jane\.</code> would look for 
"Jane" at the end of the sentence. 
</p>


<h2>Exact match</h2>

<p>
An exact match can be performed with the <code>fullmatch</code>
function or by placing the term between the anchors: ^ and $.
</p>

<div class="codehead">exact_match.py</div>
<pre class="code">
#!/usr/bin/env python

import re

words = ('book', 'bookworm', 'Bible', 
    'bookish','cookbook', 'bookstore', 'pocketbook')

pattern = re.compile(r'^book$')

for word in words:

    if re.search(pattern, word):
        print(f'The {word} matches')  
</pre>

<p>
In the example, we look for an exact match for the 'book' term.
</p>

<pre class="compact">
$ ./exact_match.py 
The book matches
</pre>



<h2>Character classes</h2>

<p>
A character class defines a set of characters, any 
one of which can occur in an input string for a match to succeed.
</p>

<div class="codehead">character_class.py</div>
<pre class="code">
#!/usr/bin/env python

import re

words = ('a gray bird', 'grey hair', 'great look')

pattern = re.compile(r'gr[ea]y')

for word in words:

    if re.search(pattern, word):
        print(f'{word} matches') 
</pre>

<p>
In the example, we use a character class to include both gray and grey
words.
</p>

<pre class="explanation">
pattern = re.compile(r'gr[ea]y')
</pre>

<p>
The <code>[ea]</code> class allows to use either 'e' or 'a' charcter
in the pattern.
</p>


<h2>Named character classes</h2>

<p>
There are some predefined character classes. The <code>\s</code>
matches a whitespace character <code>[\t\n\t\f\v]</code>, the
<code>\d</code> a digit <code>[0-9]</code>, and the <code>\w</code>
a word character <code>[a-zA-Z0-9_]</code>.
</p>

<div class="codehead">named_character_class.py</div>
<pre class="code">
#!/usr/bin/env python

import re

text = 'We met in 2013. She must be now about 27 years old.'

pattern = re.compile(r'\d+')

found = re.findall(pattern, text)

if found:
    print(f'There are {len(found)} numbers')   
</pre>

<p>
In the example, we count numbers in the text.
</p>

<pre class="explanation">
pattern = re.compile(r'\d+')
</pre>

<p>
The <code>\d+</code> pattern looks for any number of digit sets in
the text.
</p>

<pre class="explanation">
found = re.findall(pattern, text)
</pre>

<p>
With <code>findall</code> method, we look up all numbers in the text.
</p>

<pre class="compact">
$ ./named_character_classes.py 
There are 2 numbers
</pre>



<h2>Case insensitive match</h2>

<p>
By default, the matching of patterns is case sensitive. 
By passing the <code>re.IGNORECASE</code> to the <code>compile</code>
function, we can make it case insensitive.
</p>

<div class="codehead">case_insensitive.py</div>
<pre class="code">
#!/usr/bin/env python

import re

words = ('dog', 'Dog', 'DOG', 'Doggy')

pattern = re.compile(r'dog', re.IGNORECASE)

for word in words:
    if re.match(pattern, word):
        print(f'{word} matches')
</pre>

<p>
In the example, we apply the pattern on words regardless of the case.
</p>

<pre class="compact">
$ ./case_insensitive.py 
dog matches
Dog matches
DOG matches
Doggy matches
</pre>

<p>
All four words match the pattern.
</p>


<h2>Alternations</h2>

<p>
The alternation operator | creates a regular expression with several choices. 
</p>

<div class="codehead">alternations.py</div>
<pre class="code">
#!/usr/bin/env python

import re

words = ("Jane", "Thomas", "Robert",
    "Lucy", "Beky", "John", "Peter", "Andy")

pattern = re.compile(r'Jane|Beky|Robert')

for word in words:
    
    if re.match(pattern, word):
        print(word)
</pre>

<p>
We have eight names in the list.
</p>

<pre class="explanation">
pattern = re.compile(r'Jane|Beky|Robert')
</pre>

<p>
This regular expression looks for "Jane", "Beky", or "Robert" strings. 
</p>


<h2>The finditer function</h2>

<p>
The <code>finditer</code> function returns an iterator yielding match 
objects over all non-overlapping matches for the pattern in a string.
</p>

<div class="codehead">finditer_fun.py</div>
<pre class="code">
#!/usr/bin/env python

import re

text = 'I saw a fox in the wood. The fox had red fur.'

pattern = re.compile(r'fox')

found = re.finditer(pattern, text)

for item in found:

    s = item.start()
    e = item.end()
    print(f'Found {text[s:e]} at {s}:{e}')
</pre>

<p>
In the example, we search for the 'fox' term in the text. We go over
the iterator of the found matches and print them with their indexes.
</p>

<pre class="explanation">
s = item.start()
e = item.end()
</pre>

<p>
The <code>start</code> and <code>end</code> functions return the
starting and ending index, respectively.
</p>

<pre class="compact">
$ ./finditer_fun.py 
Found fox at 8:11
Found fox at 29:32
</pre>



<h2>Capturing groups</h2>

<p>
Capturing groups is a way to treat multiple characters as a single unit. 
They are created by placing characters inside a set of round brackets. 
For instance, (book) is a single group containing 'b', 'o', 'o', 'k', 
characters.
</p>

<p>
The capturing groups technique allows us to find out those parts of a 
string that match the regular pattern.
</p>

<div class="codehead">capturing_groups.py</div>
<pre class="code">
#!/usr/bin/python3

import re

content = '''&lt;p&gt;The &lt;code&gt;Pattern&lt;/code&gt; is a compiled
representation of a regular expression.&lt;/p&gt;'''

pattern = re.compile(r'(&lt;/?[a-z]*&gt;)')

found = re.findall(pattern, content)

for tag in found:
    print(tag)
</pre>

<p>
The code example prints all HTML tags from the supplied string by 
capturing a group of characters. 
</p>

<pre class="explanation">
found = re.findall(pattern, content)
</pre>

<p>
In order to find all tags, we use the <code>findall</code> method.
</p>

<pre class="compact">
$ ./capturing_groups.py 
&lt;p&gt;
&lt;code&gt;
&lt;/code&gt;
&lt;/p&gt;
</pre>

<p>
We have found four HTML tags.
</p>


<h2>Python regex email example</h2>

<p>
In the following example, we create a regex pattern for checking 
email addresses. 
</p>

<div class="codehead">emails.py</div>
<pre class="code">
#!/usr/bin/env python

import re

emails = ("luke@gmail.com", "andy@yahoocom", 
    "34234sdfa#2345", "f344@gmail.com")

pattern = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z.]{2,18}$')

for email in emails:

    if re.match(pattern, email):
        print(f'{email} matches')
    else:
        print(f'{email} does not match')
</pre>

<p>
This example provides one possible solution. 
</p>

<pre class="explanation">
pattern = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z.]{2,18}$')    
</pre>

<p>
The first <code>^</code> and the last <code>$</code> characters provide 
an exact pattern match. No characters before and after the pattern are allowed.
The email is divided into five parts. The first part is the local part. 
This is usually a name of a company, individual, or a nickname.
The <code>[a-zA-Z0-9._-]+</code> lists all possible characters, we can 
use in the local part. They can be used one or more times. 
</p>

<p>
The second part consists of the literal <code>@</code> character. The third 
part is the domain part. It is usually the domain name of the email provider 
such as Yahoo, or Gmail. The <code>[a-zA-Z0-9-]+</code> 
is a character class providing all characters that can be used in the domain name. 
The <code>+</code> quantifier allows to use of one or more of these characters. 
</p>

<p>
The fourth part is the dot character. It is preceded by the escape character (\)
to get a literal dot. 
</p>

<p>
The final part is the top level domain: <code>[a-zA-Z.]{2,18}</code>.
Top level domains can have from 2 to 18 characters, such as sk, net, info, 
travel, cleaning, travelinsurance. The maximum length can be 63 characters, 
but most domain are shorter than 18 characters today. There is also a 
dot character. This is because some top level domains have two parts; 
for instance co.uk.
</p>

<pre class="compact">
$ ./emails.py 
luke@gmail.com matches
andy@yahoocom does not match
34234sdfa#2345 does not match
f344@gmail.com matches
</pre>


</div> <!-- content -->

<div class="rtow">


</div>

</div> <!-- container -->

</body>
</html>

