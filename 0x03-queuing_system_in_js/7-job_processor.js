import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Array of blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Create a function to send notifications
function sendNotification(phoneNumber, message, job, done) {
  // Track the progress of the job
  job.progress(0, 100);

  // Check if phoneNumber is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    // Fail the job with an error
    done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  } else {
    // Update progress to 50%
    job.progress(50, 100);

    // Log the notification message
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    
    // Complete the job
    done();
  }
}

// Set up queue processing for push_notification_code_2
queue.process('push_notification_code_2', 2, (job, done) => {
  // Extract data from the job
  const { phoneNumber, message } = job.data;

  // Call the sendNotification function
  sendNotification(phoneNumber, message, job, done);
});

// Log a message when the queue is ready
queue.on('ready', () => {
  console.log('Queue is ready to process jobs...');
});

// Log errors if they occur
queue.on('error', (err) => {
  console.error('Queue error:', err);
});

