$(document).ready(function () {

    $('.dropDownBtn').on('click', function() {

        let icon = $(this).find('.bi-caret-right-fill');

        if(icon.hasClass('opened')){
            icon.removeClass('opened');
            icon.addClass('closed');
        }else{
            icon.removeClass('closed');
            icon.addClass('opened');
        }
    
    });

});




/**
 * Función para simplificar peticiones ajax
 * @author Luis GP
 * @param {
 *  url: string,
 *  method: string,
 *  body: FormData,
 *  success: function,
 *  error: function
 * } json 
 */
const ajax = (json) => {

    try {

        fetch(urlBase+json.url, {
            method: json.method ? json.method : "POST",
            headers: {
                'X-CSRFToken': csrfToken
            },
            mode: 'same-origin',
            body: json.body ? json.body : null
        })
        .then(response => response.json())
        .then(data => {
            
            if(data.code == 200){
                json.success(data)
            }else if(data.code == 500){
                json.error(data)
            }else{
                json.complete(data);
            }
    
        })
        .catch(error => {
            
            if(json.catch){
                json.catch(error);
            }else{
                console.error(error);
            }
            
        })
        
    } catch (error) {
        console.error(error);
    }

}



/**
 * Funcion para mostrar una alerta en caso de que algo haya salido bien
 * @author Luis Godínez
 * @param {JSON} data 
 */
const alertSuccess = (data) => {

    document.getElementById('modal-content').classList.remove('modal-bg-danger');
    document.getElementById('modal-content').classList.add('modal-bg-success');
    document.getElementById('alert-body-message').innerHTML = `<div class="text-center">${data.message}</div>`;

    $("#modal-alert").modal('show');

}





/**
 * Función para mostrar una alerta en caso de que algo haya salido mal
 * @author Luis Godínez
 * @param {*} data 
 */
const alertError = (data) => {

    document.getElementById('modal-content').classList.remove('modal-bg-success');
    document.getElementById('modal-content').classList.add('modal-bg-danger');
    document.getElementById('alert-body-message').innerHTML = `<div class="text-center">${data.message}</div>`;

    $("#modal-alert").modal('show');

}



/**
 * Función para formatear un número en dinero
 * @param {string} numero 
 * @returns {string}
 */
const formatoDinero = (numero) => {

    return numero.toLocaleString("en", {
        style: "currency",
        currency: "MXN"
    });

}




/**
 * Función para mostrar los productos del carrito de compras
 * @author Luis GP
 * @return {json}
 */
const cargarMiniCarrito = () => {

    try {
        
        ajax({
            url: '/api/v1/carrito',
            method: "GET",
            complete: (response) => {
                let carritoBody = document.getElementById("mini_carrito-body");
                
                let html = '<div class="mini-carrito-content">';
                let total = 0;

                console.log(response)

                for(let i of response[0].detalles){
                    let subtotal = parseFloat(i.producto.precio_venta) * parseInt(i.cantidad);
                    html += `<div class="row">
                        <div class="col-5"><img class="img-fluid" src="${i.imagenproducto.imagen}"/></div>
                        <div class="col-7">
                            <h4 class="fw-bold">${i.producto.nombre}</h4>
                            <p class="m-0">
                                <small>Talla: <span>${i.talla.talla}</span></small>
                            </p>
                            <p class="m-0">
                                <small>Código: <span>${i.producto.codigo}</span></small>
                            </p>
                            <p>
                                <small>${i.cantidad} pza.</small>
                            </p>
                            <h4 class="fw-bold">${formatoDinero(subtotal)}</h4>
                        </div>
                    </div><hr>`;
                    total += subtotal;
                }

                html += `</div>
                <div>
                    <h3 class="d-flex justify-content-between">Total: <span>${formatoDinero(total)}</span></h3>
                    <button class="btn btn-info w-100 mt-3 text-uppercase">Proceder con el pago</button>
                    <a href="${urlBase}/carrito/" class="btn btn-primary w-100 mt-1 text-uppercase">Ir al carrito</a>
                </div>`;

                carritoBody.innerHTML = html;

            },
            catch: (error) => {
                console.error(error)
                document.getElementById("mini_carrito-body").innerHTML = `<div class="h-100 d-flex justify-content-center align-items-center">
                    <p class="lead">El carrito esta vacío</p>
                </div>`;
            }
        });

    } catch (error) {
        
        console.error(error);
    }

    return false;

}




/**
 * Función para actualizar el total por producto del carrito
 * @author Luis GP
 * @returns 
 */
const actualizarPrecioProductoCarrito = (select) => {

    try {

        const idDetalle = select.dataset.id_detalle;
        const data = new FormData()
        
        data.append('cantidad', select.value)

        ajax({
            url: `/api/v1/detallecarrito/${idDetalle}/`,
            method: 'PUT',
            body: data,
            complete: (data) => {
                const totalField = document.getElementById('total_producto-'+idDetalle);
                totalField.innerHTML = formatoDinero(data.cantidad*data.producto.precio_venta);
            },
            error: (error) => {
                console.log(error)
            }
        })
        
    } catch (error) {
        console.error(error);
    }

    return false;

}