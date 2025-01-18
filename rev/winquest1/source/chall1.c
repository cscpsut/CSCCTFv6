#include <Windows.h>

#pragma comment(linker, "/ENTRY:entry")

#define PRINT(STR, ...)                                                                                                 \
if (1) {                                                                                                               \
    LPWSTR buf = (LPWSTR)HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, 1024);                                           \
    if (buf != NULL) {                                                                                                 \
        int len = wsprintfW(buf, STR, __VA_ARGS__);                                                                    \
        WriteConsoleW(GetStdHandle(STD_OUTPUT_HANDLE), buf, len, NULL, NULL);                                          \
        HeapFree(GetProcessHeap(), 0, buf);                                                                            \
    }                                                                                                                  \
}
\

#define READ(INPUT_VAR)                                                                                                 \
if (1) {                                                                                                               \
    DWORD charsRead = 0;                                                                                               \
    INPUT_VAR = (LPWSTR)HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, 1024 * sizeof(WCHAR));                            \
    if (INPUT_VAR != NULL) {                                                                                           \
        HANDLE hInput = GetStdHandle(STD_INPUT_HANDLE);                                                                \
        if (hInput != INVALID_HANDLE_VALUE) {                                                                          \
            ReadConsoleW(hInput, INPUT_VAR, 1024, &charsRead, NULL);                                                   \
            INPUT_VAR[charsRead - 2] = L'\0'; /* Replace newline with null terminator */                               \
        } else {                                                                                                       \
            HeapFree(GetProcessHeap(), 0, INPUT_VAR);                                                                  \
            INPUT_VAR = NULL;                                                                                          \
        }                                                                                                              \
    }                                                                                                                  \
}

BYTE rotate_left(BYTE value, int bits) {
    return (value << bits) | (value >> (8 - bits));
}

int entry() {
    LPWSTR userInput;

    PRINT(L"Want to learn all about the windows API together??\nLet's start nice and simple, Enter the flag: ");
    READ(userInput);

    if (userInput == NULL) {
        PRINT(L"Failed to read input.\n");
        ExitProcess(1);
    }

    BYTE expected[] = {
        0x82,0x02,0x82,0x82,0x3a,0xaa,0x43,0x22,
        0x01,0xfb,0x83,0x19,0xf3,0x01,0x62,0x3b,
        0x19,0x62,0x23,0x11,0xeb,0xbb,0x19,0x23,
        0x31,0x62,0x0b,0x01,0x2b,0x01,0x0b,0x31,
        0x11,0xeb,0xa3,0x73
    };
    size_t expectedLength = sizeof(expected) / sizeof(expected[0]);

    size_t inputLength = lstrlenW(userInput);
    if (inputLength != expectedLength) {
        PRINT(L"Incorrect input length.\n");
        HeapFree(GetProcessHeap(), 0, userInput);
        ExitProcess(1);
    }

    for (size_t i = 0; i < inputLength; ++i) {
        BYTE processed = (BYTE)userInput[i] ^ 0x13;   
        processed = rotate_left(processed, 3);       

        if (processed != expected[i]) {
            PRINT(L"Incorrect :(\n");
            HeapFree(GetProcessHeap(), 0, userInput);
            ExitProcess(1);
        }
    }

    PRINT(L"Well done! Now submit the flag and let us move on to part 2\n");
    HeapFree(GetProcessHeap(), 0, userInput);
    ExitProcess(0);
}