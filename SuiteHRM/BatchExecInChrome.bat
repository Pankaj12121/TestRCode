cd C:\SuiteCRM\

echo ********** Executing SuiteCRM Test Scripts on Chrome Browser *****************

pybot --variable BROWSER:gc --outputdir C:\SuiteCRM\Results\GC_%date:~-4,4%%date:~-10,2%%date:~-7,2%%RANDOM% TestCases\Accounts.txt TestCases\Leads.txt TestCases\Oppurtunities.txt