const express = require('express');
const merge = require('merge-objects');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
require('express-async-errors');

const app = express();
const PORT = 3000;

const ADMIN_TOKEN = uuidv4(); // randomized
console.log(ADMIN_TOKEN);
app.set('view engine', 'ejs');


app.use(express.json());

// clear __proto__ remove in dist


app.use((req, res, next) => {

  const o = Object();

  for (const k in o.__proto__) {
    if (k !== undefined) {
      console.log(`deleting ${k}`);
      delete o.__proto__[k];
    }
  }
  next();
});

/* Mi solucion xD
const { body, validationResult } = require('express-validator');

// Middleware para validar las propiedades del objeto de solicitud
const validateRequest = [
  body().custom((value, { req }) => {
    // Eliminar propiedades adicionales del objeto de solicitud
    delete req.body.__proto__;
    delete req.params.__proto__;
    delete req.query.__proto__;
    return true;
  }),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  }
];

app.use(express.json());

// Aplicar middleware de validación en todas las rutas
app.use(validateRequest);
*/


// check auth
app.use(function (req, res, next) {
  if (req.query.token && req.query.token === ADMIN_TOKEN) res.locals.adminLogged = true;
  next();
});

app.get('/', async (req, res) => {
  res.render('index');
});

app.get('/hi', async (req, res) => {
  res.render('present_form');
});

app.post('/hi', async (req, res) => {
  // default values
  
  let user = {
    name: 'random visitor',
    hobby: 'sleeping',
    age: '18'
  };
   var sexo = "anal";

  merge(user, req.body);

  console.log({user});
  console.log(ADMIN_TOKEN);
  console.log(res.locals )
  //res.render('present_result', { user });
  res.render('present_result', {user} );

    console.log(sexo);


});

app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
