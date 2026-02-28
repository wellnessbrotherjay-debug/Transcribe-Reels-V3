const ASSEMBLYAI_API_KEY = process.env.ASSEMBLYAI_API_KEY;

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed. Use GET.' });
  }

  if (!ASSEMBLYAI_API_KEY) {
    return res.status(500).json({ error: 'Missing ASSEMBLYAI_API_KEY environment variable.' });
  }

  const { id } = req.query || {};

  if (!id || typeof id !== 'string') {
    return res.status(400).json({ error: 'Query parameter id is required.' });
  }

  try {
    const response = await fetch(`https://api.assemblyai.com/v2/transcript/${encodeURIComponent(id)}`, {
      method: 'GET',
      headers: {
        authorization: ASSEMBLYAI_API_KEY,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: 'AssemblyAI status lookup failed.',
        details: data,
      });
    }

    return res.status(200).json({
      id: data.id,
      status: data.status,
      language_code: data.language_code,
      text: data.text || '',
      error: data.error || null,
    });
  } catch (error) {
    return res.status(500).json({
      error: 'Failed to fetch transcript status.',
      details: error instanceof Error ? error.message : String(error),
    });
  }
};
