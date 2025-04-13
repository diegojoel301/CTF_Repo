
/*let a = ["hi", "bye"];
console.log(a);
a.confuse();
console.log(a);
a.confuse();
console.log(a);
*/

// Creamos un ArrayBuffer para representar un bloque de memoria
let buffer = new ArrayBuffer(16); // 16 bytes de espacio
let view = new DataView(buffer); // Usamos DataView para leer y escribir datos de forma binaria

// Sobreescribimos el prototipo de ArrayBuffer
ArrayBuffer.prototype.confuse = function() {
    // Simulamos la alteración de la memoria escribiendo directamente en el buffer
    this[0] = 0xdeadbeef;  // Escribimos un valor arbitrario en el primer byte del buffer
    this[1] = 0xdeadbeef;  // Escribimos el mismo valor en la siguiente posición
};

// Activamos la vulnerabilidad en el ArrayBuffer
buffer.confuse();

// Mostramos el contenido del buffer (esto solo es posible con herramientas avanzadas como el navegador DevTools)
console.log(view.getUint32(0, true).toString(16));  // Imprimimos el valor del primer "byte"
console.log(view.getUint32(4, true).toString(16));  // Imprimimos el valor del siguiente "byte"
