const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const morgan = require('morgan');
const { generateKeys, createToken, getJWKS, verifyToken } = require('./jwtservice');

const app = express();
app.use(cookieParser());
app.use(morgan('combined')); // Add morgan middleware for logging

app.set('view cache', false); // Disable EJS caching globally

const FLAG = process.env.FLAG || 'CSCCTF{FAKE_FLAG_FOR_TESTING}';

app.use(express.static(path.join(__dirname, 'static')));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.get('/', async (req, res) => {
    if (!req.query.redirect) {
        const token = await createToken({
            user: 'guest',
            exp: Math.floor(Date.now() / 1000) + (30 * 60),
        });
        res.cookie('token', token);
        res.redirect('/main.html');
    } else {
        res.redirect(req.query.redirect);
    }
});

app.get('/.well-known/jwks.json', async (req, res) => {
    try {
        const jwks = await getJWKS();
        res.json(jwks);
    } catch (err) {
        console.error(err);
        res.status(500).send({ error: 'Could not retrieve JWKS' });
    }
});

app.get('/admin', async (req, res) => {
    const token = req.cookies.token;
    if (!token) {
        return res.status(403).render('AccessDenied');
    }
    try {
        const data = await verifyToken(token);
        if (data.user === 'admin') {
            return res.render('admin', { flag: FLAG });
        }
    } catch (err) {
        console.error(err);
        res.status(403).json({ message: err.message });
    }
    return res.status(403).render('AccessDenied');
});

generateKeys().then(() => {
    app.listen(1337, '0.0.0.0', () => {
        console.log('Server running on http://0.0.0.0:1337');
    });
}).catch(err => {
    console.error('Failed to generate keys:', err);
});