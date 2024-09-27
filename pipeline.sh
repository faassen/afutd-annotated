# this probably should have been a makefile. oh well.

# consts
STYLESHEET_LOCAL_PATH="tufte.css"
STYLESHEET_DOWNLOAD_PATH="https://raw.githubusercontent.com/edwardtufte/tufte-css/gh-pages/tufte.css"

# used to automate conversion from RTF to HTML
LIBRE_OFFICE_APPLICATION_PATH="/usr/bin/soffice"

# will delete and remake the RTF conversion directory
function convertRtfFilesToHtml {
	rm -rf ./rtf_to_html
	# convert RTF files to HTML
	mkdir -p ./rtf_to_html
	$LIBRE_OFFICE_APPLICATION_PATH --convert-to html:"XHTML Writer File" --outdir ./rtf_to_html *.rtf
}

# if CSS stylesheet doesn't exist, get it
if test -f "${STYLESHEET_LOCAL_PATH}"; then
	echo "CSS stylesheet already downloaded."
else
	echo "Downloading stylesheet to ${STYLESHEET_LOCAL_PATH}"
	wget "${STYLESHEET_DOWNLOAD_PATH}" -O "${STYLESHEET_LOCAL_PATH}"
fi

if [ ! -d "./rtf_to_html"  ]; then
	echo "RTF conversion directory does not exist. Will convert RTF files."
	echo "This may take a minute."
	convertRtfFilesToHtml
fi

echo "Validating RTF conversion (checking all files exist)"
for chapter_num in `seq -w 0 42`; do
	if ! test -f "./rtf_to_html/c${chapter_num}b.html"; then
		echo "Could not find chapter 'c${chapter_num}b.html'. Aborting check, reconverting."
		convertRtfFilesToHtml
	fi
done

echo "Stripping everything but the body **contents** in each file."
for chapter_num in `seq -w 0 42`; do
    ## COMPATABILITY NOTES:
    # If on a mac, `brew install coreutils` to get ghead
    # if on something sane, just edit ghead to be head
    # I have no idea where xmllint comes from. You could probably hack around all this with beautifulsoup, but I was knee deep in this and lazy, so I stuck with what I had
	 echo "cat //html/body" | xmllint --html --shell ./rtf_to_html/c${chapter_num}b.html | sed '/^\/ >/d' | tail -n +2 | head -n -1 > ./rtf_to_html/working.txt
	mv ./rtf_to_html/working.txt ./rtf_to_html/c${chapter_num}b.html
done

echo "Reformatting HTML to something sane..."
rm -rf assembly
mkdir -p ./assembly

echo '<html><head><link rel="stylesheet" href="tufte.css"/></head><body>' > a_fire_upon_the_deep_annotated.html

for chapter_num in `seq -w 0 42`; do
    ./process_html.py --prefix "${chapter_num}" --inputFile "./rtf_to_html/c${chapter_num}b.html" --outputFile "./assembly/c${chapter_num}.html"

    cat "./assembly/c${chapter_num}.html" >> a_fire_upon_the_deep_annotated.html
done

echo "</body></html>" >> a_fire_upon_the_deep_annotated.html
