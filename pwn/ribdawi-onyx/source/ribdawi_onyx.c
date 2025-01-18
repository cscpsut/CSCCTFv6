#include <stdio.h>
#include <string.h>
#include <openssl/aes.h>

void pwn_jail(){
    void banner(){


puts("         .::::::::::.        -(_)====u         .::::::::::.");
puts("       .::::''''''::::.                      .::::''''''::::.");
puts("    .:::'          `::::....           ....::::'          `:::.");
puts("    .::'             `:::::::|         |:::::::'             `::.");
puts("    .::|               |::::::|_ ___ __|::::::|               |::. ");
puts("    `--'               |::::::|_()__()_|::::::|               `--'");
puts("    :::               |::-o::|         |::o-::|               :::");
puts("    `::.             .|::::::|         |::::::|.             .::'");
puts("    `:::.          .::/------'         `-----/::.          .:::'");
puts("        `::::......::::'                         `::::......::::'");
puts("      `::::::::::'                           `::::::::::'\n\n\n");



return;
}
int main(int argc, char const *argv[]){

    setup(); 
    banner();
    
    
    printf("This is your prisoner id  : %p\n",&printf);
    int a=0x1337,b=0xc0d3;
    char msg[40];
    read(0,msg,40);
    scanf(msg,&a,&b);
    puts(msg);
    
}


    
}




unsigned char decrypt_aes(const unsigned char *ciphertext, const unsigned char *key, const unsigned char *iv, size_t ciphertext_len) {
    unsigned char plaintext[256];
    AES_KEY decryptKey;
    int padding_len = 0;
    int plaintext_len = 0;
    AES_set_decrypt_key(key, 128, &decryptKey); // Set the AES decryption key (128-bit in this example)
    AES_cbc_encrypt(ciphertext, plaintext, ciphertext_len, &decryptKey, (unsigned char *)iv, AES_DECRYPT);
    plaintext_len = ciphertext_len - ciphertext_len % AES_BLOCK_SIZE;
    printf("Plaintext length: %d\n", ciphertext_len);
    printf(plaintext);
    padding_len  = plaintext[plaintext_len - 1];


    if (padding_len <= 0 || padding_len > AES_BLOCK_SIZE) {
        printf("Invalid padding\n");
        return -1;
    }
    pwn_jail();

    return  plaintext;

}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
     // Buffer for decrypted plaintext
    unsigned char key[16] = "examplekey123456"; // 16 bytes for AES-128
    unsigned char iv[16] = "initialvector123";  // 16 bytes initialization vector

    char ciphertext_input[512];
    printf("Enter ciphertext (hexadecimal format): ");
    scanf("%512s", ciphertext_input);

    // Convert the input ciphertext from hex to bytes
    size_t len = strlen(ciphertext_input) / 2;
    unsigned char ciphertext[len];
    for (size_t i = 0; i < len; i++) {
        sscanf(&ciphertext_input[i * 2], "%2hhx", &ciphertext[i]);
    }
    


    decrypt_aes(ciphertext,  key, iv, len);
    



    return 0;
}