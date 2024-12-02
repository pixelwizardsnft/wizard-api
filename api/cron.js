export default async function handler(req, res) {
  const apiKey = process.env.API_KEY
  try {
    const response = await fetch('https://api.pixelwizards.art/v1/updateKnowledge', {
      method: 'POST',
      headers: {
        'X-Api-Key': apiKey,
        'Content-Type': 'application/json',
      },
    });

    const data = await response.text();

    res.status(200).send(data);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('Internal Server Error');
  }
}