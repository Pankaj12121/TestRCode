set source=%~dp0
set today=%Date:~10,4%%Date:~4,2%%Date:~7,2%
set t=%time:~0,8%
set t=%t::=%
set t=%t: =0%
set timestamp=%today%_%t%
echo %timestamp%

set executebaleDir=D:\Tenx\HDFCLifePOC
cd %executebaleDir%
D:
set captureScreenShot=True

echo ************Executing FG Testcases***********
call pybot --variable ScheduleBatchName:Scheduled_L2RESADD --outputdir %executebaleDir%\Results\%timestamp% -t ScheduledBatchProcessing TestSuites\Testsuite.txt
