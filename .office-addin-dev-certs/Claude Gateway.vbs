' ============================================================================
' Claude Gateway.vbs — Launcher v1.0 (Python embedded local)
' ============================================================================
Set objShell = WScript.CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

Dim appDir, pythonDir, pythonExe, guiScript

appDir = objFSO.GetParentFolderName(WScript.ScriptFullName) & "\.app"
pythonDir = appDir & "\python"
pythonExe = pythonDir & "\pythonw.exe"
guiScript = appDir & "\gateway_gui.py"

' Validate
If Not objFSO.FileExists(pythonExe) Then
    MsgBox "Python nao encontrado em:" & vbCrLf & pythonDir, vbCritical, "Claude Gateway"
    WScript.Quit 1
End If
If Not objFSO.FileExists(guiScript) Then
    MsgBox "gateway_gui.py nao encontrado em:" & vbCrLf & appDir, vbCritical, "Claude Gateway"
    WScript.Quit 1
End If

' Set TCL/TK env (required for embedded Python with tkinter)
Dim tclDir
tclDir = pythonDir & "\tcl"
If objFSO.FolderExists(tclDir) Then
    Dim env
    Set env = objShell.Environment("Process")
    env("TCL_LIBRARY") = tclDir & "\tcl8.6"
    env("TK_LIBRARY") = tclDir & "\tk8.6"
End If

' Launch (window style 0 = hidden, pythonw.exe = no console)
objShell.Run """" & pythonExe & """ """ & guiScript & """", 1, False
