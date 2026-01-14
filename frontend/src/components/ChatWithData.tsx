import React, { useState } from 'react';
import {
  Card,
  CardHeader,
  Button,
  Text,
  makeStyles,
  tokens,
  Spinner,
} from '@fluentui/react-components';
import { CheckmarkCircle20Regular, DismissCircle20Regular } from '@fluentui/react-icons';

const useStyles = makeStyles({
  container: {
    padding: '20px',
    maxWidth: '800px',
    margin: '0 auto',
  },
  card: {
    marginBottom: '20px',
  },
  testSection: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
    padding: '20px',
  },
  buttonRow: {
    display: 'flex',
    gap: '12px',
    alignItems: 'center',
  },
  statusBox: {
    padding: '12px',
    borderRadius: '6px',
    marginTop: '12px',
  },
  statusSuccess: {
    backgroundColor: tokens.colorPaletteGreenBackground2,
    color: tokens.colorPaletteGreenForeground1,
  },
  statusError: {
    backgroundColor: tokens.colorPaletteRedBackground2,
    color: tokens.colorPaletteRedForeground1,
  },
  statusInfo: {
    backgroundColor: tokens.colorNeutralBackground2,
    color: tokens.colorNeutralForeground1,
  },
  statusContent: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  infoText: {
    color: tokens.colorNeutralForeground3,
    fontSize: '14px',
    marginTop: '8px',
  },
});

interface ConnectionStatus {
  connected: boolean;
  message: string;
  modelInfo?: {
    model: string;
    loadedModel?: string;
  };
}

export const ChatWithData: React.FC = () => {
  const styles = useStyles();
  const [testing, setTesting] = useState(false);
  const [status, setStatus] = useState<ConnectionStatus | null>(null);
  const [lmStudioUrl, setLmStudioUrl] = useState('http://localhost:1234');

  const testConnection = async () => {
    setTesting(true);
    setStatus(null);

    try {
      // Test LM Studio connection
      const response = await fetch(`${lmStudioUrl}/v1/models`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      setStatus({
        connected: true,
        message: 'Successfully connected to LM Studio!',
        modelInfo: {
          model: data.data?.[0]?.id || 'No model loaded',
          loadedModel: data.data?.[0]?.id,
        },
      });
    } catch (error) {
      setStatus({
        connected: false,
        message: error instanceof Error ? error.message : 'Failed to connect to LM Studio',
      });
    } finally {
      setTesting(false);
    }
  };

  const testSimpleEndpoint = async () => {
    setTesting(true);
    setStatus(null);

    try {
      // Test with a simple chat completion
      const response = await fetch(`${lmStudioUrl}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'local-model',
          messages: [
            {
              role: 'user',
              content: 'Say "Connection test successful" if you can read this.',
            },
          ],
          temperature: 0.7,
          max_tokens: 50,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const responseText = data.choices?.[0]?.message?.content || 'No response';

      setStatus({
        connected: true,
        message: `LM Studio responded: "${responseText}"`,
        modelInfo: {
          model: data.model || 'Unknown',
        },
      });
    } catch (error) {
      setStatus({
        connected: false,
        message: error instanceof Error ? error.message : 'Failed to send test message',
      });
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card className={styles.card}>
        <CardHeader
          header={<Text weight="semibold" size={500}>Chat with Your Data</Text>}
          description="Connect to LM Studio to chat with your Garmin health data using AI"
        />
        <div className={styles.testSection}>
          <div>
            <Text weight="semibold">LM Studio Connection Test</Text>
            <Text className={styles.infoText}>
              Make sure LM Studio is running locally with a model loaded.
              Default URL: http://localhost:1234
            </Text>
          </div>

          <div>
            <label>
              <Text size={300} weight="semibold">LM Studio URL:</Text>
              <input
                type="text"
                value={lmStudioUrl}
                onChange={(e) => setLmStudioUrl(e.target.value)}
                style={{
                  width: '100%',
                  padding: '8px',
                  marginTop: '4px',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                }}
                placeholder="http://localhost:1234"
              />
            </label>
          </div>

          <div className={styles.buttonRow}>
            <Button
              appearance="primary"
              onClick={testConnection}
              disabled={testing}
            >
              {testing ? (
                <>
                  <Spinner size="tiny" /> Testing...
                </>
              ) : (
                'Test Connection'
              )}
            </Button>

            <Button
              appearance="secondary"
              onClick={testSimpleEndpoint}
              disabled={testing}
            >
              {testing ? (
                <>
                  <Spinner size="tiny" /> Testing...
                </>
              ) : (
                'Test Chat Endpoint'
              )}
            </Button>
          </div>

          {status && (
            <div
              className={`${styles.statusBox} ${
                status.connected ? styles.statusSuccess : styles.statusError
              }`}
            >
              <div className={styles.statusContent}>
                {status.connected ? (
                  <CheckmarkCircle20Regular />
                ) : (
                  <DismissCircle20Regular />
                )}
                <div>
                  <Text weight="semibold">
                    {status.connected ? 'Connected' : 'Connection Failed'}
                  </Text>
                  <br />
                  <Text size={300}>{status.message}</Text>
                  {status.modelInfo && (
                    <>
                      <br />
                      <Text size={200}>Model: {status.modelInfo.model}</Text>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}

          {!status && !testing && (
            <div className={`${styles.statusBox} ${styles.statusInfo}`}>
              <Text size={300}>
                <strong>Setup Instructions:</strong>
                <br />
                1. Download and install LM Studio from lmstudio.ai
                <br />
                2. Load a model (e.g., Llama, Mistral, or Phi)
                <br />
                3. Start the local server (Server tab → Start Server)
                <br />
                4. Click "Test Connection" above
              </Text>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
};
