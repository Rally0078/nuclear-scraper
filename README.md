<h1>Nuclear Scraper (NSFW)</h1>
<br />
This is a program to find the nhentai categories of a given nuclear code.<br />
I made this solely for <i>personal use</i> and experimentation, and probably has bad code in it.<br />
<br /><br />Usage:<br />
ws2.py contains a class NuclearScraper that can be initialized with an nhentai URL number:<br /><br />

```python
obj = NuclearScraper(70133) 
```
The actual data can be printed by using the print_cat() method:<br />
```python
obj.print_cat()
```
The "Uploaded:" feature is currently WIP(shows wrong numbers) and the actual date, time of creation of the nhentai page can be printed by adding the 'd' flag to the constructor:<br />

```python
obj2 = NuclearScraper(354322,'d')
```
Printing this instance with print_cat() will show the exact date and time when the page was created:<br />

```python
obj2.print_cat() #2021-04-06 08:47:26.210055+00:00
```
<br />
To do:<br />
1. elementwise access of cat_dictionary<br />
2. working "Uploaded:" day<br />
