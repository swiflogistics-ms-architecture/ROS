const axios = require('axios');

async function optimizeRoutes(srcAddress, addresses, vehicles) {
  try {
    const response = await axios.post('http://127.0.0.1:5000/optimize', {
      srcAddress,
      addresses,
      vehicles
    });
    return response.data;
  } catch (error) {
    console.error('Error optimizing routes:', error.response ? error.response.data : error.message);
    throw error;
  }
}
