import { expect } from 'chai';
import kue from 'kue';
import { createPushNotificationsJobs } from './8-job'; // Adjust the import path as needed

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    // Create a Kue queue in test mode
    queue = kue.createQueue({ redis: { createClientFactory: () => require('kue/lib/redis').createClient({ detect_buffers: true }) } });
  });

  afterEach(() => {
    // Clear the queue and exit test mode
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('invalid', queue)).to.throw('Jobs is not an array');
  });

  it('should create jobs and log events for each job', () => {
    const jobs = [
      { phoneNumber: '4151234567', message: 'Test message 1' },
      { phoneNumber: '4159876543', message: 'Test message 2' },
    ];

    createPushNotificationsJobs(jobs, queue);

    // Check if jobs are added to the queue
    expect(queue.testMode.jobs.length).to.equal(jobs.length);

    // Simulate processing the jobs (in real use, jobs would be processed by a worker)
    queue.testMode.jobs.forEach((job) => {
      job.process();
    });

    // Check if job creation, completion, and failure events were logged
    expect(queue.testMode.events).to.deep.equal([
      'enqueue',
      'enqueue',
      'complete',
      'complete',
    ]);
  });
});

