const smtp = require('./smtp')


async function start() {
  try {
    await smtp()
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log('Mails error', e.message)
    process.exit(1)
  }
}

start()
