# Plug-Scraper
<b>An advnace Plugable Based Scraper</b>

A Plugin Based Scraper with some extra features

Note: This is in beta phase (buggy) and requires fixes as I've used hackish methods (I think so) to make it work and you are free to clone and make pull requests<br>While my main moto was to make my scraping as easy as possible so I made this you can impliment and use it in other projects/codes as well ;-)

<b>Features:</b>
<ul>
<li>Completey Pluggable (Plugins to add support for various sites without toucing the main code)</li>
<li>New Modules can be added easily in the ./scraper/plugins folder</li>
<li> Pluggins can be reloaded or updated in runtime without stopping the program (This is applicable if you use this project with a api or bots so you can use the reload_plugins() function) </li>
<li>Data returned in a dictionary </li>
<li>The main imports are done in core module so the scraper plugin is as clean and readable as possible</li>
</ul>

<b>Languages Used:</b>
  1. Python

<b>To Do</b>
<ul>
  <li>Add More Plugs</li>
  <li>Find Better Ways to load modules and get loaded modules data!</li>
  <strike><li>Removing Plugs would clear the defined functions and delete the data from globals(for now removing plugs wont work the data will still be there) </li></strike>
  <li>Batch Scraping</li>
  <li>Async Support for Faster processing</li>
 </ul>
    
Thanks and you are always welcome to modify and make changes!
