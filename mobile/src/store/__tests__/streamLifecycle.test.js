/**
 * Lightweight stream lifecycle checks for chatStore helpers.
 * Run: node --test src/store/__tests__/streamLifecycle.test.js
 */
const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

function findStreamingMessageIndex(msgs, streamId, messageId) {
  if (!msgs?.length) return -1;
  if (streamId) {
    const byStream = msgs.findIndex((m) => m.streamId && String(m.streamId) === String(streamId));
    if (byStream >= 0) return byStream;
  }
  if (messageId) {
    const byId = msgs.findIndex((m) => String(m.id) === String(messageId));
    if (byId >= 0) return byId;
  }
  return -1;
}

function applyStreamLifecycle(messages, events) {
  let msgs = [...messages];
  for (const data of events) {
    if (data.type === 'stream_start') {
      msgs = [
        ...msgs,
        {
          id: `stream_${data.stream_id}`,
          content: '',
          streamId: data.stream_id,
          isStreaming: true,
          user: 'Misa',
        },
      ];
    } else if (data.type === 'stream_chunk') {
      const idx = findStreamingMessageIndex(msgs, data.stream_id, data.message_id);
      if (idx >= 0) {
        const next = [...msgs];
        next[idx] = {
          ...next[idx],
          content: `${next[idx].content || ''}${data.delta || ''}`,
          isStreaming: true,
        };
        msgs = next;
      }
    } else if (data.type === 'stream_end' || data.type === 'chat_message') {
      const idx = findStreamingMessageIndex(msgs, data.stream_id, data.message_id);
      if (idx >= 0) {
        const next = [...msgs];
        next[idx] = {
          ...next[idx],
          id: data.message_id || next[idx].id,
          content: data.message || next[idx].content,
          isStreaming: false,
        };
        msgs = next;
      } else if (data.type === 'chat_message') {
        msgs = [
          ...msgs,
          {
            id: data.message_id,
            content: data.message,
            user: 'Misa',
            isStreaming: false,
            streamId: data.stream_id,
          },
        ];
      }
    } else if (data.type === 'stream_error') {
      msgs = msgs.filter(
        (m) => !(m.isStreaming && String(m.streamId) === String(data.stream_id))
      );
    }
  }
  return msgs;
}

describe('stream lifecycle', () => {
  it('builds chunks then finalizes without duplicates', () => {
    const out = applyStreamLifecycle([], [
      { type: 'stream_start', stream_id: 's1' },
      { type: 'stream_chunk', stream_id: 's1', delta: 'Hel' },
      { type: 'stream_chunk', stream_id: 's1', delta: 'lo' },
      { type: 'stream_end', stream_id: 's1', message_id: '9', message: 'Hello' },
      { type: 'chat_message', stream_id: 's1', message_id: '9', message: 'Hello' },
    ]);
    assert.equal(out.length, 1);
    assert.equal(out[0].content, 'Hello');
    assert.equal(out[0].id, '9');
    assert.equal(out[0].isStreaming, false);
  });

  it('removes placeholder on error', () => {
    const out = applyStreamLifecycle([], [
      { type: 'stream_start', stream_id: 's2' },
      { type: 'stream_chunk', stream_id: 's2', delta: 'partial' },
      { type: 'stream_error', stream_id: 's2' },
    ]);
    assert.equal(out.length, 0);
  });
});
