import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Define the function to create push notification jobs
function createPushNotificationsJobs(jobs, queue) {
  // Check if jobs is not an array
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // Process each job in the array
  jobs.forEach((jobData) => {
    // Create a job in the queue push_notification_code_3
    const job = queue.create('push_notification_code_3', jobData);

    // Log when a job is created
    job.on('enqueue', () => {
      console.log(`Notification job created: ${job.id}`);
    });

    // Log when a job is completed
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });

    // Log when a job is failed
    job.on('failed', (err) => {
      console.log(`Notification job ${job.id} failed: ${err}`);
    });

    // Log progress when a job is making progress
    job.on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });

    // Save the job to the queue
    job.save();
  });
}

// Example usage:
const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account',
  },
];

try {
  createPushNotificationsJobs(jobs, queue);
} catch (error) {
  console.error(error.message);
}

// Close the queue connection when done
queue.on('job complete', (id) => {
  kue.Job.get(id, (err, job) => {
    if (err) return;
    job.remove(() => {
      console.log(`Removed completed job ${job.id}`);
    });
  });
});

// Log a message when the queue is ready
queue.on('ready', () => {
  console.log('Queue is ready to process jobs...');
});

// Log errors if they occur
queue.on('error', (err) => {
  console.error('Queue error:', err);
});

