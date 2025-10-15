var accion = "nuevo",
    idPedido = 0;

document.addEventListener("DOMContentLoaded", event => { 
    frmPedidos.addEventListener("submit", e => {
        e.preventDefault();
        guardarPedidos();
    });
    obtenerPedidos();
});

async function guardarPedidos(){
    let datos = {
        accion,
        idPedido,
        idCliente: txtIdCliente.value,
        productos: txtProductos.value,
        total: txtTotal.value,
        fecha: txtFecha.value,
        estado: txtEstado.value,
        observaciones: txtObservaciones.value
    };
    let response = await fetch("/pedidos", {
        method: "POST",
        body: JSON.stringify(datos),
    }),
    respuesta = await response.json();

    if(respuesta.msg != "ok"){
        alertify.error(`Error al procesar pedido: ${respuesta}`);
        return;
    }
    limpiarFormulario();
    obtenerPedidos();
}

function limpiarFormulario(){
    accion = "nuevo";
    idPedido = 0;
    txtIdCliente.value = "";
    txtProductos.value = "";
    txtTotal.value = "";
    txtFecha.value = "";
    txtEstado.value = "";
    txtObservaciones.value = "";
}

async function obtenerPedidos(){
    let response = await fetch("/pedidos"),
        respuesta = await response.json();
    mostrarDatosPedidos(respuesta);
}

function mostrarDatosPedidos(pedidos){
    let filas = "";
    pedidos.forEach(pedido => {
        filas += `
            <tr onClick='mostrarPedido(${ JSON.stringify(pedido) })'>
                <td>${pedido.idCliente}</td>
                <td>${pedido.productos}</td>
                <td>${pedido.total}</td>
                <td>${pedido.fecha}</td>
                <td>${pedido.estado}</td>
                <td>${pedido.observaciones}</td>
                <td><button onClick='eliminarPedido(${ JSON.stringify(pedido) }, event)' class="btn btn-danger btn-sm">ELIMINAR</button></td>
            </tr>
        `;
    });
    tblPedidos.innerHTML = filas;
}

function mostrarPedido(pedido){
    accion = "modificar";
    idPedido = pedido.idPedido;
    txtIdCliente.value = pedido.idCliente;
    txtProductos.value = pedido.productos;
    txtTotal.value = pedido.total;
    txtFecha.value = pedido.fecha;
    txtEstado.value = pedido.estado;
    txtObservaciones.value = pedido.observaciones;
}

function eliminarPedido(pedido, event){
    event.preventDefault();

    if(confirm(`¿Está seguro de eliminar el pedido ${pedido.idPedido}?`)){
        idPedido = pedido.idPedido;
        accion = "eliminar";
        guardarPedidos();
    }
}
