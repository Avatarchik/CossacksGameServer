import os
import json
import redis
import socket
import struct
import logging

SERVER_HOST = ''
SERVER_PORT = 3708
LOGGER_FMT = '%(asctime)s %(levelname)s:%(message)s'

logging.basicConfig(filename='stun.log',
                    format=LOGGER_FMT, level=logging.DEBUG)
log_fmt = logging.Formatter(LOGGER_FMT)
stdout_log = logging.StreamHandler()
stdout_log.setFormatter(log_fmt)
logging.getLogger().addHandler(stdout_log)


def parse_packet(packet):
    tag, version = struct.unpack('<4sc', packet[0:5])
    player_id = struct.unpack('>L', packet[5:9])[0]
    access_key = struct.unpack('16s', packet[9:])[0].decode('utf-8')
    access_key = access_key[:access_key.index('\0')]
    return tag.decode('utf-8'), version[0], player_id, access_key


def get_handler(storage, keep_alive_interval):
    keep_alive_interval = int(keep_alive_interval * 1.5)
    notify = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def handle_packet(packet, remote):
        try:
            host, port = remote
            tag, version, player_id, access_key = parse_packet(packet)
            remote_info = {
                'host': host,
                'port': port,
                'version': version,
                'access_key': access_key
            }
            if tag != 'CSHP':
                logging.warning(f'unknown packet {packet}')
            if version == 1:
                if storage.set(
                        player_id,
                        json.dumps(remote_info),
                        px=keep_alive_interval):
                    logging.debug(f'player_id {player_id} ({host},{port})')
                    notify.sendto(b'ok', remote)
                else:
                    logging.warning(f'player_id {player_id} is not saved')
            else:
                logging.warning('version %d is not supported', version)

        except struct.error:
            logging.error(f'invalid packet {packet}')

    return handle_packet


def main():
    storage_host = 'redis'
    try:
        socket.gethostbyname(storage_host)
    except socket.gaierror:
        storage_host = 'localhost'
    storage = redis.StrictRedis(host=storage_host, port=6379, db=0)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    handle_packet = get_handler(
        storage, int(os.environ.get('UDP_KEEP_ALIVE_INTERVAL', '1000')))

    while True:
        packet, remote_addr = server.recvfrom(512)
        handle_packet(packet, remote_addr)


if __name__ == '__main__':
    main()
