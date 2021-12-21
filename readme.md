<ol>
    <li>
        Get all the papers for a dr from scholar and Scopus download all the author papers as a CSV file.
    </li>
    <li>
        Reorder the column into the following: cites, auths, title, publisher, year, URL
</li>
<li>
    You should have two files, <b>scholar.csv</b> and <b>scopus.csv</b>
</li>
<li>
Run <span style="color: blue;font-weight: bold">difference_report.py</span>. A new file will be generated called <b>difference_report.csv.</b> This file contains all the papers that have a difference in citations that you should focus on
    </li>
    <li>
    For each paper with differences:
    <ul>
        <li>
            Use "publish or perish" to get all scholar citations and put them into the "scholar" folder.
        </li>
        <li>
            Use "Scopus" to get all Scopus citations and put them into the "Scopus" folder.
        </li>
    </ul>
    </li>
    <li>
   Run <span style="color: blue;font-weight: bold">generate_missing_report.py</span> this file will generate the missing report to submit for Scopus.
    </li>
</ol>