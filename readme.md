<ol>
    <li>
        the first step is to get the all the paper for a dr from scholar and scopus download all the author paper as a csv file
    </li>
    <li>
        reorder the column into the following:
        cites, auths, title, publisher, year, url 
</li>
<li>
run "difference_report.py", a new file will be generated called
        difference_report.csv this file contains all the paper that have difference in citations that you should focus on
    </li>
    <li>
    for each paper with differences:
    <ul>
        <li>
            use publish or perish to get all scholar citation and put them into "scholar" folder
        </li>
        <li>
            use scopus to get all scopus citation and put them into "scopus" folder
        </li>
    </ul>
    </li>
    <li>
    run "generate_missing_report.py"
    this file will generate the missing report to submit for scopus
    </li>
</ol>