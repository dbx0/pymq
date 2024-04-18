CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    sender TEXT,
    recipient TEXT,
    read INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS valid_tokens (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    token TEXT UNIQUE DEFAULT gen_random_uuid()
);

CREATE FUNCTION update_read_timestamp() RETURNS trigger AS $$
BEGIN
  IF NEW.read = 1 THEN
    NEW.read_timestamp = CURRENT_TIMESTAMP;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_read_timestamp
BEFORE UPDATE ON messages
FOR EACH ROW
EXECUTE PROCEDURE update_read_timestamp();

INSERT INTO valid_tokens (username) VALUES ('telegram_bot') ON CONFLICT (username) DO NOTHING;
INSERT INTO valid_tokens (username) VALUES ('binance_bot') ON CONFLICT (username) DO NOTHING;
INSERT INTO valid_tokens (username) VALUES ('logic_gate') ON CONFLICT (username) DO NOTHING;
