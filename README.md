# scrapers
Repository of all my scrapers both finished and unfinished

Coastal
Coastal's website had two different formats for the size and pricing of the contacts so I had to account for both instances.  I intentially ignored the information for hard lenses as I did not need that data for the project I was working on.  The script could be modified to account for it at a later date if needed.  I also had to use Selenium to make the page load up all of the available contacts by first clicking the "View All" button and then scrolling all the way to the bottom of the page multiple times until the page completely loaded all of the contacts.

1800-contacts
There's a problem with the 1800 contacts scraper.  Selenium will sometimes not find or select the price despite it being on the page and loaded.
I'm not sure if there is a problem with my internet or if there is an error or edge case I'm not accounting for.  I also had some difficulty with the size.  I couldn't find a consistent way to select the pack size without using the webdriver and Selenium which would have slowed the program down even more.  I already have to use Selenium to find the price which caused the spider to take over 17 minutes to run instead of the under 30 seconds it took when I ran it without getting the price.

Lenscom
Lenscome has a similar situtation to Coastal in that I simply made two different ways of detecting the size and price of the contacts.

LensCrafter
LensCrafters has a few errors on their website where it will list the number of lenses per box as 0 instead of 90.  Aside from that, it does not require the different formats like Coastal and Lenscom. 

LensDirect
Nightmare.  The size of each box is sometimes in the product details.  Sometimes it's buried in a mountain of marketing fluff named in an inconsistent way.  Sometimes it will say 6 lenses per pack.  Sometimes it will say 90 lenses in each box.  Sometimes it won't say the size anywhere in the description and you have to zoom in on the picture to read the tiny text.  It's usually in the name of the product but not always.  Pretty much if it's not in the name and it's nowhere on the page, it's 6 lenses.  Keep that in mind.
