// Inicializa Firebase Messaging
const messaging = firebase.messaging();

// Solicitar permiso para recibir notificaciones (Esto es opcional si ya lo hiciste)
messaging.requestPermission().then(function () {
    return messaging.getToken();
}).then(function (token) {
    console.log('Token:', token);
    // Guarda el token en tu backend si es necesario
}).catch(function (err) {
    console.log('Error al obtener el permiso:', err);
});

// Código existente...
document.getElementById('notifyBtn').addEventListener('click', function () {
    console.log("Botón clickeado");

    if (!("Notification" in window)) {
        alert("Este navegador no soporta notificaciones de escritorio.");
        return;
    }

    if (Notification.permission === "granted") {
        console.log("Permiso ya concedido");
        showNotification();
    } else if (Notification.permission !== "denied") {
        console.log("Solicitando permiso para notificaciones");
        Notification.requestPermission().then(function (permission) {
            if (permission === "granted") {
                showNotification();
            }
        });
    }
});

function showNotification() {
    console.log("Mostrando notificación");

    var options = {
        body: "Haz clic para ver la tabla de datos.",
        icon: "icon.png",  // Asegúrate de que 'icon.png' esté en el directorio correcto
        tag: "alerta-1",
        data: {
            url: "tabla.html"
        }
    };

    var notification = new Notification("¡Alerta!", options);

    notification.onclick = function (event) {
        event.preventDefault();
        window.open(notification.data.url);
    };
}
