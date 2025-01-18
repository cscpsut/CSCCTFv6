const express = require('express');
const jwt = require('jsonwebtoken');
const path = require('path');
const cookieParser = require('cookie-parser');
const https = require('https');
const fs = require('fs');

const app = express();
app.use(cookieParser());

const FLAG = process.env.FLAG || 'CSCCTF{FAKE_FLAG_FOR_TESTING}';

// algs
const verify_alg = ["HS256", "RS256"];
const sign_alg = "RS256";

// keys
const private_key = fs.readFileSync('./keys/priv.key', 'utf8');

const public_key = fs.readFileSync('./keys/pubkeyrsa.pem', 'utf8');
const certificate = fs.readFileSync('./keys/fullchain.pem', 'utf8');

app.use(express.static(path.join(__dirname, 'static')));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.get('/', (req, res) => {
    const token = jwt.sign(
        {
            user: 'guest',
            exp: Math.floor(Date.now() / 1000) + (30 * 60),
        },
        private_key,
        { algorithm: sign_alg }
    );
    console.log(token);
    res.cookie('token', token);
    res.redirect('/main.html');
});

app.get('/admin', (req, res) => {
    const token = req.cookies.token;
    if (!token) {
        return res.status(403).render('AccessDenied');
    }
    try {
        const data = jwt.verify(token, public_key, { algorithms: verify_alg });
        if (data.user === 'admin') {
            return res.render('admin', { flag: FLAG });
        }
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(403).json({ message: 'Token has expired' });
        }
        return res.status(403).json({ message: err });
    }
    return res.status(403).render('AccessDenied');
});


https.createServer({
    key: fs.readFileSync('./keys/priv.key'),
    cert: fs.readFileSync('./keys/fullchain.pem')
}, app).listen(1337, '0.0.0.0', () => {
    console.log('Server running on https://0.0.0.0:1337');
});