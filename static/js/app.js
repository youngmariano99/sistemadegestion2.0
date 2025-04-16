// Función para formatear números como moneda
function formatCurrency(amount) {
    return '$' + parseFloat(amount).toFixed(2);
  }
  
  // Función para calcular subtotal (precio * cantidad)
  function calcularSubtotal() {
    const cantidad = parseFloat(document.getElementById('cantidad').value) || 0;
    const precio = parseFloat(document.getElementById('precio_unitario').value) || 0;
    const subtotal = cantidad * precio;
    document.getElementById('subtotal').value = subtotal.toFixed(2);
  }
  
  // Inicializar elementos cuando el DOM esté listo
  document.addEventListener('DOMContentLoaded', function() {
    // Inicializar los links activos en el sidebar
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    
    navLinks.forEach(link => {
      if (currentPath.includes(link.getAttribute('href'))) {
        link.classList.add('active');
      }
    });
    
    // Inicializar cálculos de subtotal en formularios de venta
    const cantidadInput = document.getElementById('cantidad');
    const precioInput = document.getElementById('precio_unitario');
    
    if (cantidadInput && precioInput) {
      cantidadInput.addEventListener('input', calcularSubtotal);
      precioInput.addEventListener('input', calcularSubtotal);
    }
    
    // Inicializar mensaje de alerta para que se cierre automáticamente
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => {
          alert.style.display = 'none';
        }, 500);
      }, 5000);
    });
  });
  
  // Función para seleccionar un producto
  function seleccionarProducto(selectElement) {
    const productoId = selectElement.value;
    if (!productoId) return;
    
    // Realizar una petición AJAX para obtener datos del producto
    fetch(`/productos/api/${productoId}`)
      .then(response => response.json())
      .then(producto => {
        // Actualizar campos del formulario
        document.getElementById('precio_unitario').value = producto.precio;
        document.getElementById('stock_disponible').textContent = producto.stock;
        calcularSubtotal();
      })
      .catch(error => console.error('Error al obtener datos del producto:', error));
  }
  