const amqp = require('amqplib')

const url = process.env.AMQP_HOST
const queue = process.env.QUEUE_NAME


const publishToQueue = async (message, durable = true) => {
    try {
        const cluster = await amqp.connect(url);
        const channel = await cluster.createChannel();
        await channel.assertQueue(queue, durable);
        await channel.sendToQueue(queue, Buffer.from(message));
        console.info(' [x] Sending message to queue', queue, message);
        await channel.close()
        await cluster.close()        
    } catch (error) {
        console.error(error, 'Unable to connect to cluster!');  
    }
}
module.exports = publishToQueue;
