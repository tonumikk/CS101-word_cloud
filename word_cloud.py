# Ranked search results with word cloud

# Commented code to use cache instead
#import urllib

#def get_page(url):
#    try:
#        return urllib.urlopen(url).read()
#    except:
#        return ""

cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the 
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a> 
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>
""",
   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from 
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try 
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>
""",
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>
""",
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablespoons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>
""",
}  

def get_page(url):
    if url in cache:
        return cache[url]
    return ""  
    
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b: 
        if e not in a:
            a.append(e)
            
# Better splitting from Homework 4.5 
def split_string(source, splitlist):
    split = [] 
    for char in source:
        if char in splitlist:
            if source[0] == char:
                source = source[1:]
            else:
                location = source.find(char)
                split.append(source[0:location])
                source = source[location+1:]
    return split
            
def add_page_to_index_word_cloud(index, word_cloud, url, content,):
    words = split_string(content, " ,!-<>='\'/") # modify the split characters if necessary
    add_to_word_cloud(word_cloud, url, words) # builds the word_cloud index
    for word in words:
        add_to_index(index, word, url)
               
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

# From Unit 5.28 "Finishing Urank"
def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node]/len(graph[node]))            
            newranks[page] = newrank
        ranks = newranks
    return ranks
        
# From Homework 6 Starred 3 Quicksort
def quicksort_pages(pages, ranks):
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = ranks[pages[0]] #find pivot
        worse = []
        better = []
        for page in pages[1:]:
            if ranks[page] <= pivot:
                worse.append(page)
            else:
                better.append(page)
        return quicksort_pages(better, ranks) + [pages[0]] + quicksort_pages(worse, ranks)
        
# Added a new definition for output to include wordcloud results
def quicksort_pages_word_cloud(pages, ranks, word_cloud):
    ranked_pages_with_word_cloud = {} # {<url>:[(word,count), (word1,count), ...]}
    for page in quicksort_pages(pages, ranks):
        ranked_pages_with_word_cloud[page] = word_cloud[page][0:5] # return 5 highest occurring words and their count
    return ranked_pages_with_word_cloud
    
# From Homework 6 Starred 3 Ordered Search
def ordered_search_word_cloud(index, ranks, keyword):
    pages = lookup(index, keyword)
    if pages == None:                   # Added a check to return None if there are no pages found for a given keyword
        return None
    else:
        return quicksort_pages_word_cloud(pages, ranks, word_cloud)

# Count words takes a list as an input and returns a dictonary of word and their count pairs         
ignore_list = ['is', 'li', 'the', 'are', 'h1', 'html', '\n', 'ul', '"http:', 'href', 'a', 'ul', 'ol', 'in'] 
def count_words(p):
    counted_words = {}
    for word in p:
        num = p.count(word)
        if word in ignore_list:
            pass
        elif word in counted_words:
            pass
        elif num < 2: # Only count if the word appears more than once
            pass
        else:
            counted_words[word] = num
    ordered_dict = (sorted(counted_words.items(), key=lambda t: t[1], reverse = True)) # sort the dictonary resulting in list of tuples sorted by 
                                                                                        # most frequently appearing words first
    return ordered_dict

def add_to_word_cloud(word_cloud, url, word_list):
    if url in word_cloud:
        pass
    else:
        word_cloud[url] = count_words(word_list) # calls on count_word to provide a dictonary of word and count pairs
    return word_cloud
    
def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    word_cloud = {} # {<URL>: [(word1,count), (word2,count), ...]}
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index_word_cloud(index, word_cloud, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph, word_cloud

index, graph, word_cloud = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)

#print ordered_search_word_cloud(index, ranks, 'Hummus')
#>>> {'http://udacity.com/cs101x/urank/index.html': [('urank', 5), ('udacity.com', 5), ('cs101x', 5), ('Hummus', 3), ('s', 3)],
#'http://udacity.com/cs101x/urank/kathleen.html': [('body', 2), ('of', 2), ('Add', 2), ('\n\n', 2)],
#'http://udacity.com/cs101x/urank/arsenic.html': [('body', 2), ('Chef', 2), ('\n\n', 2)], 
#'http://udacity.com/cs101x/urank/nickel.html': [('body', 2)]}

#print ordered_search_word_cloud(index, ranks, 'garbonzo')
#>>> {'http://udacity.com/cs101x/urank/kathleen.html': [('body', 2), ('of', 2), ('Add', 2), ('\n\n', 2)]}

#print ordered_search_word_cloud(index, ranks, 'Chef')
#>>> {'http://udacity.com/cs101x/urank/zinc.html': [('p', 3), ('body', 2), ('Chef', 2), ('urank', 2), ('udacity.com', 2)],
# 'http://udacity.com/cs101x/urank/arsenic.html': [('body', 2), ('Chef', 2), ('\n\n', 2)], 
# 'http://udacity.com/cs101x/urank/nickel.html': [('body', 2)], 
# 'http://udacity.com/cs101x/urank/index.html': [('urank', 5), ('udacity.com', 5), ('cs101x', 5), ('Hummus', 3), ('s', 3)]}

#print ordered_search_word_cloud(index, ranks, 'Taurus')
#>>> None    


