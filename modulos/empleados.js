var accion = "nuevo",
    idEmpleado = 0;

document.addEventListener("DOMContentLoaded", event => { 
    frmEmpleados.addEventListener("submit", e => {
        e.preventDefault();
        guardarEmpleados();
    });
    obtenerEmpleados();
});

async function guardarEmpleados(){
    let datos = {
        accion,
        idEmpleado,
        nombre: txtNombreEmpleado.value,
        cargo: txtCargoEmpleado.value,
        email: txtEmailEmpleado.value,
        telefono: txtTelefonoEmpleado.value,
        usuario: txtUsuarioEmpleado.value,
        contrasena: txtContrasenaEmpleado.value,
        estado: txtEstadoEmpleado.value
    };
    let response = await fetch("/empleados", {
        method: "POST",
        body: JSON.stringify(datos),
    }),
    respuesta = await response.json();

    if(respuesta.msg != "ok"){
        alertify.error(`Error al procesar empleado: ${respuesta}`);
        return;
    }
    limpiarFormulario();
    obtenerEmpleados();
}

function limpiarFormulario(){
    accion = "nuevo";
    idEmpleado = 0;
    txtNombreEmpleado.value = "";
    txtCargoEmpleado.value = "";
    txtEmailEmpleado.value = "";
    txtTelefonoEmpleado.value = "";
    txtUsuarioEmpleado.value = "";
    txtContrasenaEmpleado.value = "";
    txtEstadoEmpleado.value = "";
}

async function obtenerEmpleados(){
    let response = await fetch("/empleados"),
        respuesta = await response.json();
    mostrarDatosEmpleados(respuesta);
}

function mostrarDatosEmpleados(empleados){
    let filas = "";
    empleados.forEach(empleado => {
        filas += `
            <tr onClick='mostrarEmpleado(${ JSON.stringify(empleado) })'>
                <td>${empleado.nombre}</td>
                <td>${empleado.cargo}</td>
                <td>${empleado.email}</td>
                <td>${empleado.telefono}</td>
                <td>${empleado.usuario}</td>
                <td>${empleado.estado}</td>
                <td><button onClick='eliminarEmpleado(${ JSON.stringify(empleado) }, event)' class="btn btn-danger btn-sm">ELIMINAR</button></td>
            </tr>
        `;
    });
    tblEmpleados.innerHTML = filas;
}

function mostrarEmpleado(empleado){
    accion = "modificar";
    idEmpleado = empleado.idEmpleado;
    txtNombreEmpleado.value = empleado.nombre;
    txtCargoEmpleado.value = empleado.cargo;
    txtEmailEmpleado.value = empleado.email;
    txtTelefonoEmpleado.value = empleado.telefono;
    txtUsuarioEmpleado.value = empleado.usuario;
    txtContrasenaEmpleado.value = empleado.contrasena;
    txtEstadoEmpleado.value = empleado.estado;
}

function eliminarEmpleado(empleado, event){
    event.preventDefault();

    if(confirm(`¿Está seguro de eliminar al empleado ${empleado.nombre}?`)){
        idEmpleado = empleado.idEmpleado;
        accion = "eliminar";
        guardarEmpleados();
        alertify.success('Empleado eliminado correctamente');
    }
}
