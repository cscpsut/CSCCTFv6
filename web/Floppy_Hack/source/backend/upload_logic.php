<?php
// Set the upload directory
$uploadDir = '../uploads/';
$uploadedFile = $_FILES['file'];

// Function to validate file magic bytes (e.g., JPEG signature)
function isValidJPEG($filePath) {
    $file = fopen($filePath, 'rb');
    $header = fread($file, 8); // Read the first 8 bytes
    fclose($file);

    // Look for JPEG magic bytes in the first 8 bytes
    return strpos($header, "\xFF\xD8\xFF") !== false;
}

// Validate the file upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($uploadedFile)) {
    if ($uploadedFile['error'] === UPLOAD_ERR_OK) {
        $filePath = $uploadedFile['tmp_name'];

        // Validate MIME type using getimagesize
        $imageSize = getimagesize($filePath);
        if ($imageSize !== false && $imageSize['mime'] === 'image/jpeg') {
            // Validate magic bytes
            if (isValidJPEG($filePath)) {
                $destination = $uploadDir . basename($uploadedFile['name']);
                if (move_uploaded_file($filePath, $destination)) {
                    // Successful upload
                    $uploadedFilePath = $uploadDir . basename($uploadedFile['name']);
                    echo "File uploaded successfully!<br>";
                    echo "<a href='{$uploadedFilePath}' target='_blank'>Click here to view your uploaded image</a>";
                    exit;
                }
            }
        }
    }
}

// Default response for invalid files
echo "Not a valid JPEG file.";
?>
