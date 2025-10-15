var accion = "nuevo",
    idProducto = 0;

document.addEventListener("DOMContentLoaded", event => { 
    frmProductos.addEventListener("submit", e => {
        e.preventDefault();
        guardarProductos();
    });
    obtenerProductos();
});

async function guardarProductos(){
    let datos = {
        accion,
        idProducto,
        nombre: txtNombreProducto.value,
        descripcion: txtDescripcionProducto.value,
        precio: txtPrecioProducto.value,
        categoria: txtCategoriaProducto.value,
        estado: txtEstadoProducto.value,
        imagen: txtImagenProducto.value
    };
    let response = await fetch("/productos", {
        method: "POST",
        body: JSON.stringify(datos),
    }),
    respuesta = await response.json();

    if(respuesta.msg != "ok"){
        alertify.error(`Error al procesar producto: ${respuesta}`);
        return;
    }
    limpiarFormulario();
    obtenerProductos();
}

function limpiarFormulario(){
    accion = "nuevo";
    idProducto = 0;
    txtNombreProducto.value = "";
    txtDescripcionProducto.value = "";
    txtPrecioProducto.value = "";
    txtCategoriaProducto.value = "";
    txtEstadoProducto.value = "";
    txtImagenProducto.value = "";
}

async function obtenerProductos(){
    let response = await fetch("/productos"),
        respuesta = await response.json();
    mostrarDatosProductos(respuesta);
}

function mostrarDatosProductos(productos){
    let filas = "";
    productos.forEach(producto => {
        filas += `
            <tr onClick='mostrarProducto(${ JSON.stringify(producto) })'>
                <td>${producto.nombre}</td>
                <td>${producto.descripcion}</td>
                <td>${producto.precio}</td>
                <td>${producto.categoria}</td>
                <td>${producto.estado}</td>
                <td>${producto.imagen}</td>
                <td><button onClick='eliminarProducto(${ JSON.stringify(producto) }, event)' class="btn btn-danger btn-sm">ELIMINAR</button></td>
            </tr>
        `;
    });
    tblProductos.innerHTML = filas;
}

function mostrarProducto(producto){
    accion = "modificar";
    idProducto = producto.idProducto;
    txtNombreProducto.value = producto.nombre;
    txtDescripcionProducto.value = producto.descripcion;
    txtPrecioProducto.value = producto.precio;
    txtCategoriaProducto.value = producto.categoria;
    txtEstadoProducto.value = producto.estado;
    txtImagenProducto.value = producto.imagen;
}

function eliminarProducto(producto, event){
    event.preventDefault();

    if(confirm(`¿Está seguro de eliminar el producto ${producto.nombre}?`)){
        idProducto = producto.idProducto;
        accion = "eliminar";
        guardarProductos();
        alertify.success('Producto eliminado correctamente');
    }
}