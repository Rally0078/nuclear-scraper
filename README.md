<h1>Nuclear Scraper (NSFW)</h1>
<br />
This is a program to find the nhentai categories of a given nuclear code(nhentai URL number).<br />
I made this for <i>personal use</i> and experimentation, and it probably has bad code in it.<br />
<br /><br />Usage:<br />
ws2.py contains a class NuclearScraper that can be initialized with an nhentai URL number:<br /><br />

```python
obj = NuclearScraper(70133) 
```
The actual data can be printed by using the print_cat() method:<br />

```python
obj.print_cat()
```
The "Uploaded:" feature is currently WIP as it shows wrong numbers. The actual date, time of creation of the nhentai page can be printed by adding the diagnostics flag 'd' to the constructor:<br />

```python
obj2 = NuclearScraper(354322,'d')
```
Printing this instance with print_cat() will show the exact date and time when the page was created:<br />

```python
obj2.print_cat() #2021-04-06 08:47:26.210055+00:00
```
<br />
To do:<br />
1. General code refractoring<br />
2. Elementwise access of cat_dictionary<br />
3. Working "Uploaded:" day<br />
