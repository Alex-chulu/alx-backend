import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Array of jobs
const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account'
  },
  // ... Add more jobs here
];

// Loop through the array of jobs and create Kue jobs
jobs.forEach((jobData, index) => {
  const job = queue.create('push_notification_code_2', jobData);

  job
    .on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    })
    .on('failed', (err) => {
      console.log(`Notification job ${job.id} failed: ${err}`);
    })
    .on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });

  job.save((err) => {
    if (!err) {
      console.log(`Notification job created: ${job.id}`);
    }
  });
});

