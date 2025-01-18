<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Windows XP</title>
    <link rel="stylesheet" href="assets/styles/style.css">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <header></header>
    <main>
        <div class="img">
            <img src="assets/images/logo.png" alt="Windows XP Logo" />
            <h1>To begin, click your user name</h1>
        </div>
        <div class="line"></div>
        <div class="users">
            <section class="guest">
                <div class="iconA"></div>
                <div class="user">
                    <h3>Guest</h3>
                    <p>Type your password</p>
                    <div class="input">
                        <input type="password">
                        <button class="green">
                            <img src="assets/images/Vector_(1).png" alt="">
                        </button>
                        <button class="blue">
                            <img src="assets/images/_.png" alt="">
                        </button>
                    </div>
                </div>
            </section>
        </div>
    </main>
    <footer>
        <div class="btn">
            <button>
                <img src="assets/images/Group_2.png" alt="">
            </button>
            <p>Turn off computer</p>
        </div>
        <div class="informations">
            <p>After you log on, you can add or change accounts</p>
            <p>Just go to your Control Panel and click User Accounts</p>
        </div>
    </footer>
    <script>
        // Redirect to upload page on clicking "Guest"
        document.querySelector('.guest').addEventListener('click', function () {
            window.location.href = "upload.php";
        });
    </script>
</body>
</html>
