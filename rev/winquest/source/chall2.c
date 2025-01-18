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

void to_upper_ascii(WCHAR* wideStr, char* asciiStr, DWORD length) {
    for (DWORD i = 0; i < length; ++i) {
        char ch = (char)wideStr[i];
        if (ch >= 'a' && ch <= 'z') {
            ch -= 32;
        }
        asciiStr[i] = ch;
    }
    asciiStr[length] = '\0';
}

void to_hex_string(DWORD value, char* hexStr, DWORD digits) {
    for (DWORD i = 0; i < digits; ++i) {
        BYTE nibble = (value >> (4 * (digits - 1 - i))) & 0xF;
        hexStr[i] = (nibble < 10) ? ('0' + nibble) : ('A' + nibble - 10);
    }
    hexStr[digits] = '\0';
}

void base64_encode(const char* input, DWORD inputLen, char* output) {
    const char base64Table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    DWORD outIndex = 0;
    for (DWORD i = 0; i < inputLen; i += 3) {
        DWORD buffer = (input[i] << 16) | (inputLen > i + 1 ? input[i + 1] << 8 : 0) | (inputLen > i + 2 ? input[i + 2] : 0);
        output[outIndex++] = base64Table[(buffer >> 18) & 0x3F];
        output[outIndex++] = base64Table[(buffer >> 12) & 0x3F];
        output[outIndex++] = (inputLen > i + 1) ? base64Table[(buffer >> 6) & 0x3F] : '=';
        output[outIndex++] = (inputLen > i + 2) ? base64Table[buffer & 0x3F] : '=';
    }
    output[outIndex] = '\0';
}

int entry() {
    LPWSTR username;
    LPWSTR key;

    PRINT(L"Enter your username: ");
    READ(username);

    if (username == NULL) {
        PRINT(L"Failed to read username.\n");
        ExitProcess(1);
    }

    PRINT(L"Enter your key: ");
    READ(key);

    if (key == NULL) {
        PRINT(L"Failed to read key.\n");
        HeapFree(GetProcessHeap(), 0, username);
        ExitProcess(1);
    }

    char asciiName[1024];
    DWORD usernameLen = lstrlenW(username);
    to_upper_ascii(username, asciiName, usernameLen);

    char expectedAAAA[5];
    for (DWORD i = 0; i < 4; ++i) {
        expectedAAAA[i] = asciiName[i];
    }
    expectedAAAA[4] = '\0';


    char expectedBBBB[5];
    to_hex_string((asciiName[0] << 8) | asciiName[1], expectedBBBB, 4);

    char base64Output[16];
    base64_encode(asciiName, usernameLen, base64Output);
    char expectedCCCC[5];
    for (DWORD i = 0; i < 4; ++i) {
        expectedCCCC[i] = base64Output[i];
    }
    expectedCCCC[4] = '\0';

    char expectedDDDD[5];
    for (DWORD i = 0; i < 4; ++i) {
        char xoredChar = asciiName[i] ^ 0x4;
        if (xoredChar >= 'a' && xoredChar <= 'z') {
            xoredChar -= 32; // Convert to uppercase
        }
        expectedDDDD[i] = xoredChar;
    }
    expectedDDDD[4] = '\0';

    char expectedKey[37];
    wsprintfA(expectedKey, "%s-%s-%s-%s", expectedAAAA, expectedBBBB, expectedCCCC, expectedDDDD);

    char enteredKey[1024];
    DWORD keyLen = lstrlenW(key);
    for (DWORD i = 0; i < keyLen; ++i) {
        enteredKey[i] = (char)key[i];
    }
    enteredKey[keyLen] = '\0';

    //PRINT(L"Expected AAAA: %S\n", expectedAAAA);

    //// Debugging BBBB
    //PRINT(L"Expected BBBB: %S\n", expectedBBBB);

    //// Debugging CCCC
    //PRINT(L"Expected CCCC: %S\n", expectedCCCC);

    //// Debugging DDDD
    //PRINT(L"Expected DDDD: %S\n", expectedDDDD);

    //// Debugging full key
    //PRINT(L"Expected Key: %S\n", expectedKey);
    //PRINT(L"Entered Key: %S\n", enteredKey);

    if (lstrcmpA(expectedKey, enteredKey) == 0) {
        PRINT(L"Key is valid!\n");
    }
    else {
        PRINT(L"Invalid key.\n");
    }

    HeapFree(GetProcessHeap(), 0, username);
    HeapFree(GetProcessHeap(), 0, key);

    ExitProcess(0);
}
