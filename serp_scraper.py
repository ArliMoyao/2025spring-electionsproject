# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
import os
from urllib.parse import urlparse
import json
import sys

def getFeaturedSnippet(block):
    """
    Takes a featured snippet component as a parameter and returns a dictionary of information about it, like:
    title, link and domain of the source page. It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    featured_snippet = {}
    div = block.find('div', class_='yuRUbf')
    a_link = div.find('a')
    link = a_link.get('href')
    title = div.find('h3').text
    cite_domain = block.find('cite')
    domain = cite_domain.text.split()[0]
    featured_snippet['title'] = title
    featured_snippet['link'] = link
    featured_snippet['domain'] = domain
    featured_snippet['type'] = 'featured snippet'
    return featured_snippet

def getPeopleAlsoAsk(block):
    """
    Takes a People also ask component as a parameter and returns a dictionary of information about it, like:
    title, link and domain of each source page. It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    paa = {} #people also ask
    data = []
    g_divs = block.find_all('div', class_='g')
    for g in g_divs:
        div = g.find('div', class_='yuRUbf')
        a_link = div.find('a')
        link = a_link.get('href')
        title = div.find('h3').text
        cite_domain = div.find('cite')
        domain = cite_domain.text.split()[0]
        data.append((domain, link, title))
    paa['data'] = data
    paa['type'] = 'people also ask'
    return paa

def getTwitter(block):
    """
    Takes a Tweeter results component as a parameter and returns a dictionary of information about it, like:
    tweet link, tweeter name and tweeter handle of the person who tweets belong to.
    It also adds a type key to the resulting dictionary, which indicated what component it is.
    
    The function also differentiates between two kinds of Tweeter results: 1) first kind of result includes
    from different users, so the HTML is a little different, 2) second kind of result includes tweets from
    one particular user.
    """
    twitter = {}
    data = []
    search_url = 'https://twitter.com/search/'
    url = block.find('cite', class_='ellip iUh30').text
    if search_url in url: #tweets from different accounts
        tweet_divs = block.find_all('div', class_='fy7gGf')
        for div in tweet_divs:
            overlapping = div.find('div', class_='fy7gGf')
            if not overlapping and len(div.contents)>0:
                g_link = div.find('g-link')
                link = g_link.find('a').get('href')
                texts = div.find('div', class_ = 'zTpPx').text.split('@')
                data.append({'twitter_name': texts[0], 'twitter_handle': texts[1],'link': link})
        
    else: #tweets from one account
        tweeter_info = block.find('g-link')
        tweeter_info = tweeter_info.find('h3').text.split('·')[0]
        name = tweeter_info.split(' (')[0].strip()
        handle = tweeter_info.split(' (')[1].replace(')', '').strip()
        tweet_divs = block.find_all('div', class_='fy7gGf')
        for div in tweet_divs:
            overlapping = div.find('div', class_='fy7gGf')
            if not overlapping and len(div.contents)>0:
                link = div.find('a', class_='h4kbcd').get('href')
                data.append({'twitter_handle': handle, 'twitter_name': name, 'link': link})
                
    twitter['type'] = 'twitter results'
    twitter['data'] = data
    return twitter

def getVideos(block):
    """
    Takes a Videos component as a parameter and returns a dictionary of information about it, like:
    platform, link and source of each video. It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    videos = {}
    data = []
    vvs = block.find_all('video-voyager') #vvs - video-voyager tags
    for v in vvs:
        link = v.find('a', class_='X5OiLe').get('href')
        title = v.find('div', class_='uOId3b').text
        texts = v.find('span', class_='pcJO7e').text
        platform = texts.split('·')[0].strip()
        if len(texts.split('·'))>1:
            source_name = texts.split('·')[1].strip() 
            data.append({'source': source_name, 'platform': platform, 'link': link})
        data.append({'source': platform, 'platform': platform, 'link': link})
    videos['type'] = 'videos'
    videos['data'] = data
    return videos

def getRelatedSearch(relser_div):
    """
    Takes a Related Searcher component as a parameter and returns a dictionary of information about it, like:
    all all of the suggested search queries. It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    related_search = {}
    data = []
    divs = relser_div.find_all('div', class_='AJLUJb')
    for div in divs:
        for c in div.children:
            search = c.text.strip()
            data.append(search)
    related_search['type'] = 'related searches'
    related_search['data'] = data
    return related_search

def getTopStories(block):
    """
    Takes a top stories component as a parameter and returns a dictionary of information about it, like:
    title, link and domain of each top story. It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    top_stories = {}
    data = []
    ts_blocks = block.find_all('a', class_='WlydOe')
    for ts in ts_blocks:
        link = ts.get('href')
        domain = urlparse(link).netloc
        title = ts.find('div', class_='mCBkyc tNxQIb ynAwRc nDgy9d').text.strip()
        data.append({'domain':domain, 'link':link, 'title':title})
    top_stories['type'] = 'top stories'
    top_stories['data'] = data
    
    return top_stories

def getMap(block):
    """
    Takes a map component as a parameter, and returns a 
    dictionary with a type of the component.
    """
    local_results = {}
    local_results['type'] = 'map'
    return local_results

def getImages(block):
    """
    Takes an Images component as a parameter, and returns a 
    dictionary with a type of the component.
    """
    images = {}
    images['type'] = 'images'
    return images

def getKnowledgePanel(block): #does not yet recognize different subsections of the panel
    """
    Takes a knowledge panel component as a parameter, and returns a 
    dictionary with a type of the component.
    """
    knowledge_panel = {}
    data = []
    knowledge_panel['type'] = 'knowledge panel'
    return knowledge_panel

def getSeeResultsAbout(block):
    """
    Takes a See results about component as a parameter and returns a dictionary of information about it, like:
    all of the suggested searcher and their links. It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    sra = {}
    data = []
    a_blocks = block.find_all('a')
    for a in a_blocks:
        link = a.get('href')
        text = a.find('div', class_='RJn8N').text
        data.append({'text': text, 'link': link})
    sra['type'] = 'see results about'
    sra['data'] = data
    return sra

def getDictionary(block):
    """
    Takes a Dictionary component as a parameter and returns a dictionary of information about it, like:
    link to the dictionary, where deffinition is from. It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    dct = {}
    source_div = block.find('div', class_='c07z9')
    link = source_div.find('a').get('href')
    dct['type'] = 'dictionary'
    dct['link'] = link
    return dct

def getHotline(block):
    """
    Takes a Hotline (Help is available) component as a parameter and returns a dictionary 
    of information about it, like: source of the hotline number. 
    It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    hotline = {}
    source = block.find('div', class_='bwM3Xb').text.strip()
    hotline['type'] = 'hotline'
    hotline['source'] = source
    return hotline

def getGoogleScolar(block): ##add
    gs = {}
    gs['type'] = 'google scholar'
    return gs

def getNonOrganic(block):
    """
    Takes a non-organic component as a parameter and returns a dictionary of imformation about it,
    including a type of the component.
    To recongize a type of a component, the function looks for specific "signals" inside
    a component. If a component does not correspond to any signal, then its type is "unknown"
    """
    fs = block.find('h2', text='Featured snippet from the web') #featured snippet

    paa1 = block.find('h3', class_='O3JH7', text = 'People also ask') #People also ask v1
    paa2 = block.find('div', class_='HnYYW', text = 'People also ask') #People also ask v2
    
    vd1 = block.find('h3', text='Videos') #Videos v1
    vd2 = block.find('div', class_='HnYYW', text='Videos') #Videos v2

    tweet = block.find('h2', text='Twitter Results') #Twitter Results

    ts1 = block.find('h3', text = 'Top stories')#Top Stories v1
    ts2 = block.find('div',class_='HnYYW',text = 'Top stories')#Top Stories v2

    lr = block.find('h2', class_='Uo8X3b OhScic zsYMMe', text='Local Results') #map
    img = block.find('h3', class_='GmE3X kWYf3c') #images
    dct = block.find('div', class_='gJBeNe vbr5i', text='Dictionary') #dictionary
    gs = block.find('h3', class_='ohqNXb') #google scholar results

    rs = block.find('span', class_='q8U8x', text='Related searches') #related searches v2
    
    if fs:
        featured_snippet = getFeaturedSnippet(block)
        return(featured_snippet)
    if paa1 or paa2:
        people_also_ask = getPeopleAlsoAsk(block)
        return(people_also_ask)
    if vd1 or vd2:
        videos = getVideos(block)
        return(videos)
    if tweet:
        tweeter_results = getTwitter(block)
        return(tweeter_results)
    if ts1 or ts2:
        top_stories = getTopStories(block)
        return(top_stories)
    if lr:
        local_results = getMap(block)
        return(local_results)
    if img and "Images for" in img.text:
        images = getImages(block)
        return(images)
    if dct:
        dictionary = getDictionary(block)
        return(dictionary)
    if gs and "Scholarly articles for" in gs.text.strip():
        g_scholar = getGoogleScolar(block)
        return(g_scholar)
    if rs:
        related_search = getRelatedSearch(block)
        return(related_search)
    return {'type': 'unknown'} #if type wasn't identified

def getOrganic(block):
    """
    Takes an organic result as a parameter and returns a dictionary of information about it, like:
    title, link and domain of the source page. It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    div = block.find('div', class_='yuRUbf')
    link = div.find('a').get('href')
    title = div.find('h3').text
    cite_domain = block.find('cite')
    domain = cite_domain.text.split()[0]
    
    return {'type': 'organic', 'domain': domain, 'link': link, 'title': title}

def getAds(block, ad_type):
    """
    Takes ads component as a parameter and returns a dictionary of information about it, like:
    title, link and domain of the source page. It also adds a type key to the resulting dictionary,
    which indicated what component it is.
    """
    ads = {}
    data = []
    
    shop_carousel = block.find('div', class_='DUkiH cu-container')
    if shop_carousel:
        data.append({'type': 'shop ad'})
    
    ads_divs = block.find_all('div', class_='uEierd')

    if len(ads_divs)>0:
        for ad in ads_divs:
            a = ad.find('a', class_='sVXRqc')
            link = a.get('href')
            title = a.text.split('·')[0]
            domain = a.text.split('·')[1]
            data.append({'domain':domain,'link':link, 'title':title})
            
    if len(data)>0:
        ads['type'] = ad_type
        ads['data'] = data
        return ads
    
    return []

def getComponents(htmlText, query):
    """
    Takes an HTML text of the page and corresponding search query, returns a list of dicitonaries with 
    information about each block and their positions on the SERP.
    """
    cmpts = []
    soup = BS(htmlText,'html.parser')
    counter = 1
    
    #featured snippet(sometimes appears before any other element)
    top_fs = soup.find('div', class_='M8OgIe')
    if top_fs:
        top_fs_text = top_fs.find('h2', class_='Uo8X3b OhScic zsYMMe', text='Featured snippet from the web')
        if top_fs_text:
            cmp = getFeaturedSnippet(top_fs)
            cmp['position'] = counter
            cmp['query'] = query
            cmpts.append(cmp)
            counter+=1
    
    ##top ads and hotline
    top_block = soup.find('div', id='taw')
    help_block = top_block.find('div', id='oFNiHe')
    if help_block:
        help_is_available = help_block.find('div', class_='VAVtdc', text = '  Help is available  ')
        if help_is_available and len(help_block.contents)>0:
            cmp = getHotline(help_block)
            cmp['position'] = counter
            cmp['query'] = query
            counter+=1
            cmpts.append(cmp)
    if top_block:    
        res_top_ads = getAds(top_block, 'top ads')
        if len(res_top_ads)>0:
            res_top_ads['position'] = counter
            res_top_ads['query'] = query
            counter+=1
            cmpts.append(res_top_ads)
        
######organic and non-organic blocks in the center column###################
    lastOrganic = 1
    allBlocks = soup.find('div', class_ = 'v7W49e')
    childrenElements = []
    for ch in allBlocks.children:
        childrenElements.append(ch)

    ###Different process
    if len(childrenElements) == 1 and childrenElements[0]['class'][0] == 'ULSxyf':
        singularBlock = childrenElements[0]
        sb_text_element = singularBlock.find('h1', class_='Uo8X3b',text="Main Results")
        if sb_text_element:
            sibling = sb_text_element.next_sibling
            main_div = sibling.find('div', id='kp-wp-tab-overview')
            for block in main_div.children:
                if block.name == 'div' and block.has_attr('class'):
                    position = counter
                    counter+=1
                    if ' '.join(block['class']) == 'TzHB6b cLjAic K7khPe': ##organic block
                        cmp = getOrganic(block)
                        cmp['org-position'] = lastOrganic
                        lastOrganic+=1
                    else: #non-organic block
                        cmp = getNonOrganic(block) 
                    cmp['position'] = position
                    cmp['query'] = query
                    cmpts.append(cmp)
    #Usual process        
    else:
        for block in allBlocks.children:
            if block.name == 'div':
                position = counter
                counter+=1
                if block.has_attr('class') and block['class'][0] == 'ULSxyf': ## non-organic block
                    cmp = getNonOrganic(block)
                else: # organic
                    cmp = getOrganic(block)
                    cmp['org-position'] = lastOrganic
                    lastOrganic+=1
                cmp['position'] = position
                cmp['query'] = query
                cmpts.append(cmp)
#############################################################################
    
    ##bottom ads
    bot_ads_block = soup.find('div', id='bottomads')
    res_bot_ads = getAds(bot_ads_block, 'bottom ads')
    if len(res_bot_ads)>0:
        res_bot_ads['position'] = counter
        res_bot_ads['query'] = query
        counter+=1
        cmpts.append(res_bot_ads)
    
    ##related searches
    bottom_part = soup.find('div', id='bres')
    if bottom_part:
        bottom_search = bottom_part.find_all('div', class_='ULSxyf')
        if len(bottom_search) > 0:
            for div in bottom_search:
                if len(div.contents)>0:
                    cmp = getRelatedSearch(div)
                    cmp['position'] = counter
                    cmp['query'] = query
                    counter+=1
                    cmpts.append(cmp)
        
    ##knowledge panel and see results about
    compl_block = soup.find('div', role='complementary')
    if compl_block:
        kp_block1 = compl_block.find('div', class_='kp-wholepage')
        kp_block2 = compl_block.find('div', class_='TzHB6b Hwkikb WY0eLb LMRCfc EqrSYc')
        if kp_block1 :
            cmp = getKnowledgePanel(kp_block1)
        elif kp_block2:
            cmp = getKnowledgePanel(kp_block1)
        cmp['position'] = counter
        cmp['query'] = query
        cmpts.append(cmp)
        counter+=1
        
        sra = compl_block.find('div', class_='Hhmu2e wDYxhc NFQFxe viOShc LKPcQc', text='See results about')
        if sra:
            block = sra.next_sibling
            cmp = getSeeResultsAbout(block)
            cmp['position'] = counter
            cmp['query'] = query
            cmpts.append(cmp)

    return cmpts

def runFile(main_html_folder, date, time, state, city, file):
    """
    Takes a path to the directory with all of the saved SERPs and a particular html file, returns
    the result of getComponents() function for this html file.
    """
    #path = f"SERP_Collection/{date}/{file}"
    path = f'{main_html_folder}/{date}/{time}/{state}/{city}/{file}'
    print(path)
    html = open(path, 'r')
    htmltext = html.read()
    query = file.split('.')[0] ## change when needed
    return getComponents(htmltext, query)

def main(main_html_folder, date, time, state, city, file):
    main_results_folder = f"{main_html_folder}_json_results"
    if not os.path.isdir(main_results_folder):
        os.mkdir(main_results_folder)
    date_data = runFile(main_html_folder, date, time, state, city, file)
    filename = file.replace('/', '')
    output_file = f"{filename.split('.')[0]}.json"

    if not os.path.isdir(f"{main_results_folder}/{date}"):
        os.mkdir(f"{main_results_folder}/{date}")
    if not os.path.isdir(f"{main_results_folder}/{date}/{time}"):
        os.mkdir(f"{main_results_folder}/{date}/{time}")
    if not os.path.isdir(f"{main_results_folder}/{date}/{time}/{state}"):
        os.mkdir(f"{main_results_folder}/{date}/{time}/{state}")
    if not os.path.isdir(f"{main_results_folder}/{date}/{time}/{state}/{city}"):
        os.mkdir(f"{main_results_folder}/{date}/{time}/{state}/{city}")

    path_to_file = f"{main_results_folder}/{date}/{time}/{state}/{city}/{output_file}"
    with open(path_to_file, "w") as outfile:
        json.dump(date_data, outfile)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])