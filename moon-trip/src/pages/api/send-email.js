import { Resend } from 'resend';

const resend = new Resend(config.resend_api_key);
//API Request to send email through server
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { to, startDate, endDate, earthCoords, moonCoords, name } = req.body;

  try {
    await resend.emails.send({
      from: 'rocketssrl@development.com',
      to: [to],
      subject: 'Your Rocket Trip is Confirmed!',
      html: `<p>Hey ${name || ''},</p>
        <p>Your trip from Earth to the Moon has been successfully planned 🚀</p>
        <ul>
          <li><strong>Departure:</strong> ${startDate}</li>
          <li><strong>Return:</strong> ${endDate}</li>
          <li><strong>Launch Site:</strong> (${earthCoords.lat.toFixed(4)}, ${earthCoords.lng.toFixed(4)})</li>
          <li><strong>Moon Landing:</strong> (${moonCoords.lat.toFixed(4)}, ${moonCoords.lng.toFixed(4)})</li>
        </ul>
        <p>Safe travels, astronaut!</p>`
    });

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Email error:', error);
    return res.status(500).json({ success: false, error: error.message });
  }
}
