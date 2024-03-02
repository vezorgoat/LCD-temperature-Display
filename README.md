[Unit]
Description=TDS Sensor Service
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/your/script/tds_sensor.py

[Install]
WantedBy=multi-user.target
