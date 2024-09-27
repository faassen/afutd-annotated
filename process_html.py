#!/usr/bin/env python3

from bs4 import BeautifulSoup, Comment
from bs4.element import NavigableString

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--inputFile", required=True)
parser.add_argument("--outputFile", required=True)
parser.add_argument("--prefix", required=True, help="prefix to add to footnote IDs to avoid collisions")
args = parser.parse_args()

page_flush_header = BeautifulSoup('<p class="P1"><span class="T1">.</span><span class="T2">Delete this paragraph to shift page flush </span></p>', "html.parser")

cleaned_body_text = []
sidenotes = dict()
curr_sidenote = None

# clean up junk & parse out footnotes
with open(args.inputFile, "r") as the_file:
    soup = BeautifulSoup(the_file.read(), "html.parser")
    for child in soup.children:
        if type(child) is NavigableString:
             # newlien from file
            continue
        elif child.get_text() == page_flush_header.get_text():
            # drop the thing
            continue
        elif isinstance(child, Comment):
            continue
        elif "Footnote" in str(child["class"]):
            # drop
            continue
        elif "Standard" in str(child["class"]):
            if "footnodeNumber" in list(child.children)[0]["class"]:
                # this is the start of a footnote
                anchor_id = f"{list(list(child.children)[0].children)[0]['id']}"

                new_sidenote_tag = soup.new_tag("span")
                new_sidenote_tag["class"] = "sidenote"
                
                s = ""
                for sub_child in list(child.children)[1:]:
                    s += sub_child.get_text()

                new_sidenote_tag.append(s)
                new_sidenote_tag.append(soup.new_tag("br"))

                sidenotes[anchor_id] = new_sidenote_tag
                curr_sidenote = new_sidenote_tag
            else:
                s = ""
                for sub_child in child.children:
                    s += sub_child.get_text()
                curr_sidenote.append(s)
                new_sidenote_tag.append(soup.new_tag("br"))
        else:
            #print("default", child['class'])
            cleaned_body_text.append(child)


# iterate over cleaned stuff, filtering out anchors & replacing with sidenote spans instead

new_soup = BeautifulSoup('', "html.parser")

for element in cleaned_body_text:
        new_soup.append(element)

for span in new_soup.findAll('span'):
    if span["class"] == []:
        span.replaceWith(list(span.children)[0])


for anchor in new_soup.findAll('a'):
    # new span to contain goodies
    new_span = new_soup.new_tag('span')
    
    new_label = new_soup.new_tag("label")
    new_label["for"] = f"{args.prefix}{anchor['href'][1:]}"
    new_label["class"] = "margin-toggle sidenote-number"
    
    new_input = new_soup.new_tag("input")
    new_input["type"] = "checkbox"
    new_input["id"] = f"{args.prefix}{anchor['href'][1:]}"
    new_input["class"] = "margin-toggle"

    new_span.append(new_label)
    new_span.append(new_input)
    new_span.append(sidenotes[anchor["href"][1:]])

    anchor.parent.replaceWith(new_span)

for div in new_soup.findAll('div'):
    # TODO: more directly translate the formatting here, rather than just stripping it
    # div P4s (and P7s?) seem to be section breaks--consider replacing with hrules
    # p P6s may be chapter breaks (chapter headers don't seem to be formatted at all)
    # div (P8s, P9s, P12s) and p (P8s, P9s, P12s) look  to be message blocks, but end with some P3s of normal text (and P3 is shared by normal book text too)
    #   (looks like they contain span T7s that are unique, though--possible to key off those? use one font for message header and another for message body?)
    div_classes_to_strip = ["P2", "P3", "P5",  "P8", "P9", "P12"]
    divs_that_may_be_hrules = ["P4", "P7"]
    if any([x in div["class"] for x in div_classes_to_strip]):
        div.name = "p"
    elif any([x in div["class"] for x in divs_that_may_be_hrules]):
        div.append(new_soup.new_tag("hr"))

with open(args.outputFile, "w") as ofile:
    ofile.write(str(new_soup))
