const ASSEMBLYAI_API_KEY = process.env.ASSEMBLYAI_API_KEY;

function readJsonBody(req) {
  if (!req.body) return {};
  if (typeof req.body === 'object') return req.body;
  try {
    return JSON.parse(req.body);
  } catch {
    return {};
  }
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed. Use POST.' });
  }

  if (!ASSEMBLYAI_API_KEY) {
    return res.status(500).json({ error: 'Missing ASSEMBLYAI_API_KEY environment variable.' });
  }

  const { mediaUrl } = readJsonBody(req);

  if (!mediaUrl || typeof mediaUrl !== 'string') {
    return res.status(400).json({ error: 'mediaUrl is required.' });
  }

  let parsed;
  try {
    parsed = new URL(mediaUrl);
  } catch {
    return res.status(400).json({ error: 'mediaUrl must be a valid URL.' });
  }

  if (!/^https?:$/.test(parsed.protocol)) {
    return res.status(400).json({ error: 'mediaUrl must start with http or https.' });
  }

  try {
    const response = await fetch('https://api.assemblyai.com/v2/transcript', {
      method: 'POST',
      headers: {
        authorization: ASSEMBLYAI_API_KEY,
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        audio_url: mediaUrl,
        speech_model: 'best',
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: 'AssemblyAI rejected transcript creation.',
        details: data,
      });
    }

    return res.status(200).json({
      id: data.id,
      status: data.status,
    });
  } catch (error) {
    return res.status(500).json({
      error: 'Failed to contact AssemblyAI.',
      details: error instanceof Error ? error.message : String(error),
    });
  }
};
