const { SMTPServer } = require('smtp-server')
const { simpleParser } = require('mailparser')
const publishToQueue = require('./producer')

let mailserver

async function startSMTPServer() {
  const { smtpPort } = process.env
  mailserver = new SMTPServer({
    logger: false,
    authOptional: true,
    disabledCommands: ['AUTH'],
    disableReverseLookup: true,
    onConnect(session, callback) {
      return callback()
    },
    onMailFrom(address, session, callback) {
      // eslint-disable-next-line no-console
      console.info(`SMTP MAIL FROM: ${address.address}`)
      return callback()
    },
    onData(stream, session, callback) {
      let mailDataSting = ''

      stream.on('data', (chunk) => {
        mailDataSting += chunk
      })

      stream.on('end', async () => {
        await simpleParser(mailDataSting, async (err, mail) => {
          const { text, html, textAsHtml } = mail
          const from_at = mail.from.value[0].address
          const to = mail.to.value[0].address
          const subject = mail.headers.get('subject')

          const m = JSON.stringify({
            subject,
            from_at,
            to,
            text,
            html,
            textAsHtml})
          await publishToQueue(m);
        })
        return callback()
      })
    },
  })

  mailserver.on('error', (err) => {
    // eslint-disable-next-line no-console
    console.info(`Error ${err.message}`)
  })
  mailserver.listen(smtpPort)
  return mailserver
}

module.exports = startSMTPServer
