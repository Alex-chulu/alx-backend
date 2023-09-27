const express = require('express');
const bodyParser = require('body-parser');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Create a Redis client
const client = redis.createClient();

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

app.use(bodyParser.json());

// Sample product data
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

// Function to get an item by ID
function getItemById(itemId) {
  return listProducts.find((product) => product.itemId === itemId);
}

// Route to list all products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Route to get product details
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);

  if (!product) {
    res.status(404).json({ status: 'Product not found' });
    return;
  }

  const currentQuantity = await getAsync(`item.${itemId}`) || 0;
  res.json({ ...product, currentQuantity: parseInt(currentQuantity) });
});

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);

  if (!product) {
    res.status(404).json({ status: 'Product not found' });
    return;
  }

  const currentQuantity = await getAsync(`item.${itemId}`) || 0;

  if (currentQuantity < 1) {
    res.json({ status: 'Not enough stock available', itemId });
    return;
  }

  // Decrement the stock in Redis
  await setAsync(`item.${itemId}`, currentQuantity - 1);

  res.json({ status: 'Reservation confirmed', itemId });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

