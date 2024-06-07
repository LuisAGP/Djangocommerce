/**
 * Función para visualizar imagen  anterior del carrusel
 * @author Luis GP
 * @returns {Boolean}
 */
const previousImage = () => {

    try {
        
        let img = document.getElementsByClassName("img-active")[0];
        if (!img.previousElementSibling) return false;
        img.classList.remove('img-active');
        
        let prevImg = img.previousElementSibling;
        prevImg.classList.add('img-active');
        prevImg.focus();

        document.getElementById('imagen-zoomed').innerHTML = `<img src=${prevImg.dataset.img_url} class="img-fluid"/>`;

    } catch (error) {
        console.error(error);
    }

    return false;
    
}



/**
 * Función para visualizar la siguiente imagen del carrusel
 * @author Luis GP
 * @returns {Boolean}
 */
const nextImage = () => {

    try {
        
        let img = document.getElementsByClassName("img-active")[0];
        if (!img.nextElementSibling) return false;
        img.classList.remove('img-active');
        
        let nextImg = img.nextElementSibling;
        nextImg.classList.add('img-active');
        nextImg.focus();
        
        document.getElementById('imagen-zoomed').innerHTML = `<img src=${nextImg.dataset.img_url} class="img-fluid" />`;

    } catch (error) {
        console.error(error);
    }

    return false;
    
}



/**
 * Función para visualizar la imagen del carrusel que de clic el usuario
 * @author Luis GP
 * @returns {Boolean}
 */
const setImage = (element) => {

    try {

        let img = document.getElementsByClassName("img-active")[0];
        img.classList.remove('img-active');

        element.classList.add('img-active');
        element.focus()
        
        document.getElementById('imagen-zoomed').innerHTML = `
            <img src=${element.dataset.img_url} class="img-fluid" />
        `;
        
    } catch (error) {
        console.error(error);
    }

    return false;

}



/**
 * Función para obtener el stok de una talla
 * @author Luis GP
 * @param {Node DOM} select
 * @returns {Integer}
 */
const getStockOptions = (select) => {

    try {

        let data = new FormData()
        data.append('id_talla', select.value)
        
        ajax({
            url: '/get_stock',
            body: data,
            success: (response) => {

                let selectStock = document.getElementById('producto-stock');
                selectStock.innerHTML = "";
                
                for(let i = 1; i <= response.stock; i++ ){
                    selectStock.innerHTML += `<option value="${i}">${i}</option>`;
                }

                select.scrollIntoView(false);

            },
            error: (error) => {
                alertError(error);
            }
        });

    } catch (error) {
        console.error(error);
    }

    return 0

}



/**
 * Función para agregar un producto al carrito de compras
 * @author Luis GP
 * @return {Boolean}
 */
const agregarProductoCarrito =  () => {

    try {

        let talla = parseFloat(document.getElementById('producto-tallas').value)
        let data = new FormData(document.getElementById('form-comprar_producto'))

        if(!talla){
            alertError({
                message: "Debes seleccionar la talla"
            });

            return false;
        }

        ajax({
            url: "/agregar_producto/",
            body: data,
            success: (response) => {
                cargarMiniCarrito();
                let carrito = document.getElementById('mini_carrito');
                new bootstrap.Offcanvas(carrito).show()
            },
            error: (error) => {
                alertError(error);
            }
        })
        
    } catch (error) {
        console.error(error);
    }

    return false;

}