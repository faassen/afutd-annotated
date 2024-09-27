# source material

You'll need the download of the Hugo 1993 files, available from [here](https://archive.org/details/hugo_nebula_1993). If that link dies, you can scour the [original HackerNews post](https://news.ycombinator.com/item?id=24866730) to see if anyone has a mirror, or if there's other helpful files

# deps

## mac
- libreoffice installed to the `Applications/` dir
- `xmllint` I think comes for free?
- `coreutils` from `brew` (e.g. `brew install coreutils`)
- `python3`
  - `bs4` from `pip` (e.g. `pip3 install bs4`)
 
## linux
- modify the `LIBRE_OFFICE_APPLICATION_PATH` in `pipeline.sh` to point to wherever your `soffice` binary is
- modify the `ghead` call in `pipeline.sh` to plain `head`
- I've no idea if `xmllint` is available on normal distros; it's not strictly necessary, you could modify my beautifulsoup stuff to do what I use xmllint for, I'm just lazy and don't feel like doing that myself
- `python3` and `bs4`, as above

# how do

- download and unzip the hugo stuff
- navigate to `hugo-nebula anthology 1993/hugo/novel/vinge`
- download `pipeline.sh` and `process_html.py` to that directory
  - `wget whatever-the-raw-link-of-this-gist-is`
- make 'em executable
  - `chmod +x pipeline.sh && chmod +x process_html.py`
- run `pipeline.sh`
- open `a_fire_upon_the_deep_annotated.html`

# notes
- I personally recommend modifying the `css` file that's downloaded just a teensey bit. Make the `body` section look like this:

```css
body {
    width: 87.5%;
    /* margin-left: 12.5%; */
    /* margin-right: auto; */
    padding-left: 12.5%;
    /* padding-right: 12.5%; */
    font-family: et-book, Palatino, "Palatino Linotype", "Palatino LT STD", "Book Antiqua", Georgia, serif;
    background-color: #fffff8;
    color: #111;
    max-width: 50%;
    counter-reset: sidenote-counter;
}
```

and make the `.sidenote, .marginnote` section look like this:

```css
.sidenote,
.marginnote {
    float: right;
    clear: right;
    margin-right: -60%;
    width: 50%;
    margin-top: 0.3rem;
    margin-bottom: 0;
    padding: 1rem;
    font-size: 1.1rem;
    line-height: 1.0;
    vertical-align: baseline;
    position: relative;
    background: lightgray;
}
```