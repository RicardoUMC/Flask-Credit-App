let chartInstance = null;

/**
 * The function `obtenerDatos` asynchronously fetches credit data from an API endpoint and returns the
 * parsed JSON response, handling errors by logging them and returning an empty array.
 * @returns The function `obtenerDatos` is returning the data fetched from the '/api/creditos' endpoint
 * as a JSON object if the fetch is successful. If there is an error during the fetch or parsing of the
 * response, an empty array `[]` is returned.
 */
async function obtenerDatos() {
    try {
        const response = await fetch('/api/creditos');
        const datos = await response.json();
        return datos;
    } catch (error) {
        console.error('Error al obtener los datos:', error);
        return [];
    }
}

/**
 * The function generates a bar chart showing the total credits per client based on the provided data.
 * @param datos - An array of objects where each object represents a credit transaction with the
 * following properties:
 * @returns A Chart object representing a bar chart displaying the total credits per client, based on
 * the provided data.
 */
function generarGraficaCreditosPorCliente(datos) {
    const clientes = datos.map(credito => credito.cliente);
    const montos = datos.map(credito => credito.monto);

    const creditosCtx = document.getElementById('creditosChart').getContext('2d');
    return new Chart(creditosCtx, {
        type: 'bar',
        data: {
            labels: clientes,
            datasets: [{
                label: 'Total de Créditos por Cliente',
                data: montos,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

/**
 * The function `generarGraficaDistribucionPorRangos` generates a bar chart showing the distribution of
 * credits based on different ranges of amounts.
 * @param datos - The function `generarGraficaDistribucionPorRangos` takes an array of credit data
 * (`datos`) as input. Each element in the `datos` array represents a credit object with a `monto`
 * property indicating the amount of the credit.
 * @returns A Chart.js object representing a bar chart showing the distribution of credits by range of
 * amounts based on the input data.
 */
function generarGraficaDistribucionPorRangos(datos) {
    const rangos = { '0-1000': 0, '1000-5000': 0, '5000+': 0 };

    datos.forEach(credito => {
        if (credito.monto <= 1000) {
            rangos['0-1000']++;
        } else if (credito.monto <= 5000) {
            rangos['1000-5000']++;
        } else {
            rangos['5000+']++;
        }
    });

    const rangosCtx = document.getElementById('rangosChart').getContext('2d');
    return new Chart(rangosCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(rangos),
            datasets: [{
                label: 'Distribución de Créditos por Rango de Montos',
                data: Object.values(rangos),
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

/**
 * The function `toggleGrafica` toggles the display of a chart container and updates the text content
 * of a button accordingly.
 */
function toggleGrafica() {
    const chartContainer = document.querySelector('.chart-container.active');
    if (chartContainer && chartContainer.style.display === 'none') {
        chartContainer.style.display = 'block';
        toggleChartButton.textContent = 'Ocultar Gráfica';
    } else {
        chartContainer.style.display = 'none';
        toggleChartButton.textContent = 'Mostrar Gráfica';
    }
}

/**
 * The function "cargarDatosYGenerarGraficas" asynchronously loads data and generates different types
 * of charts based on user selection.
 */
async function cargarDatosYGenerarGraficas() {
    const datos = await obtenerDatos();

    if (datos.length > 0) {
        chartSelector.addEventListener('change', (event) => {
            const selectedChart = event.target.value;

            document.querySelectorAll('.chart-container').forEach(container => {
                container.classList.remove('active');
                container.style.display = 'none';
            });

            toggleChartButton.style.display = 'initial';

            if (selectedChart === 'creditosChart') {
                if (chartInstance) chartInstance.destroy();
                chartInstance = generarGraficaCreditosPorCliente(datos);
                creditosChartContainer.classList.add('active');
                creditosChartContainer.style.display = 'block';
                toggleChartButton.textContent = 'Ocultar Gráfica';
            } else if (selectedChart === 'rangosChart') {
                if (chartInstance) chartInstance.destroy();
                chartInstance = generarGraficaDistribucionPorRangos(datos);
                rangosChartContainer.classList.add('active');
                rangosChartContainer.style.display = 'block';
                toggleChartButton.textContent = 'Ocultar Gráfica';
            } else {
                toggleChartButton.style.display = 'none';
            }
        });

        toggleChartButton.addEventListener('click', toggleGrafica);
    }
}

cargarDatosYGenerarGraficas();
