import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
    let queue;

    before(() => {
        queue = kue.createQueue();
        queue.testMode.enter();
    });

    after(() => {
        queue.testMode.clear();
        queue.testMode.exit();
    });

    it('display an error message if jobs is not an array', () => {
        expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
    });

    it('create two new jobs to the queue', () => {
        const jobs = [
            { phoneNumber: '1234567890', message: 'Test message 1' },
            { phoneNumber: '0987654321', message: 'Test message 2' }
        ];

        createPushNotificationsJobs(jobs, queue);

        expect(queue.testMode.jobs.length).to.equal(2);

        expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[0].data.phoneNumber).to.equal('1234567890');
        expect(queue.testMode.jobs[0].data.message).to.equal('Test message 1');

        expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[1].data.phoneNumber).to.equal('0987654321');
        expect(queue.testMode.jobs[1].data.message).to.equal('Test message 2');
    });
});
