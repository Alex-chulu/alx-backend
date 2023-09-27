const express = require('express');
const bodyParser = require('body-parser');
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');

const app = express();
const port = 1245;

// Create a Redis client
const client = redis.createClient();

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Create a Kue queue
const queue = kue.createQueue();

app.use(bodyParser.json());

// Set the initial number of available seats
const initialAvailableSeats = 50;
client.set('available_seats', initialAvailableSeats);

// Set the reservationEnabled flag
let reservationEnabled = true;

// Function to reserve a seat
function reserveSeat(number) {
  return setAsync('available_seats', number);
}

// Function to get the current available seats
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats);
}

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const currentAvailableSeats = await getCurrentAvailableSeats();

  if (currentAvailableSeats <= 0) {
    res.json({ status: 'Reservation failed' });
    return;
  }

  // Create and queue a job
  const job = queue.create('reserve_seat', {}).save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

// Route to process the queue and decrease available seats
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  // Process the queue
  queue.process('reserve_seat', async (job, done) => {
    const currentAvailableSeats = await getCurrentAvailableSeats();

    if (currentAvailableSeats <= 0) {
      done(new Error('Not enough seats available'));
    } else {
      const newAvailableSeats = currentAvailableSeats - 1;
      await reserveSeat(newAvailableSeats);

      if (newAvailableSeats === 0) {
        reservationEnabled = false;
      }

      done();
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

