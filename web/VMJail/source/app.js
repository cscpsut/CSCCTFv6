const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const pug = require('pug');
const vm = require('vm');
const PORT = 3000;
 
var urlencodedParser = bodyParser.urlencoded({ extended: true });
const app = express();
 
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');
app.use(express.static(path.join(__dirname, 'views')));
 
app.get('/', function (req, res, next) {
    res.send(pug.renderFile(path.join(__dirname, 'views/index.pug'), { code: '', result: '' }));
});
 
app.post('/', urlencodedParser, function (req, res) {
    const code = req.body.code + '';
    if (code.length != 0) {
        try {
            // vm with empty context
            data = vm.runInNewContext(
                code,
                vm.createContext(Object.create(null)),
                { timeout: 600 }
            );
            if (data !== undefined) {
                if (data['result'] !== undefined) {
                    result = {result: data['result']};
                } else {
                    result = {result: data};
                }
            } else {
                result = {result: "undefined"};
            }
        } catch (err) {
            result = {result: err};
        }
    } else {
        result = {result: 'Empty code'};
    }
 
    try {
        res.send(
            pug.renderFile(
                path.join(__dirname, 'views/index.pug'), {
                    code: code,
                    result: result['result']
                }
            )
        );
    } catch (err) {
        res.send(
            pug.renderFile(
                path.join(__dirname, 'views/index.pug'),
                { code: code, result: err }
            )
        );
    }
});
 
app.get('/css/style.css', function (req, res) {
    res.sendFile(path.join(__dirname, 'css/style.css'));
});
 
app.listen(PORT, function () {
    console.log('Challenge listening on port ' + PORT);
});

