CS101 Extend the search engine contest
Tonu Mikk 04/13/2012

Project Title:  Ranked search results with word cloud
Project Goal: For each search result create a word cloud of most frequently appearing words in each 
search result page and display the word cloud results with the returned page.

For this project I did the following:
1.  Started with the finished search engine code from Unit 7 supplementary materials.
2.  Added cach of pages instead of live crawling of pages.
3.  Added code to use cach and commented out the code for live crawling.
4.  Added "Better Splitting" of page content into words from Homework 4.5.
5.  Added "Urank" from Unit 5 section 28 which is necessary for ranked pages.
6.  Added "Quicksort Pages" and returning of pages by rank from Homework 6 Starred 3.
5.  Created a new definition "count_words" that takes a list as an input and outputs a sorted list tuples
 where the first element is a most frequently appearing word and the second element is the number of times 
 this word occurs in the page.  This definition ignores words that are in the "ignore_list".  It also ignores
 words if they appear only once.  The "count_words" function is called from "add_page_to_index_word_cloud" 
 function that generates a split list of words from a page.
 6.  Added a function "add_to_word_cloud" that builds the word_cloud dictonary.  The dictonary consists of 
<URL> as a key and a list of frequently appearing words from "count_words".
7. Added a global variable "word_cloud" in the "crawl_web" definition.
8. Added the "word_cloud" variable into definitions where necessary.
9. Renamed the definitions to better reflect the added "word_cloud" functionality:
    ordered_search --> ordered_search_word_cloud
    add_page_to_index --> add_page_to_index_word_cloud
10.  Added the "quicksort_pages_word_cloud" to output the ranked search results each accompanied by a word cloud
of 5 most frequently appearing words.
11.  Modified the "ordered_search_word_cloud" function to return "None" if there are no pages found
with a given keyword.
12.  Added test cases and the output that they generate