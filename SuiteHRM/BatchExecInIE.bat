cd C:\SuiteCRM\

echo ********** Executing SuiteCRM Test Scripts on Internet Explorer Browser *****************

pybot --variable BROWSER:ie --outputdir C:\SuiteCRM\Results\IE_%date:~-4,4%%date:~-10,2%%date:~-7,2%%RANDOM% TestCases\Accounts.txt TestCases\Leads.txt TestCases\Oppurtunities.txt