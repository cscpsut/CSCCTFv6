const express = require('express');
const jwt = require('jsonwebtoken');
const path = require('path');
const cookieParser = require('cookie-parser');
const morgan = require('morgan');

const app = express();
app.use(cookieParser());
app.use(morgan('combined')); // Add morgan middleware for logging

const FLAG = process.env.FLAG || 'CSCCTF{FAKE_FLAG_FOR_TESTING}';
const SECRET_KEY = 'reddington';

app.use(express.static(path.join(__dirname, 'static')));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.get('/', (req, res) => {
    const token = jwt.sign(
        {
            user: 'guest',
            exp: Math.floor(Date.now() / 1000) + (30 * 60),
        },
        SECRET_KEY,
        { algorithm: 'HS256' }
    );
    res.cookie('token', token);
    res.redirect('/main.html');
});

app.get('/admin', (req, res) => {
    const token = req.cookies.token;
    if (!token) {
        return res.status(403).render('AccessDenied');
    }
    try {
        const data = jwt.verify(token, SECRET_KEY, { algorithms: ['HS256'] });
        if (data.user === 'admin') {
            return res.render('admin', { flag: FLAG });
        }
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(403).json({ message: 'Token has expired' });
        }
        return res.status(403).json({ message: 'Invalid token' });
    }
    return res.status(403).render('AccessDenied');
});

app.listen(1337, '0.0.0.0', () => {
    console.log('Server running on http://0.0.0.0:1337');
});