$(document).ready(function (e) {

    /**
     * Método que se ejecuta al abrir el modal de modal-eliminarProducto
     * @author Luis GP
     * @return void
     */
    $('#modal-eliminarProducto').on('show.bs.modal', function(e){
        $("#modal-eliminarProducto-id_producto").val($(e.relatedTarget).data('id_producto'));
        $("#modal-eliminarProducto-nombre").html($(e.relatedTarget).data('nombre'));
    });



    /**
     * Método que se ejecuta al abrir el modal de #modal-eliminarCategoria
     * @author Luis GP
     * @return void
     */
    $('#modal-eliminarCategoria').on('show.bs.modal', function(e){
        $("#modal-eliminarCategoria-id_categoria").val($(e.relatedTarget).data('id_categoria'));
        $("#modal-eliminarCategoria-nombre").html($(e.relatedTarget).data('nombre'));
    });



    /**
     * Método que se ejecuta al abrir el modal de modal-eliminarProductoImagen
     * @author Luis GP
     * @return void
     */
    $('#modal-eliminarProductoImagen').on('show.bs.modal', function(e){
        $("#modal-eliminarProductoImagen-id_imagen").val($(e.relatedTarget).data('id_imagen'));
    });

});




/**
 * Función para visualizar imagenes de los productos
 * @author Luis GP
 * @param {Elemnto DOM} inputFile 
 */
const previewImages = (inputFile) => {

    try {

        const files = inputFile.files;
        $(".imgNotSaved").remove();

        if (files) {
            for(let file of files){
                let src = URL.createObjectURL(file)
                $("#producto-imagenes-preview").append(
                    `<div class="col-lg-4 position-relative imgNotSaved">
                        <img src="${src}" class="img-fluid" />
                        <div class="hover-content hidden" onmouseover="showBack(this)" onmouseout="hideBack(this)">
                            <span class="badge bg-warning">Esta imagen no ha sido guardada</span>
                        </div>
                    </div>`
                );
            }

        }
        
    } catch (error) {
        console.error(e);
    }

}




/**
 * Función para habilitar el input para stock por talla
 * @author Luis GP
 * @param {Elemento DOM} checkbox
 * @returns {Boolean}
 */
const cambiarStock = (checkbox) => {

    try {

        let input = document.getElementById(checkbox.dataset.id_input);

        if(!checkbox.checked){
            document.getElementById(checkbox.dataset.id_input).value = 0;
            input.setAttribute('readonly', true);
            recalcularStock();
        }else{
            input.removeAttribute('readonly');
        }

    } catch (error) {
        console.error(error);
    }

    return false;

}




/**
 * Función que calcula el stock total por producto
 * @author Luis GP
 * @returns {Boolean}
 */
const recalcularStock = () => {

    try {
        
        let inputs = document.getElementsByClassName('input_stock');
        let total = 0;

        for(let i of inputs){
            total += parseInt(i.value);
        }

        document.getElementById('producto-stock').value = total;
        
    } catch (error) {
        console.error(error);
    }

    return false;

}





/**
 * Función para eliminar imagen de un producto
 * @author Luis GP
 * @returns {Boolean}
 */
const eliminarImagenProducto = () => {

    try {

        ajax({
            url: '/admin_panel/eliminar_imagen_producto/',
            method: 'POST',
            body: new FormData(document.getElementById('form-eliminarProductoImagen')),
            success: (response) => {
                $("#modal-eliminarProductoImagen").modal('hide');
                alertSuccess(response);
                $(`#productoImagenContent-${response.id_imagen}`).remove();
            },
            error: (err) => {
                console.log(err);
                $("#modal-eliminarProductoImagen").modal('hide');
                alertError(err);
            }
        });
        
    } catch (error) {
        console.error(error);
    }

    return false;

}



/**
 * Función para mostrar alternativo cuando se hace hover a un elemento
 * @author Luis GP
 * @returns {Boolean}
 */
const showBack = (div) => {

    try {
        
        $(div).removeClass('hidden');
        $(div).addClass('shown');

    } catch (error) {
        console.error(error);
    }

    return false;

}





/**
 * Función para ocultar alternativo cuando se hace hover a un elemento
 * @author Luis GP
 * @returns {Boolean}
 */
const hideBack = (div) => {

    try {
        
        $(div).removeClass('shown');
        $(div).addClass('hidden');

    } catch (error) {
        console.error(error);
    }

    return false;

}



/**
 * Función para ocultar alternativo cuando se hace hover a un elemento
 * @author Luis GP
 * @returns {Boolean}
 */
const guardarProducto = (form) => {

    try {

        let data = new FormData(form)
        data.append('descripcion', document.getElementById("editor").getElementsByClassName("ql-editor")[0].innerHTML)

        ajax({
            url: form.dataset.url,
            body: data,
            success: (data) => {
                window.location.href = urlBase+"/admin_panel/todos_productos/";
            },
            error: (data) => {
                alertError(data)
            }
        });
        
    } catch (error) {
        console.error(error);
    }

    return false;

}