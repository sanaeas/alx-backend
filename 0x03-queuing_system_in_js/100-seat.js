import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const port = 1245;

const client = redis.createClient();

let availableSeats = 50;
let reservationEnabled = true;

const queue = kue.createQueue();

const reserveSeat = async (number) => {
  await promisify(client.set).bind(client)('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  const seats = await promisify(client.get).bind(client)('available_seats');
  return seats ? parseInt(seats) : availableSeats;
};

reserveSeat(availableSeats);

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', (result) => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentAvailableSeats = await getCurrentAvailableSeats();

    if (currentAvailableSeats <= 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      await reserveSeat(currentAvailableSeats - 1);

      if (currentAvailableSeats === 0) {
        reservationEnabled = false;
      }

      done();
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
