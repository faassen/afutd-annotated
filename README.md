# A Fire Upon the Deep Annotated in HTML

This is code to convert the author annotated version of Vernor Vinge's novel "A
Fire Upon the Deep" from the original RTF to readable HTML.

This is not my own work, but is based on the following [gist](https://gist.github.com/bocajnotnef/f3f43acc065a2a1a4dd433b8eace3f2b)

I had some problems making it work on my Fedora 40 system.

In particular:

The pipeline.sh script used the soffice flag `--convert-to html` but this didn't
output any class information, only inline styles. Modifiying it to use
`-convert-to html:"XHTML Writer File"` fixed this.

The Python script also ran into some problems: 

* HTML comments were beautiful soup nodes and are now skipped

* The check for the presence of substrings in class names wasn't working
  properly, and a `str()` call fixed that.

* Some paragraphs became div for some reason, so turn them back into proper
  `p`
  
See `instructions.md` for the original instructions on how to run this.
