#!/bin/bash

#  createHtml.sh
#
#
#  Created by Felle on 8/19/15.
#

year=0;

cd papers

echo "<head>" >> papers.html
echo "  <title>Ulderico Fugacci - Home Page</title>" >> papers.html
echo "	<link rel='stylesheet' type='text/css' href='styles/style.css' />" >> papers.html
echo "  <script type='text/javascript' src='scripts/details-shim.min.js'></script>" >> papers.html
echo "  <link rel='stylesheet' type='text/css' href='styles/details-shim.min.css'>" >> papers.html
echo "  <link rel="shortcut icon" type="image/x-icon" href="images/favicon.png">" >> papers.html
echo "</head>" >> papers.html
echo "<body>" >> papers.html
echo "<div id='main'>" >> papers.html
echo "		<div id='header'>" >> papers.html
echo "				<table width=90%>" >> papers.html
echo "						<tr>" >> papers.html
echo "							<td align='left'><div id=title>Ulderico Fugacci   </div></td>" >> papers.html
echo "							<td align='left'>" >> papers.html
echo "							<img src="images/index0.png" alt=" " class="logo"  width=100px/>" >> papers.html
echo "							</a>" >> papers.html
echo "							</td>" >> papers.html
echo "							<td align='right'>" >> papers.html
echo "							<a target='_blank' href='http://www.imati.cnr.it/make_home_page.php?status=start'>" >> papers.html
echo "							<img src="images/logo-imati.png" alt="IMATI" class="logo"  width=275px/>" >> papers.html
echo "							</a>" >> papers.html
echo "							</td>" >> papers.html
echo "						</tr>" >> papers.html
echo "				</table>" >> papers.html
echo "				<div id='menubar'>" >> papers.html
echo "						<ul id='menu'>" >> papers.html
echo "							<li><a href='index.html'>Home</a></li>" >> papers.html
echo "							<li class='selected'><a href='papers.html'>Publications</a></li>" >> papers.html
# echo "							<li><a href='extras.html'>Extras</a></li>" >> papers.html
echo "						</ul>" >> papers.html
echo "				</div>" >> papers.html
echo "			</div>" >> papers.html
echo "<div id=content>" >> papers.html

for i in $(ls -d */ | sort -r);
do
	cd $i

	#rm papers.html

	arr=("","","","","","","","")
	k=0;

	while read line
	do
		arr[k]=$line;
		k=$k+1;
	done <${i%%/}-description.txt

	if [ $year != ${arr[1]} ]
	then
		year=${arr[1]};
		echo "<br><h2 id=name>" >> ../papers.html
		echo $year >> ../papers.html
		echo "</h2>" >> ../papers.html
	fi

	echo "<div id=paper>" >>  ../papers.html
	echo "<p><b>" >>  ../papers.html
	echo ${arr[0]} >>  ../papers.html
	echo "</b><br>" >>  ../papers.html
	echo ${arr[2]} >>  ../papers.html
	echo "<br>" >>  ../papers.html
	echo "<em>" >>  ../papers.html
	echo ${arr[3]} >>  ../papers.html
	echo "</em><br>" >>  ../papers.html


	if [ -f ${i%%/}-bibtex.txt ]
	then
		echo "[<a target='_blank' href='" >> ../papers.html
		echo papers/$i${i%%/}-bibtex.txt >> ../papers.html
		echo "'>bibtex</a>]" >> ../papers.html
	fi
	if [ -f ${i%%/}.pdf ]
	then
		echo "[<a target='_blank' href='" >> ../papers.html
		echo papers/$i${i%%/}.pdf >> ../papers.html
		echo "'>paper</a>]" >> ../papers.html
	fi
	if [ "${arr[4]}" != "to appear" ] && [ "${arr[4]}" != "" ] && [ "${arr[4]}" != $'\n' ]
	then
		echo "[<a target='_blank' href='" >> ../papers.html
		echo ${arr[4]} >> ../papers.html
		echo "'>doi</a>]" >> ../papers.html
	fi
	if [ -f ${i%%/}-pres.pdf ]
	then
		echo "[<a target='_blank' href='" >> ../papers.html
		echo papers/$i${i%%/}-pres.pdf >> ../papers.html
		echo "'>slides</a>]" >> ../papers.html
	fi
	if [ -f ${i%%/}-pres.ppt ]
	then
		echo "[<a target='_blank' href='" >> ../papers.html
		echo papers/$i${i%%/}-pres.ppt >> ../papers.html
		echo "'>presentation</a>]" >> ../papers.html
	fi
	if [ -f ${i%%/}-poster.pdf ]
	then
		echo "[<a target='_blank' href='" >> ../papers.html
		echo papers/$i${i%%/}-poster.pdf >> ../papers.html
		echo "'>poster</a>]" >> ../papers.html
	fi
	if [ -f ${i%%/}-poster.ppt ]
	then
		echo "[<a target='_blank' href='" >> ../papers.html
		echo papers/$i${i%%/}-poster.ppt >> ../papers.html
		echo "'>poster</a>]" >> ../papers.html
	fi
	if [ "${arr[6]}" == "M" ]
	then
		echo "<div class=h3Green align='right'> Awarded with a Honorable Mention at SMI 2015 </div>" >> ../papers.html
	fi
  if [ "${arr[6]}" == "N" ]
	then
		echo "<div class=h3Green align='right'> Awarded as Best Paper at SMI 2019 </div>" >> ../papers.html
	fi
	if [ "${arr[6]}" == "B" ]
	then
		echo "<div class=h3Green align='right'> Awarded as Best Paper </div>" >> ../papers.html
	fi
	if [ "" != "${arr[5]}" ]
	then
		echo "<details><summary>Abstract</summary>" >> ../papers.html
		echo ${arr[5]} >> ../papers.html
		echo "</details>" >> ../papers.html
	fi
	echo "  </div>" >>  ../papers.html
	cd ..
done

echo "</div>" >> papers.html
echo "</body>" >> papers.html

mv papers.html ../papers.html
