const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

const JWKS_URI = 'http://127.0.0.1:1337/.well-known/jwks.json';
const KEY_ID = uuidv4();

let privateKey = null;
let jwks = null;

const generateKeys = async () => {
    const { privateKey: generatedPrivateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
        modulusLength: 2048,
        publicKeyEncoding: { type: 'spki', format: 'pem' },
        privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
    });

    const publicKeyObject = crypto.createPublicKey(publicKey);
    const publicJwk = publicKeyObject.export({ format: 'jwk' });

    const jwk = {
        kty: 'RSA',
        ...publicJwk,
        alg: 'RS256',
        use: 'sig',
        kid: KEY_ID,
    };

    jwks = {
        keys: [jwk],
    };

    privateKey = generatedPrivateKey;
};

const getPrivateKey = async () => {
    if (!privateKey) {
        throw new Error('Private key not found in memory. Generate keys first.');
    }
    return privateKey;
};

const getJWKS = async () => {
    if (!jwks) {
        throw new Error('JWKS not found in memory. Generate keys first.');
    }
    return jwks;
};

const createToken = async (payload) => {
    const privateKey = await getPrivateKey();
    return jwt.sign(payload, privateKey, {
        algorithm: 'RS256',
        header: {
            kid: KEY_ID,
            jku: JWKS_URI,
        },
    });
};

const verifyToken = async (token) => {
    try {
        const decodedHeader = jwt.decode(token, { complete: true });

        if (!decodedHeader || !decodedHeader.header) {
            throw new Error('Invalid token: Missing header');
        }

        const { kid, jku } = decodedHeader.header;

        if (!jku) {
            throw new Error('Invalid token: Missing header jku');
        }

        if (!jku.startsWith('http://127.0.0.1:1337/')) {
            throw new Error('Invalid token: jku claim does not start with http://127.0.0.1:1337/');
        }

        if (!kid) {
            throw new Error('Invalid token: Missing header kid');
        }

        if (kid !== KEY_ID) {
            throw new Error('Invalid token: kid does not match the expected key ID');
        }

        let jwks;
        try {
            const response = await axios.get(jku);
            if (response.status !== 200) {
                throw new Error(`Failed to fetch JWKS: HTTP ${response.status}`);
            }
            jwks = response.data;
        } catch (error) {
            throw new Error(`Error fetching JWKS from jku: ${error.message}`);
        }

        if (!jwks || !Array.isArray(jwks.keys)) {
            throw new Error('Invalid JWKS: Expected keys array');
        }

        const jwk = jwks.keys.find((key) => key.kid === kid);
        if (!jwk) {
            throw new Error('Invalid token: kid not found in JWKS');
        }

        if (jwk.alg !== 'RS256') {
            throw new Error('Invalid key algorithm: Expected RS256');
        }

        if (!jwk.n || !jwk.e) {
            throw new Error('Invalid JWK: Missing modulus (n) or exponent (e)');
        }

        const publicKey = jwkToPem(jwk);

        const decoded = jwt.verify(token, publicKey, { algorithms: ['RS256'] });
        return decoded;
    } catch (error) {
        console.error(`Token verification failed: ${error.message}`);
        throw error;
    }
};

const jwkToPem = (jwk) => {
    if (jwk.kty !== 'RSA') {
        throw new Error("Invalid JWK: Key type must be 'RSA'");
    }

    const key = {
        kty: jwk.kty,
        n: jwk.n.toString('base64url'),
        e: jwk.e.toString('base64url'),
    };

    const pem = crypto.createPublicKey({
        key,
        format: 'jwk',
    });

    return pem.export({ type: 'spki', format: 'pem' });
};

module.exports = {
    generateKeys,
    getJWKS,
    createToken,
    verifyToken,
};