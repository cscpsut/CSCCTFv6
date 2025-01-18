<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Floppy Disk Upload</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/styles/upload.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="background d-flex align-items-center justify-content-center vh-100">
        <div class="floppy">
            <div class="top">
                <div class="slider"></div>
                <div class="fitinha"></div>
            </div>
            <div class="down">
                <div class="notes">
                    <p>Upload Floppy Disks</p>
                    <p>An advice, use only <span>JPEG</span></p>
                </div>
                <!-- Upload functionality -->
                <div class="upload-area mt-4">
                    <form method="POST" action="backend/upload_logic.php" enctype="multipart/form-data">
                        <input type="file" id="file-upload" name="file" class="form-control form-control-lg mb-3" required>
                        <button type="submit" class="btn btn-dark btn-lg w-100">
                            <i class="fas fa-save"></i> Upload
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
