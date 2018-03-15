cd C:\SuiteCRM\

echo ********** Executing SuiteCRM Test Scripts on Firefox Browser *****************

pybot --variable BROWSER:ff --outputdir C:\SuiteCRM\Results\FF_%date:~-4,4%%date:~-10,2%%date:~-7,2%%RANDOM% TestCases\Accounts.txt TestCases\Leads.txt TestCases\Oppurtunities.txt