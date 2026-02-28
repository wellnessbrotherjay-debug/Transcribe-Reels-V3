const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

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

  if (!OPENAI_API_KEY) {
    return res.status(500).json({ error: 'Missing OPENAI_API_KEY environment variable.' });
  }

  const { text } = readJsonBody(req);

  if (!text || typeof text !== 'string' || text.trim().length < 20) {
    return res.status(400).json({ error: 'text is required and must be at least 20 characters.' });
  }

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        authorization: `Bearer ${OPENAI_API_KEY}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        temperature: 0.2,
        messages: [
          {
            role: 'system',
            content:
              'You summarize reel transcripts into clear creator notes. Return compact markdown with sections: Summary, Hooks, CTA Ideas.',
          },
          {
            role: 'user',
            content: text,
          },
        ],
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: 'OpenAI request failed.',
        details: data,
      });
    }

    const summary = data?.choices?.[0]?.message?.content || '';
    return res.status(200).json({ summary });
  } catch (error) {
    return res.status(500).json({
      error: 'Failed to contact OpenAI.',
      details: error instanceof Error ? error.message : String(error),
    });
  }
};
