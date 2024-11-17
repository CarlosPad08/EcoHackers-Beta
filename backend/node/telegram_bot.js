const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
//const datos = JSON.parse(fs.readFileSync('../pyhton/database/analisis_calidad_aire.json', 'utf-8'));
const datos = JSON.parse(fs.readFileSync('../pyhton/database/pronostico_semanal.json', 'utf-8'));

// 'TOKEN'
const bot = new TelegramBot('7634065879:AAHLn8X2XWf4LBuG7-l9EJ8GECGatK_Ru-0', { polling: true });

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const welcomeMessage = `¡Hola ${fullName}! Soy AIre bienestar, tu asistente que te ayuda a preparate para respirar tranquilamente en la ciudad. \n\n ¿Cómo puedo ayudarte? Prueba preguntar por los pronósticos de calidad de aire.`;
    bot.sendMessage(chatId, welcomeMessage);
});

// Función para buscar el pronóstico en la base de datos
function buscarPronostico(fecha) {
    return datos.find((item) => item.fecha === fecha);
};

// Manejar mensajes
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id; // ID del usuario
    const userName = msg.from.first_name || 'Usuario'; // Nombre del usuario
    const userLastName = msg.from.last_name || ''; // Apellido (si está disponible)
    const fullName = `${userName} ${userLastName}`.trim(); // Nombre completo
    const palabrasClave = ["calidad del aire para hoy", "pronostico para hoy", "pronosticos para hoy", "pronostico del dia", "estado del aire hoy", "calidad del aire hoy", "condiciones para hoy", "prediccion para hoy", "estado ambiental del dia", "prevision de calidad hoy", "como esta el aire hoy", "aire del dia", "que tal el aire hoy", "condiciones ambientales hoy", "nivel de contaminacion hoy", "calidad ambiental actual", "pronostico ambiental diario", "aire limpio hoy", "estado del ambiente hoy", "que esperar hoy", "predicciones del aire para hoy", "situacion ambiental hoy"];
    const palabrasClavePrediccionManana = ["calidad del aire para mañana", "pronostico para mañana", "pronosticos para mañana", "pronostico del dia siguiente", "estado del aire mañana", "calidad del aire mañana", "condiciones para mañana", "prediccion para mañana", "estado ambiental del dia siguiente", "prevision de calidad mañana", "como esta el aire mañana", "aire del dia siguiente", "que tal el aire mañana", "condiciones ambientales mañana", "nivel de contaminacion mañana", "calidad ambiental siguiente", "pronostico ambiental diario siguiente", "aire limpio mañana", "estado del ambiente mañana", "que esperar mañana", "predicciones del aire para mañana", "situacion ambiental mañana"];

    const text = msg.text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");;
  
    // Responder si el mensaje contiene palabras clave
    if (palabrasClave.some((palabra) => text.includes(palabra))) {
      const fechaHoy = new Date().toISOString().split('T')[0]; // Fecha actual en formato YYYY-MM-DD
      const resultado = buscarPronostico(fechaHoy);
  
      if (resultado) {
        bot.sendMessage(
          chatId,
          `Hola ${fullName}, para el día de hoy ${fechaHoy} tenemos los siguientes pronósticos:\n\n` +
          `Índice de calidad del aire: ${resultado.categoria_predicha}\n` +
          `${resultado.detalle}\n` +
          `${resultado.recomendaciones}`
        );
      } else {
        bot.sendMessage(chatId, `Hola ${fullName}, lo siento, no encontré pronósticos para hoy (${fechaHoy}).`);
      }
    } else {
      bot.sendMessage(chatId, `${userName}, te puedo dar informacion a cerca de la calidad del aire en la ciudad de Cali, prueba enviandome un mensaje con algo como "¿Calidad del aire para hoy?" o "Pronostico para hoy sobre la calidad del aire".`);
    }

    // Responder si el mensaje contiene palabras clave
    if (palabrasClavePrediccionManana.some((palabra) => text.includes(palabra))) {
      const fechaHoy = new Date().toISOString().split('T')[0]; // Fecha actual en formato YYYY-MM-DD

      // Convertir fechaHoy a un objeto Date
      const fecha = new Date(fechaHoy);

      // Sumar un día
      fecha.setDate(fecha.getDate() + 1);

      // Formatear la fecha resultante en formato YYYY-MM-DD
      const fechaManana = fecha.toISOString().split('T')[0];

      const resultado = buscarPronostico(fechaManana);
  
      if (resultado) {
        bot.sendMessage(
          chatId,
          `Hola ${fullName}, para el día de mañana ${fechaManana} tenemos los siguientes pronósticos:\n\n` +
          `Índice de calidad del aire: ${resultado.categoria_predicha}\n` +
          `${resultado.detalle}\n` +
          `${resultado.recomendaciones}`
        );
      } else {
        bot.sendMessage(chatId, `Hola ${fullName}, lo siento, no encontré pronósticos para hoy (${fechaHoy}).`);
      }
    } else {
      bot.sendMessage(chatId, `${userName}, te puedo dar informacion a cerca de la calidad del aire en la ciudad de Cali, prueba enviandome un mensaje con algo como "¿Calidad del aire para hoy?" o "Pronostico para hoy sobre la calidad del aire".`);
    }
});

// Función para enviar un mensaje
function sendMessage(chatId, message) {
  bot.sendMessage(chatId, message);
}
