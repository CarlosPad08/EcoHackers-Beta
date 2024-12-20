const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.post('/send-alert', (req, res) => {
  const { message } = req.body;
  //
  res.send(`Mensaje enviado: ${message}`);
});

app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
